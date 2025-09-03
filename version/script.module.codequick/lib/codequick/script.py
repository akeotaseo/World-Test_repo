from __future__ import absolute_import
import logging
import inspect
import os
import xbmcaddon
import xbmcvfs
import xbmcgui
import xbmc
from codequick.utils import ensure_unicode, ensure_native_str, unicode_type, string_map
from codequick.support import dispatcher, script_data, addon_data, logger_id, CallbackRef
translatePath = xbmcvfs.translatePath
__all__ = ["Script", "Settings"]
addon_logger = logging.getLogger(logger_id)
class Settings(object):
    def __getitem__(self, key):
        return addon_data.getSetting(key)
    def __setitem__(self, key, value):
        addon_data.setSetting(key, ensure_unicode(value))
    def __delitem__(self, key):
        addon_data.setSetting(key, "")
    @staticmethod
    def get_string(key, addon_id=None):
        if addon_id:
            return xbmcaddon.Addon(addon_id).getSetting(key)
        else:
            return addon_data.getSetting(key)
    @staticmethod
    def get_boolean(key, addon_id=None):
        setting = Settings.get_string(key, addon_id).lower()
        return setting == u"true" or setting == u"1"
    @staticmethod
    def get_int(key, addon_id=None):
        return int(Settings.get_string(key, addon_id))
    @staticmethod
    def get_number(key, addon_id=None):
        return float(Settings.get_string(key, addon_id))
class Script(object):
    is_playable = False
    is_folder = False
    CRITICAL = 50
    WARNING = 30
    ERROR = 40
    DEBUG = 10
    INFO = 20
    NOTIFY_WARNING = 'warning'
    NOTIFY_ERROR = 'error'
    NOTIFY_INFO = 'info'
    setting = Settings()
    logger = addon_logger
    params = dispatcher.params
    def __init__(self):
        self._title = self.params.get(u"_title_", u"")
        self.handle = dispatcher.handle
    def __call__(self, route, args, kwargs):
        self.__dict__.update(route.parameters)
        return route.function(self, *args, **kwargs)
    @classmethod
    def ref(cls, path):
        return CallbackRef(path, cls)
    @classmethod
    def register(cls, func=None, **kwargs):
        if inspect.isfunction(func):
            return dispatcher.register_callback(func, parent=cls, parameters=kwargs)
        elif func is None:
            def wrapper(real_func):
                return dispatcher.register_callback(real_func, parent=cls, parameters=kwargs)
            return wrapper
        else:
            raise ValueError("Only keyword arguments are allowed")
    @staticmethod
    def register_delayed(func, *args, **kwargs):
        function_type = kwargs.get("function_type", 0)
        dispatcher.register_delayed(func, args, kwargs, function_type)
    @staticmethod
    def log(msg, args=None, lvl=10):
        if args:
            addon_logger.log(lvl, msg, *args)
        else:
            addon_logger.log(lvl, msg)
    @staticmethod
    def notify(heading, message, icon=None, display_time=5000, sound=True):
        heading = ensure_native_str(heading)
        message = ensure_native_str(message)
        icon = ensure_native_str(icon if icon else Script.get_info("icon"))
        dialog = xbmcgui.Dialog()
        dialog.notification(heading, message, icon, display_time, sound)
    @staticmethod
    def localize(string_id):
        if isinstance(string_id, (str, unicode_type)):
            try:
                numeric_id = string_map[string_id]
            except KeyError:
                raise KeyError(f"no localization found for string id '{string_id}'")
            else:
                return addon_data.getLocalizedString(numeric_id)
        elif 30000 <= string_id <= 30999:
            return addon_data.getLocalizedString(string_id)
        elif 32000 <= string_id <= 32999:
            return script_data.getLocalizedString(string_id)
        else:
            return xbmc.getLocalizedString(string_id)
    @staticmethod
    def get_info(key, addon_id=None):
        if addon_id:
            resp = xbmcaddon.Addon(addon_id).getAddonInfo(key)
        elif key == "path_global" or key == "profile_global":
            resp = script_data.getAddonInfo(key[:key.find("_")])
        else:
            resp = addon_data.getAddonInfo(key)
        if resp[:10] == "special://":
            resp = translatePath(resp)
        path = resp.decode("utf8") if isinstance(resp, bytes) else resp
        if key.startswith("profile"):
            if not os.path.exists(path):
                os.mkdir(path)
        return path