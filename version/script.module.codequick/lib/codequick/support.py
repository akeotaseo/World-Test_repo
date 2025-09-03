from __future__ import absolute_import
import importlib
import binascii
import inspect
import logging
import time
import sys
import re
import xbmcaddon
import xbmcgui
import xbmc
from codequick.utils import parse_qs, ensure_native_str, urlparse, unicode_type
import pickle
from inspect import getfullargspec
PICKLE_PROTOCOL = 4
script_data = xbmcaddon.Addon("script.module.codequick")
addon_data = xbmcaddon.Addon()
plugin_id = addon_data.getAddonInfo("id")
logger_id = re.sub("[ .]", "-", addon_data.getAddonInfo("name"))
logger = logging.getLogger(f"{logger_id}.support")
auto_sort = set()
logging_map = {
    10: xbmc.LOGDEBUG,
    20: xbmc.LOGINFO,
    30: xbmc.LOGWARNING,
    40: xbmc.LOGERROR,
    50: xbmc.LOGFATAL,
}
class KodiLogHandler(logging.Handler):
    def __init__(self):
        super(KodiLogHandler, self).__init__()
        self.setFormatter(logging.Formatter("[%(name)s] %(message)s"))
        self.debug_msgs = []
    def emit(self, record):
        formatted_msg = ensure_native_str(self.format(record))
        log_level = record.levelno
        xbmc.log(formatted_msg, logging_map.get(log_level, 10))
        if log_level == 10:
            self.debug_msgs.append(formatted_msg)

        elif log_level == 50 and self.debug_msgs:
            xbmc.log("###### debug ######", xbmc.LOGWARNING)
            for msg in self.debug_msgs:
                xbmc.log(msg, xbmc.LOGWARNING)
            xbmc.log("###### debug ######", xbmc.LOGWARNING)
class CallbackRef(object):
    __slots__ = ("path", "parent", "is_playable", "is_folder")
    def __init__(self, path, parent):
        self.path = path.rstrip("/").replace(":", "/")
        self.is_playable = parent.is_playable
        self.is_folder = parent.is_folder
        self.parent = parent
    def __eq__(self, other):
        return self.path == other.path
class Route(CallbackRef):
    __slots__ = ("function", "callback", "parameters")
    def __init__(self, callback, parent, path, parameters):
        if inspect.isclass(callback):
            msg = "Use of class based callbacks are Deprecated, please use function callbacks"
            logger.warning("DeprecationWarning: " + msg)
            if hasattr(callback, "run"):
                parent = callback
                self.function = callback.run
                callback.test = staticmethod(self.unittest_caller)
            else:
                raise NameError(f"missing required 'run' method for class: '{callback.__name__}'")
        else:
            callback.test = self.unittest_caller
            self.parameters = parameters
            self.function = callback
        super(Route, self).__init__(path, parent)
        self.callback = callback
    def unittest_caller(self, *args, **kwargs):
        execute_delayed = kwargs.pop("execute_delayed", False)
        dispatcher.selector = self.path
        if args:
            dispatcher.params["_args_"] = args
        if kwargs:
            dispatcher.params.update(kwargs)
        parent_ins = self.parent()
        try:
            results = self.function(parent_ins, *args, **kwargs)
            if inspect.isgenerator(results):
                results = list(results)
        except Exception:
            raise
        else:
            if execute_delayed:
                dispatcher.run_delayed()
            return results
        finally:
            dispatcher.reset()
            auto_sort.clear()
class Dispatcher(object):
    def __init__(self):
        self.registered_delayed = []
        self.registered_routes = {}
        self.callback_params = {}
        self.selector = "root"
        self.params = {}
        self.handle = -1
    def reset(self):
        self.registered_delayed[:] = []
        self.callback_params.clear()
        kodi_logger.debug_msgs = []
        self.selector = "root"
        self.params.clear()
        auto_sort.clear()
    def parse_args(self, redirect=None):
        _, _, route, raw_params, _ = urlparse.urlsplit(redirect if redirect else sys.argv[0] + sys.argv[2])
        self.selector = route if len(route) > 1 else "root"
        self.handle = int(sys.argv[1])

        if raw_params:
            params = parse_qs(raw_params)
            self.params.update(params)
            if "_pickle_" in params:
                unpickled = pickle.loads(binascii.unhexlify(self.params.pop("_pickle_")))
                self.params.update(unpickled)
            self.callback_params = {key: value for key, value in self.params.items()
                                    if not (key.startswith(u"_") and key.endswith(u"_"))}
    def get_route(self, path=None):
        path = path.rstrip("/") if path else self.selector.rstrip("/")
        if path not in self.registered_routes:
            module_path = "resources.lib.main" if path == "root" else ".".join(path.strip("/").split("/")[:-1])
            logger.debug("Attempting to import route: %s", module_path)
            try:
                importlib.import_module(module_path)
            except ImportError:
                raise RouteMissing(f"unable to import route module: {module_path}")
        try:
            return self.registered_routes[path]
        except KeyError:
            raise RouteMissing(path)
    def register_callback(self, callback, parent, parameters):
        path = callback.__name__.lower()
        if path != "root":
            path = f'/{callback.__module__.strip("_").replace(".", "/")}/{callback.__name__}'.lower()
        if path in self.registered_routes:
            logger.debug("encountered duplicate route: '%s'", path)
        self.registered_routes[path] = route = Route(callback, parent, path, parameters)
        callback.route = route
        return callback
    def register_delayed(self, *callback):
        self.registered_delayed.append(callback)
    def run_callback(self, process_errors=True, redirect=None):
        self.reset()
        self.parse_args(redirect)
        logger.debug("Dispatching to route: '%s'", self.selector)
        logger.debug("Callback parameters: '%s'", self.callback_params)
        try:
            route = self.get_route(self.selector)
            execute_time = time.time()
            parent_ins = route.parent()
            arg_params = self.params.get("_args_", [])
            redirect = parent_ins(route, arg_params, self.callback_params)
        except Exception as e:
            self.run_delayed(e)
            if not process_errors:
                raise
            try:
                msg = str(e)
            except UnicodeEncodeError:
                msg = unicode_type(e).encode("utf8")
            logger.exception(msg)
            dialog = xbmcgui.Dialog()
            dialog.notification(e.__class__.__name__, msg, addon_data.getAddonInfo("icon"))
            return e
        else:
            logger.debug("Route Execution Time: %ims", (time.time() - execute_time) * 1000)
            self.run_delayed()
            if redirect:
                self.run_callback(process_errors, redirect)
    def run_delayed(self, exception=None):
        if self.registered_delayed:
            start_time = time.time()
            while self.registered_delayed:
                func, args, kwargs, function_type = self.registered_delayed.pop()
                if function_type == 2 or bool(exception) == function_type:
                    if "exception" in getfullargspec(func).args:
                        kwargs["exception"] = exception
                    try:
                        func(*args, **kwargs)
                    except Exception as e:
                        logger.exception(str(e))
            logger.debug("Callbacks Execution Time: %ims", (time.time() - start_time) * 1000)
def build_path(callback=None, args=None, query=None, **extra_query):
    if callback and hasattr(callback, "route"):
        route = callback.route
    elif isinstance(callback, CallbackRef):
        route = callback
    elif callback:
        msg = "passing in callback path is deprecated, use callback reference 'Route.ref' instead"
        logger.warning("DeprecationWarning: " + msg)
        route = dispatcher.get_route(callback)
    else:
        route = dispatcher.get_route()
    if args:
        query["_args_"] = args
    if extra_query:
        query = dispatcher.params.copy()
        query.update(extra_query)
    if query:
        pickled = binascii.hexlify(pickle.dumps(query, protocol=PICKLE_PROTOCOL))
        query = f'_pickle_={pickled.decode("ascii")}'
    return urlparse.urlunsplit(("plugin", plugin_id, route.path + "/", query, ""))
kodi_logger = KodiLogHandler()
base_logger = logging.getLogger()
base_logger.addHandler(kodi_logger)
base_logger.setLevel(logging.DEBUG)
base_logger.propagate = False
dispatcher = Dispatcher()
run = dispatcher.run_callback
get_route = dispatcher.get_route