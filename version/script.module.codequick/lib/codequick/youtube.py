from __future__ import absolute_import
import logging
import sqlite3
import json
import os
from codequick.route import Route
from codequick.utils import bold
from codequick.listing import Listitem
from codequick.resolver import Resolver
from codequick.support import logger_id
from codequick import localized
import urlquick
logger = logging.getLogger(f"{logger_id}.youtube")
CACHEFILE = os.path.join(Route.get_info("profile"), u"_youtube-cache.sqlite")
EXCEPTED_STATUS = [u"public", u"unlisted"]
class Database(object):
    def __init__(self):
        self.db = db = sqlite3.connect(CACHEFILE, timeout=1)
        db.isolation_level = None
        db.row_factory = sqlite3.Row
        self.cur = cur = db.cursor()
        cur.execute('PRAGMA locking_mode=EXCLUSIVE')
        cur.execute('PRAGMA journal_mode=MEMORY')
        cur.execute("""CREATE TABLE IF NOT EXISTS channels
                    (channel_id TEXT PRIMARY KEY, uploads_id TEXT, fanart TEXT, channel_title TEXT)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS categories
                    (id INT PRIMARY KEY, genre TEXT)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS videos
                    (video_id TEXT PRIMARY KEY, title TEXT, thumb TEXT, description TEXT, genre_id INT,
                    count INT, date TEXT, hd INT, duration INT, channel_id TEXT,
                    FOREIGN KEY(channel_id) REFERENCES channels(channel_id),
                    FOREIGN KEY(genre_id) REFERENCES categories(id))""")
    def execute(self, execute_obj, sqlquery, args=""):
        self.cur.execute("BEGIN")
        try:
            execute_obj(sqlquery, args)
        except Exception as e:
            self.db.rollback()
            raise e
        else:
            self.db.commit()
    def update_channels(self, channels):
        sqlquery = "INSERT INTO channels VALUES(:channel_id, :uploads_id, :fanart, :channel_title)"
        self.execute(self.cur.executemany, sqlquery, channels)
    def update_categories(self, categories):
        sqlquery = "INSERT INTO categories VALUES(?, ?)"
        self.execute(self.cur.executemany, sqlquery, categories)
    def update_videos(self, videos):
        sqlquery = """INSERT INTO videos VALUES(:video_id, :title, :thumb, :description,
                      :genre_id, :count, :date, :hd, :duration, :channel_id)"""
        self.execute(self.cur.executemany, sqlquery, videos)
    def extract_videos(self, data):
        results = self.cur.execute("""
        SELECT video_id, title, thumb, description, genre, count, date, hd, duration, videos.channel_id,
        fanart, channel_title FROM videos INNER JOIN channels ON channels.channel_id = videos.channel_id
        INNER JOIN categories ON categories.id = videos.genre_id
        WHERE video_id IN (%s)""" % ",".join("?" * len(data)), data)
        return {row[0]: row for row in results}
    @property
    def channels(self):
        return {data[0]: data[1] for data in self.cur.execute("SELECT channel_id, uploads_id FROM channels")}
    @property
    def categories(self):
        return frozenset(data[0] for data in self.cur.execute("SELECT id FROM categories"))
    def close(self):
        try:
            self.cur.close()
            self.db.close()
        except:
            pass
    def cleanup(self):
        if self.cur.execute("SELECT COUNT(*) FROM videos").fetchone()[0] > 10000:
            logger.debug("Running Youtube Cache Cleanup")
            sqlquery = """DELETE FROM videos WHERE video_id IN (select video_id from videos
                          ORDER BY date DESC LIMIT -1 OFFSET 2500)"""
            self.execute(self.cur.execute, sqlquery)
            sqlquery = """DELETE FROM channels WHERE channel_id in (SELECT channel_id from channels
                          WHERE channel_id not in (SELECT channel_id from videos))"""
            self.execute(self.cur.execute, sqlquery)
            self.cur.execute("VACUUM")
        self.close()
class API(object):
    def __init__(self, max_results=50, pretty_print=False):
        self.req_session = urlquick.Session()
        self.req_session.headers["referer"] = "http://www.codequick.com/"
        self.req_session.params = {"maxResults": str(max_results),
                                   "prettyPrint": str(pretty_print).lower(),
                                   "key": "AIzaSyD_guosGuZjoQLWIZdJzYzYEn3Oy8VOUgs"}
    def _request(self, url, query):
        source = self.req_session.get(url, params=query)
        response = json.loads(source.content)
        if u"error" not in response:
            return response
        else:
            try:
                message = response[u"error"][u"errors"][0][u"message"]
            except (KeyError, ValueError):
                raise RuntimeError("Youtube V3 API return an error response")
            else:
                raise RuntimeError(f"Youtube V3 API return an error response: {message}")
    def _connect_v3(self, api_type, query, loop=False):
        if "id" in query and hasattr(query["id"], '__iter__'):
            query["id"] = u",".join(query["id"])
        url = f"https://www.googleapis.com/youtube/v3/{api_type}"
        if "id" in query:
            ids = query["id"].split(",")
            counter = 0
            query["id"] = ",".join(ids[counter:counter + 50])
            feed = self._request(url, query)
            results = feed
            counter += 50
            while counter < len(ids):
                query["id"] = ",".join(ids[counter:counter + 50])
                feed = self._request(url, query)
                results[u"items"].extend(feed[u"items"])
                counter += 50
            return results
        elif loop:
            feed = self._request(url, query)
            results = feed
            while u"nextPageToken" in feed:
                query["pageToken"] = feed.pop(u"nextPageToken")
                feed = self._request(url, query)
                results[u"items"].extend(feed[u"items"])
            return results
        else:
            return self._request(url, query)
    def channels(self, channel_id):
        query = {"hl": "vi", "part": "contentDetails,brandingSettings,snippet", "id": channel_id,
                 "fields": "items(id,brandingSettings/image/bannerTvMediumImageUrl,"
                           "contentDetails/relatedPlaylists/uploads,snippet/localized/title)"}
        return self._connect_v3("channels", query)
    def video_categories(self, region_code="vn"):
        query = {"fields": "items(id,snippet/title)", "part": "snippet", "hl": "vi", "regionCode": region_code}
        return self._connect_v3("videoCategories", query)
    def playlist_items(self, playlist_id, pagetoken=None, loop=False):
        query = {"fields": "nextPageToken,items(snippet(channelId,resourceId/videoId),status/privacyStatus)",
                 "playlistId": playlist_id, "part": "snippet,status"}
        if pagetoken:
            query["pageToken"] = pagetoken
        return self._connect_v3("playlistItems", query, loop)
    def videos(self, video_id):
        query = {"part": "contentDetails,statistics,snippet", "hl": "vi", "id": video_id,
                 "fields": "items(id,snippet(publishedAt,channelId,thumbnails/medium/url,"
                           "categoryId,localized),contentDetails(duration,definition),statistics/viewCount)"}
        return self._connect_v3("videos", query)
    def playlists(self, channel_id, pagetoken=None, loop=False):
        query = {"part": "snippet,contentDetails", "channelId": channel_id,
                 "fields": "nextPageToken,items(id,contentDetails/itemCount,snippet"
                           "(publishedAt,localized,thumbnails/medium/url))"}
        if pagetoken:
            query["pageToken"] = pagetoken
        return self._connect_v3("playlists", query, loop)
    def search(self, **search_params):
        query = {"relevanceLanguage": "vi", "safeSearch": "none", "part": "snippet", "type": "video",
                 "fields": "nextPageToken,items(id/videoId,snippet/channelId)"}
        query.update(search_params)
        return self._connect_v3("search", query)
    def close(self):
        self.req_session.close()
class APIControl(Route):
    def __init__(self):
        super(APIControl, self).__init__()
        self.db = Database()
        self.register_delayed(self.db.cleanup)
        self.api = API()
    def valid_playlistid(self, contentid):
        if contentid.startswith("UC"):
            channel_cache = self.db.channels
            if contentid in channel_cache:
                return channel_cache[contentid]
            else:
                self.update_channel_cache([contentid])
                if contentid in self.db.channels:
                    return self.db.channels[contentid]
                else:
                    raise KeyError("Unable to find Youtube channel: {}".format(contentid))
        elif contentid[:2] in ("PL", "FL", "UU"):
            return contentid
        else:
            raise ValueError(f"contentid is not of valid type (PL,UU,UC): {contentid}")
    def update_category_cache(self):
        feed = self.api.video_categories()
        category_cache = self.db.categories
        self.db.update_categories((int(item[u"id"]), item[u"snippet"][u"title"])
                                  for item in feed[u"items"] if int(item[u"id"]) not in category_cache)
    def update_channel_cache(self, ids):
        feed = self.api.channels(ids)
        processed_channels = []
        for item in feed[u"items"]:
            data = {"channel_id": item[u"id"],
                    "channel_title": item[u"snippet"][u"localized"][u"title"],
                    "uploads_id": item[u"contentDetails"][u"relatedPlaylists"][u"uploads"]}
            try:
                data["fanart"] = item[u"brandingSettings"][u"image"][u"bannerTvMediumImageUrl"]
            except KeyError:
                data["fanart"] = None
            processed_channels.append(data)
        self.db.update_channels(processed_channels)
    def request_videos(self, ids):
        cached_videos = self.db.extract_videos(ids)
        uncached_ids = list(frozenset(key for key in ids if key not in cached_videos))
        if uncached_ids:
            feed = self.api.videos(uncached_ids)
            duration_search = __import__("re").compile(r"(\d+)(\w)")
            category_cache = self.db.categories
            channel_cache = self.db.channels
            update_categories = False
            required_channels = []
            processed_videos = []
            for video in feed[u"items"]:
                snippet = video[u"snippet"]
                content_details = video[u"contentDetails"]
                data = {
                    "title": snippet[u"localized"][u"title"],
                    "thumb": snippet[u"thumbnails"][u"medium"][u"url"],
                    "description": snippet[u"localized"][u"description"],
                    "date": snippet[u"publishedAt"],
                    "count": int(video["statistics"]["viewCount"]) if "statistics" in video else 0,
                    "channel_id": snippet[u"channelId"],
                    "video_id": video[u"id"],
                    "hd": int(content_details[u"definition"] == u"hd"),
                    "duration": "",
                    "genre_id": int(snippet[u"categoryId"])
                }
                duration_str = content_details[u"duration"]
                duration_match = duration_search.findall(duration_str)
                if duration_match:
                    data["duration"] = self._convert_duration(duration_match)
                processed_videos.append(data)
                if data["channel_id"] not in required_channels and data["channel_id"] not in channel_cache:
                    required_channels.append(data["channel_id"])
                if update_categories is False and data["genre_id"] not in category_cache:
                    update_categories = True
            if required_channels:
                self.update_channel_cache(required_channels)
            if update_categories:
                self.update_category_cache()
            self.db.update_videos(processed_videos)
            cached = self.db.extract_videos(uncached_ids)
            cached_videos.update(cached)
        return (cached_videos[video_id] for video_id in ids if video_id in cached_videos)
    def videos(self, video_ids, multi_channel=False):
        try:
            ishd = self.setting.get_int("video_quality", addon_id="script.module.youtube.dl")
        except RuntimeError:
            ishd = True
        for video_data in self.request_videos(video_ids):
            item = Listitem()
            item.label = video_data["title"]
            item.art["fanart"] = video_data["fanart"]
            item.art["thumb"] = video_data["thumb"]
            item.info["plot"] = f'[B]{video_data["channel_title"]}[/B]\n\n{video_data["description"]}'
            item.info["studio"] = [video_data["channel_title"]]
            if video_data["count"]:
                item.info["count"] = video_data["count"]
            date = video_data["date"]
            item.info.date(date[:date.find(u"T")], "%Y-%m-%d")
            #item.info["genre"] = video_data["genre"]
            item.info["genre"] = [video_data["genre"]]
            item.stream.hd(bool(ishd and video_data["hd"]))
            item.info["duration"] = video_data["duration"]
            item.context.related(related, video_id=video_data["video_id"])
            if multi_channel:
                item.context.container(playlist, f'Go to: {video_data["channel_title"]}',
                                       contentid=video_data["channel_id"])
            item.set_callback(play_video, video_id=video_data["video_id"])
            yield item
    @staticmethod
    def _convert_duration(duration_match):
        duration = 0
        for time_segment, timeType in duration_match:
            if timeType == u"H":
                duration += (int(time_segment) * 3600)
            elif timeType == u"M":
                duration += (int(time_segment) * 60)
            elif timeType == u"S":
                duration += (int(time_segment))
        return duration
    def close(self):
        self.api.close()
        self.db.close()
@Route.register
def playlists(plugin, channel_id, show_all=True, pagetoken=None, loop=False):
    gdata = APIControl()
    if not channel_id.startswith("UC"):
        raise ValueError(f"channel_id is not valid: {channel_id}")
    fanart = gdata.db.cur.execute("SELECT fanart FROM channels WHERE channel_id = ?", (channel_id,)).fetchone()
    if fanart:
        fanart = fanart[0]
    feed = gdata.api.playlists(channel_id, pagetoken, loop)
    if u"nextPageToken" in feed:
        yield Listitem.next_page(channel_id=channel_id, show_all=False, pagetoken=feed[u"nextPageToken"])
    if show_all:
        title = bold(plugin.localize(localized.ALLVIDEOS))
        yield Listitem.youtube(channel_id, title, enable_playlists=False)
    for playlist_item in feed[u"items"]:
        item = Listitem()
        item_count = playlist_item[u"contentDetails"][u"itemCount"]
        if item_count == 0:
            continue
        snippet = playlist_item[u"snippet"]
        item.label = f'{snippet[u"localized"][u"title"]} ({item_count})'
        item.art["thumb"] = snippet[u"thumbnails"][u"medium"][u"url"]
        item.art["fanart"] = fanart
        item.info["plot"] = snippet[u"localized"][u"description"]
        item.set_callback(playlist, contentid=playlist_item[u"id"], enable_playlists=False)
        yield item
    gdata.close()
@Route.register
def playlist(plugin, contentid, pagetoken=None, enable_playlists=True, loop=False):
    gdata = APIControl()
    playlist_id = gdata.valid_playlistid(contentid)
    feed = gdata.api.playlist_items(playlist_id, pagetoken, loop)
    channel_list = set()
    video_list = []
    for item in feed[u"items"]:
        if u"status" in item and item[u"status"][u"privacyStatus"] in EXCEPTED_STATUS:
            channel_list.add(item[u"snippet"][u"channelId"])
            video_list.append(item[u"snippet"][u"resourceId"][u"videoId"])
        else:
            logger.debug("Skipping non plublic video: '%s'", item[u"snippet"][u"resourceId"][u"videoId"])
    results = list(gdata.videos(video_list, multi_channel=len(channel_list) > 1))
    if u"nextPageToken" in feed:
        next_item = Listitem.next_page(contentid=contentid, pagetoken=feed[u"nextPageToken"])
        results.append(next_item)
    if enable_playlists and contentid.startswith("UC") and pagetoken is None:
        item = Listitem()
        item.label = f"[B]{plugin.localize(localized.PLAYLISTS)}[/B]"
        item.info["plot"] = plugin.localize(localized.PLAYLISTS_PLOT)
        item.art["icon"] = "DefaultVideoPlaylists.png"
        item.art.global_thumb("playlist.png")
        item.set_callback(playlists, channel_id=contentid, show_all=False)
        results.append(item)
    gdata.close()
    return results
@Route.register
def related(plugin, video_id, pagetoken=None):
    gdata = APIControl()
    plugin.category = "Related"
    plugin.update_listing = bool(pagetoken)
    feed = gdata.api.search(pageToken=pagetoken, relatedToVideoId=video_id)
    video_list = [item[u"id"][u"videoId"] for item in feed[u"items"]]
    results = list(gdata.videos(video_list, multi_channel=True))
    if u"nextPageToken" in feed:
        next_item = Listitem.next_page(video_id=video_id, pagetoken=feed[u"nextPageToken"])
        results.append(next_item)
    gdata.close()
    return results
@Resolver.register
def play_video(plugin, video_id):
    return f"plugin://plugin.video.youtube/play/?video_id={video_id}"