from __future__ import absolute_import
from time import strptime, strftime
import logging, os, _strptime, xbmcplugin, xbmcgui
from codequick.route import Route
from codequick.script import Script
from codequick.support import auto_sort, build_path, logger_id, dispatcher, CallbackRef
from codequick.utils import ensure_unicode, ensure_native_str, unicode_type, bold
from codequick import localized
from collections.abc import MutableMapping, MutableSequence
from infotagger.listitem import ListItemInfoTag
__all__ = ["Listitem"]
logger = logging.getLogger(f"{logger_id}.listitem")
local_image = ensure_native_str(os.path.join(Script.get_info("path"), u"resources", u"media", u"{}"))
global_image = ensure_native_str(os.path.join(Script.get_info("path_global"), u"resources", u"media", u"{}"))
_fanart = Script.get_info("fanart")
fanart = ensure_native_str(_fanart) if os.path.exists(_fanart) else None
icon = ensure_native_str(Script.get_info("icon"))
stream_type_map = {"duration": int,
                   "channels": int,
                   "aspect": float,
                   "height": int,
                   "width": int}
infolable_map = {"artist": (None, xbmcplugin.SORT_METHOD_ARTIST_IGNORE_THE),
                 "studio": (ensure_native_str, xbmcplugin.SORT_METHOD_STUDIO_IGNORE_THE),
                 "title": (ensure_native_str, xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE),
                 "album": (ensure_native_str, xbmcplugin.SORT_METHOD_ALBUM_IGNORE_THE),
                 "code": (ensure_native_str, xbmcplugin.SORT_METHOD_PRODUCTIONCODE),
                 "count": (int, xbmcplugin.SORT_METHOD_PROGRAM_COUNT),
                 "rating": (float, xbmcplugin.SORT_METHOD_VIDEO_RATING),
                 "mpaa": (ensure_native_str, xbmcplugin.SORT_METHOD_MPAA_RATING),
                 "year": (int, xbmcplugin.SORT_METHOD_VIDEO_YEAR),
                 "listeners": (int, xbmcplugin.SORT_METHOD_LISTENERS),
                 "tracknumber": (int, xbmcplugin.SORT_METHOD_TRACKNUM),
                 "episode": (int, xbmcplugin.SORT_METHOD_EPISODE),
                 "country": (ensure_native_str, xbmcplugin.SORT_METHOD_COUNTRY),
                 "genre": (None, xbmcplugin.SORT_METHOD_GENRE),
                 "date": (ensure_native_str, xbmcplugin.SORT_METHOD_DATE),
                 "size": (int, xbmcplugin.SORT_METHOD_SIZE),
                 "sortepisode": (int, None),
                 "sortseason": (int, None),
                 "userrating": (int, None),
                 "discnumber": (int, None),
                 "playcount": (int, None),
                 "overlay": (int, None),
                 "season": (int, None),
                 "top250": (int, None),
                 "setid": (int, None),
                 "dbid": (int, None)}
auto_sort_add = auto_sort.add
quality_map = ((768, 576), (1280, 720), (1920, 1080), (3840, 2160))
class Params(MutableMapping):
    def __setstate__(self, state):
        self.__dict__.update(state)
    def __init__(self):
        self.__dict__["raw_dict"] = {}
    def __setattr__(self, name, value):
        self[name] = value
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    def __setitem__(self, key, value):
        if isinstance(value, bytes):
            self.raw_dict[key] = value.decode("utf8")
        else:
            self.raw_dict[key] = value
    def __getitem__(self, key):
        value = self.raw_dict[key]
        return value.decode("utf8") if isinstance(value, bytes) else value
    def __delitem__(self, key):
        del self.raw_dict[key]
    def __delattr__(self, name):
        try:
            del self.raw_dict[name]
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    def __len__(self):
        return len(self.raw_dict)
    def __iter__(self):
        return iter(self.raw_dict)
    def __str__(self):
        return str(self.raw_dict)
    def __repr__(self):
        return f"{self.__class__}({self.raw_dict})"
    def clean(self):
        for key, val in list(self.raw_dict.items()):
            if not val:
                del self.raw_dict[key]
class Art(Params):
    def __setitem__(self, key, value):
        self.raw_dict[key] = ensure_native_str(value)
    def local_thumb(self, image):
        self.raw_dict["thumb"] = local_image.format(ensure_native_str(image))
    def global_thumb(self, image):
        self.raw_dict["thumb"] = global_image.format(image)
    def _close(self, listitem, isfolder):
        if fanart and "fanart" not in self.raw_dict:
            self.raw_dict["fanart"] = fanart
        if "thumb" not in self.raw_dict:
            self.raw_dict["thumb"] = icon
        if "icon" not in self.raw_dict:
            self.raw_dict["icon"] = "DefaultFolder.png" if isfolder else "DefaultVideo.png"
        self.clean()
        listitem.setArt(self.raw_dict)
class Info(Params):
    def __setitem__(self, key, value):
        if value is None or value == "":
            logger.debug("Ignoring empty infolable: '%s'", key)
            return None
        elif key == "duration":
            auto_sort_add(xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
            self.raw_dict[key] = self._duration(value)
        else:
            type_converter, sort_type = infolable_map.get(key, (None, None))
            if type_converter:
                try:
                    value = type_converter(value)
                except ValueError:
                    msg = f"value of '{value}' for infolabel '{key}', is not of type '{type_converter}'"
                    raise TypeError(msg)
                else:
                    self.raw_dict[key] = value
            elif isinstance(value, str):
                self.raw_dict[key] = value
            elif isinstance(value, bytes):
                self.raw_dict[key] = value.decode("utf8")
            else:
                self.raw_dict[key] = value
            if sort_type:
                auto_sort_add(sort_type)
    def date(self, date, date_format):
        converted_date = strptime(ensure_native_str(date), date_format)
        self.raw_dict["date"] = strftime("%d.%m.%Y", converted_date)
        self.raw_dict["aired"] = strftime("%Y-%m-%d", converted_date)
        self.raw_dict["year"] = strftime("%Y", converted_date)
        auto_sort_add(xbmcplugin.SORT_METHOD_VIDEO_YEAR)
        auto_sort_add(xbmcplugin.SORT_METHOD_DATE)
    @staticmethod
    def _duration(duration):
        if isinstance(duration, (str, unicode_type)):
            duration = duration.replace(";", ":").strip(":")
            if ":" in duration:
                time_parts = duration.split(":")
                time_parts.reverse()
                duration = 0
                counter = 1
                for part in time_parts:
                    duration += int(part) * counter
                    counter *= 60
            else:
                duration = int(duration)
        return duration
    def _close(self, listitem, content_type):
        raw_dict = self.raw_dict
        if "plot" not in raw_dict:
            raw_dict["plot"] = raw_dict["title"]
        if ('size', 'count', 'date', ):
            listitem.setInfo(content_type, {k: raw_dict[k] for k in ('size', 'count', 'date', ) if k in raw_dict})
        ListItemInfoTag(listitem, content_type).set_info(raw_dict)
class Property(Params):
    def __setitem__(self, key, value):
        if value:
            self.raw_dict[key] = ensure_unicode(value)
        else:
            logger.debug("Ignoring empty property: '%s'", key)
    def _close(self, listitem):
        for key, value in self.raw_dict.items():
            listitem.setProperty(key, value)
class Stream(Params):
    def __setitem__(self, key, value):
        if not value:
            logger.debug("Ignoring empty stream detail value for: '%s'", key)
            return None
        type_converter = stream_type_map.get(key, ensure_native_str)
        try:
            value = type_converter(value)
        except ValueError:
            msg = f"Value of '{value}' for stream info '{key}', is not of type '{type_converter}'"
            raise TypeError(msg)
        else:
            self.raw_dict[key] = value
    def hd(self, quality, aspect=None):
        if quality is None:
            return None
        try:
            self.raw_dict["width"], self.raw_dict["height"] = quality_map[quality]
        except IndexError:
            raise ValueError(f"quality id must be within range (0 to 3): '{quality}'")
        if aspect:
            self["aspect"] = aspect
        elif self.raw_dict["height"] >= 720:
            self.raw_dict["aspect"] = 1.78
    def _close(self, listitem):
        video = {}
        subtitle = {}
        audio = {"channels": 2}
        for key, value in self.raw_dict.items():
            rkey = key.split("_")[-1]
            if key in {"video_codec", "aspect", "width", "height", "duration"}:
                video[rkey] = value
            elif key in {"audio_codec", "audio_language", "channels"}:
                audio[rkey] = value
            elif key == "subtitle_language":
                subtitle[rkey] = value
            else:
                raise KeyError(f"unknown stream detail key: '{key}'")
        ListItemInfoTag(listitem, 'video').set_stream_details(audio)
        if video:
            ListItemInfoTag(listitem, 'video').set_stream_details(video)
        if subtitle:
            ListItemInfoTag(listitem, 'video').set_stream_details(subtitle)
class Context(list):
    def related(self, callback, *args, **kwargs):
        path = callback.path if isinstance(callback, CallbackRef) else callback.route.path
        if path == dispatcher.get_route().path:
            kwargs["_updatelisting_"] = True
        related_videos_text = Script.localize(localized.RELATED_VIDEOS)
        kwargs["_title_"] = related_videos_text
        self.container(callback, related_videos_text, *args, **kwargs)
    def container(self, callback, label, *args, **kwargs):
        command = f"Container.Update({build_path(callback, args, kwargs)})"
        self.append((label, command))
    def script(self, callback, label, *args, **kwargs):
        command = f"RunPlugin({build_path(callback, args, kwargs)})"
        self.append((label, command))
    def _close(self, listitem):
        if self:
            listitem.addContextMenuItems(self)
class Listitem(object):
    def __getstate__(self):
        state = self.__dict__.copy()
        state["label"] = self.label
        del state["listitem"]
        return state
    def __setstate__(self, state):
        label = state.pop("label")
        self.__dict__.update(state)
        self.listitem = xbmcgui.ListItem(self.label, offscreen=True)
        self.label = label
    def __init__(self, content_type="video"):
        self._content_type = content_type
        self._is_playable = False
        self._is_folder = False
        self._args = None
        self._path = ""
        self.listitem = xbmcgui.ListItem()
        self.subtitles = []
        self.info = Info()
        self.art = Art()
        self.stream = Stream()
        self.context = Context()
        self.params = Params()
        self.property = Property()
    @property
    def label(self):
        label = self.listitem.getLabel()
        return label.decode("utf8") if isinstance(label, bytes) else label
    @label.setter
    def label(self, label):
        self.listitem.setLabel(label)
        self.params["_title_"] = label
        self.info["title"] = label
    @property
    def path(self):
        return self._path
    @path.setter
    def path(self, value):
        self._path = value
        self._is_playable = True
    def set_path(self, path, is_folder=False, is_playable=True):
        self._path = path
        self._is_folder = is_folder
        self._is_playable = False if path.startswith("script://") else is_playable
    def set_callback(self, callback, *args, **kwargs):
        if hasattr(callback, "route"):
            callback = callback.route
        elif not isinstance(callback, CallbackRef):
            if "://" not in callback:
                msg = "passing callback path to 'set_callback' is deprecated, " \
                      "use callback reference 'Route.ref' instead"
                logger.warning("DeprecationWarning: " + msg)
                callback = dispatcher.get_route(callback)
            else:
                msg = "passing a playable / plugin path to 'set_callback' is deprecated, use 'set_path' instead"
                logger.warning("DeprecationWarning: " + msg)
                is_folder = kwargs.pop("is_folder", False)
                is_playable = kwargs.pop("is_playable", not is_folder)
                self.set_path(callback, is_folder, is_playable)
                return
        self.params.update(kwargs)
        self._is_playable = callback.is_playable
        self._is_folder = callback.is_folder
        self._path = callback
        self._args = args
    def build(self):
        listitem = self.listitem
        isfolder = self._is_folder
        listitem.setProperty("folder", str(isfolder).lower())
        listitem.setProperty("isplayable", str(self._is_playable).lower())
        if isinstance(self._path, CallbackRef):
            path = build_path(self._path, self._args, self.params.raw_dict)
        else:
            path = self._path
        if not isfolder:
            if "mediatype" not in self.info.raw_dict and self._content_type in ("video", "music"):
                self.info.raw_dict["mediatype"] = self._content_type
            if self.subtitles:
                self.listitem.setSubtitles(self.subtitles)
            self.context.append(("$LOCALIZE[13347]", "Action(Queue)"))
            self.context.append(("$LOCALIZE[13350]", "ActivateWindow(videoplaylist)"))
            self.stream._close(listitem)
        if not self.label:
            self.label = u"UNKNOWN"
        listitem.setPath(path)
        self.property._close(listitem)
        self.context._close(listitem)
        self.info._close(listitem, self._content_type)
        self.art._close(listitem, isfolder)
        return path, listitem, isfolder
    @classmethod
    def from_dict(
            cls,
            callback,
            label,
            art=None,
            info=None,
            stream=None,
            context=None,
            properties=None,
            params=None,
            subtitles=None
    ):
        item = cls()
        item.label = label
        if isinstance(callback, str) and "://" in callback:
            item.set_path(callback)
        else:
            item.set_callback(callback)
        if params:
            item.params.update(params)
        if info:
            item.info.update(info)
        if art:
            item.art.update(art)
        if stream:
            item.stream.update(stream)
        if properties:
            item.property.update(properties)
        if context:
            item.context.extend(context)
        if subtitles:
            item.subtitles.extend(subtitles)
        return item
    @classmethod
    def next_page(cls, *args, **kwargs):
        callback = kwargs.pop("callback") if "callback" in kwargs else dispatcher.get_route().callback
        kwargs["_updatelisting_"] = True if u"_nextpagecount_" in dispatcher.params else False
        kwargs["_title_"] = dispatcher.params.get(u"_title_", u"")
        kwargs["_nextpagecount_"] = dispatcher.params.get(u"_nextpagecount_", 1) + 1
        item = cls()
        label = f'{Script.localize(localized.NEXT_PAGE)} {kwargs["_nextpagecount_"]}'
        item.info["plot"] = Script.localize(localized.NEXT_PAGE_PLOT)
        item.label = bold(label)
        item.art.global_thumb("next.png")
        item.set_callback(callback, *args, **kwargs)
        return item
    @classmethod
    def recent(cls, callback, *args, **kwargs):
        item = cls()
        item.label = bold(Script.localize(localized.RECENT_VIDEOS))
        item.info["plot"] = Script.localize(localized.RECENT_VIDEOS_PLOT)
        item.art.global_thumb("recent.png")
        item.set_callback(callback, *args, **kwargs)
        return item
    @classmethod
    def search(cls, callback, *args, **kwargs):
        if hasattr(callback, "route"):
            route = callback.route
        elif isinstance(callback, CallbackRef):
            route = callback
        else:
            route = dispatcher.get_route(callback)
        kwargs["first_load"] = True
        kwargs["_route"] = route.path
        item = cls()
        item.label = 'TÌM KIẾM'
        item.art.global_thumb("search.png")
        item.set_callback(Route.ref("/codequick/search:saved_searches"), *args, **kwargs)
        return item
    @classmethod
    def youtube(cls, content_id, label=None, enable_playlists=True):
        item = cls()
        item.label = label if label else bold(Script.localize(localized.ALLVIDEOS))
        item.art.global_thumb("videos.png")
        item.params["contentid"] = content_id
        item.params["enable_playlists"] = False if content_id.startswith("PL") else enable_playlists
        item.set_callback(Route.ref("/codequick/youtube:playlist"))
        return item
    def __repr__(self):
        return f"{self.__class__.__name__}('{ensure_native_str(self.label)}')"