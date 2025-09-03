from __future__ import absolute_import
import logging
import inspect
import xbmcplugin
import xbmcgui
import xbmc
from codequick.script import Script
from codequick.support import build_path, logger_id
from codequick.utils import unicode_type, ensure_unicode
from codequick import localized
__all__ = ["Resolver"]
logger = logging.getLogger(f"{logger_id}.resolver")
class Resolver(Script):
    is_playable = True
    def __init__(self):
        super(Resolver, self).__init__()
        self.playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        self._extra_commands = {}
    def __call__(self, route, args, kwargs):
        results = super(Resolver, self).__call__(route, args, kwargs)
        return self._process_results(results)
    def create_loopback(self, url, **next_params):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        main_listitem = xbmcgui.ListItem()
        main_listitem.setPath(url)
        if self._title.startswith(u"_loopback_"):
            main_listitem.setLabel(self._title.split(u" - ", 1)[1])
            next_params["_title_"] = self._title
        else:
            main_listitem.setLabel(self._title)
            next_params["_title_"] = f"_loopback_ - {self._title}"
            playlist.clear()
            playlist.add(url, main_listitem)
        loop_listitem = xbmcgui.ListItem()
        loop_listitem.setLabel(next_params["_title_"])
        loopback_url = build_path(**next_params)
        loop_listitem.setPath(loopback_url)
        playlist.add(loopback_url, loop_listitem)
        return main_listitem
    def extract_source(self, url, quality=None, **params):
        def ytdl_logger(record):
            if record.startswith("ERROR:"):
                stored_errors.append("Youtube-DL: " + record[7:])
            self.log(record)
            return True
        from YDStreamExtractor import getVideoInfo, setOutputCallback, overrideParam
        setOutputCallback(ytdl_logger)
        stored_errors = []
        for key, value in params.items():
            overrideParam(key, value)
        video_info = getVideoInfo(url, quality)
        if video_info:
            if video_info.hasMultipleStreams():
                video_info = self._source_selection(video_info)
            if video_info:
                if video_info.sourceName == "dailymotion":
                    self._extra_commands["setContentLookup"] = False
                return video_info.streamURL()
        elif stored_errors:
            raise RuntimeError(stored_errors[0])
    def _source_selection(self, video_info):
        display_list = [f'{stream["ytdl_format"]["extractor"].title()} - {stream["title"]}' for stream in video_info.streams()]
        dialog = xbmcgui.Dialog()
        ret = dialog.select(self.localize(localized.SELECT_PLAYBACK_ITEM), display_list)
        if ret >= 0:
            video_info.selectStream(ret)
            return video_info
    def _create_playlist(self, urls):
        listitems = [self._process_item(*item) for item in enumerate(urls, 1)]
        for item in listitems[1:]:
            self.playlist.add(item.getPath(), item)
        return listitems[0]
    def _process_item(self, count, url):
        if isinstance(url, xbmcgui.ListItem):
            return url
        elif isinstance(url, Listitem):
            return url.build()[1]
        else:
            listitem = xbmcgui.ListItem()
            if isinstance(url, (list, tuple)):
                title, url = url
                title = ensure_unicode(title)
            else:
                title = self._title
            listitem.setLabel(f"{title} Part {count}" if count > 1 else title)
            listitem.setInfo("video", {"title": title})
            listitem.setPath(url)
            return listitem
    def _process_generator(self, resolved):
        for item in enumerate(filter(None, resolved), 2):
            listitem = self._process_item(*item)
            self.playlist.add(listitem.getPath(), listitem)
    def _process_results(self, resolved):
        if resolved:
            if isinstance(resolved, (bytes, unicode_type)):
                listitem = xbmcgui.ListItem()
                listitem.setPath(resolved)
            elif isinstance(resolved, xbmcgui.ListItem):
                listitem = resolved
            elif isinstance(resolved, Listitem):
                listitem = resolved.build()[1]
            elif isinstance(resolved, (list, tuple)):
                listitem = self._create_playlist(resolved)
            elif inspect.isgenerator(resolved):
                listitem = self._process_item(1, next(resolved))
                self.register_delayed(self._process_generator, resolved)
            elif hasattr(resolved, "items"):
                items = resolved.items()
                listitem = self._create_playlist(items)
            else:
                raise ValueError(f"resolver returned invalid url of type: '{type(resolved)}'")
            logger.debug("Resolved Url: %s", listitem.getPath())
        elif resolved is False:
            listitem = xbmcgui.ListItem()
        else:
            raise RuntimeError(self.localize(localized.NO_VIDEO))
        if "setContentLookup" in self._extra_commands:
            value = self._extra_commands["setContentLookup"]
            listitem.setContentLookup(value)
        xbmcplugin.setResolvedUrl(self.handle, bool(resolved), listitem)
from codequick.listing import Listitem