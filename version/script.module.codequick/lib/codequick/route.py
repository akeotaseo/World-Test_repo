from __future__ import absolute_import
from collections import defaultdict
from operator import itemgetter
import logging
import inspect
import hashlib
import sys
import re
import xbmcplugin
from codequick.storage import Cache
from codequick.script import Script
from codequick.support import logger_id, auto_sort
from codequick.utils import ensure_native_str
__all__ = ["Route", "validate_listitems"]
logger = logging.getLogger(f"{logger_id}.route")
def get_session_id():
    url = sys.argv[0] + sys.argv[2]
    url = url.encode("utf8") if isinstance(url, type(u"")) else url
    return hashlib.sha1(url).hexdigest()
def validate_listitems(raw_listitems):
    if inspect.isgenerator(raw_listitems):
        raw_listitems = list(raw_listitems)
    elif raw_listitems is False:
        return False
    if raw_listitems:
        if isinstance(raw_listitems, (list, tuple)):
            return False if len(raw_listitems) == 1 and raw_listitems[0] is False else list(filter(None, raw_listitems))
        else:
            raise ValueError(f"Unexpected return object: {type(raw_listitems)}")
    else:
        raise RuntimeError("No items found")
def guess_content_type(mediatypes):
    if len(mediatypes) > 1:
        mediatype = sorted(mediatypes.items(), key=itemgetter(1))[-1][0]
    elif mediatypes:
        mediatype = mediatypes.popitem()[0]
    else:
        return ""
    if mediatype in ("video", "movie", "tvshow", "episode", "musicvideo", "song", "album", "artist"):
        return mediatype + "s"
def build_sortmethods(manualsort, autosort):
    if autosort:
        if not (manualsort or xbmcplugin.SORT_METHOD_DATE in autosort):
            manualsort.append(xbmcplugin.SORT_METHOD_UNSORTED)
        for method in sorted(autosort):
            if method not in manualsort:
                manualsort.append(method)
    return manualsort if manualsort else [xbmcplugin.SORT_METHOD_UNSORTED]
def send_to_kodi(handle, session):
    if session["content_type"] == -1:
        kodi_listitems = []
        folder_counter = 0.0
        mediatypes = defaultdict(int)
        for listitem in session["listitems"]:
            listitem_tuple = listitem.build()
            kodi_listitems.append(listitem_tuple)
            if "mediatype" in listitem.info:
                mediatypes[listitem.info["mediatype"]] += 1
            if listitem_tuple[2]:
                folder_counter += 1
        session["content_type"] = guess_content_type(mediatypes)
        if not session["content_type"]:
            isfolder = folder_counter > (len(kodi_listitems) / 2)
            session["content_type"] = "files" if isfolder else "videos"
    else:
        kodi_listitems = [custom_listitem.build() for custom_listitem in session["listitems"]]
    if session["redirect"] and len(kodi_listitems) == 1 and kodi_listitems[0][2] is True:
        return kodi_listitems[0][0]
    for sortMethod in session["sortmethods"]:
        xbmcplugin.addSortMethod(handle, sortMethod)
    if session["category"]:
        xbmcplugin.setPluginCategory(handle, ensure_native_str(session["category"]))
    if session["content_type"]:
        xbmcplugin.setContent(handle, ensure_native_str(session["content_type"]))
    success = xbmcplugin.addDirectoryItems(handle, kodi_listitems, len(kodi_listitems))
    xbmcplugin.endOfDirectory(handle, success, session["update_listing"], session["cache_to_disc"])
class Route(Script):
    is_folder = True
    def __init__(self):
        super(Route, self).__init__()
        self.update_listing = self.params.get(u"_updatelisting_", False)
        self.category = re.sub(r"\(\d+\)$", u"", self._title).strip()
        self.cache_to_disc = self.params.get(u"_cache_to_disc_", True)
        self.redirect_single_item = False
        self.sort_methods = list()
        self.content_type = -1
        self.autosort = True
    def __call__(self, route, args, kwargs):
        cache_ttl = getattr(self, "cache_ttl", -1)
        cache = Cache("listitem_cache.sqlite", cache_ttl * 60) if cache_ttl >= 0 else None
        session_id = get_session_id()
        if cache and session_id in cache:
            logger.debug("Listitem Cache: Hit")
            session_data = cache[session_id]
        else:
            logger.debug("Listitem Cache: Miss")
            try:
                results = super(Route, self).__call__(route, args, kwargs)
                session_data = self._process_results(results)
                if session_data and cache:
                    cache[session_id] = session_data
                elif not session_data:
                    return None
            finally:
                if cache:
                    cache.close()
        return send_to_kodi(self.handle, session_data)
    def _process_results(self, results):
        listitems = validate_listitems(results)
        if listitems is False:
            xbmcplugin.endOfDirectory(self.handle, False)
            return None
        return {
            "listitems": listitems,
            "category": ensure_native_str(self.category),
            "update_listing": self.update_listing,
            "cache_to_disc": self.cache_to_disc,
            "sortmethods": build_sortmethods(self.sort_methods, auto_sort if self.autosort else None),
            "content_type": self.content_type,
            "redirect": self.redirect_single_item
        }
    def add_sort_methods(self, *methods, **kwargs):
        if kwargs.get("disable_autosort", False):
            self.autosort = False
        for method in methods:
            self.sort_methods.append(method)