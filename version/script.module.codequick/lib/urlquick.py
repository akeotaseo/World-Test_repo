__version__ = "2.0.1"
from functools import wraps
import warnings
import logging
import hashlib
import sqlite3
import os
import pickle
from htmlement import HTMLement
from requests.structures import CaseInsensitiveDict
from requests import adapters
from requests import *
import requests
import xbmc, xbmcvfs, xbmcaddon
_addon_data = xbmcaddon.Addon()
_translate_path = xbmcvfs.translatePath if hasattr(xbmcvfs, "translatePath") else xbmc.translatePath
_CACHE_LOCATION = _translate_path(_addon_data.getAddonInfo("profile"))
_DEFAULT_RAISE_FOR_STATUS = True
logger = logging.getLogger("urlquick")
logging.captureWarnings(True)
CACHEABLE_METHODS = {"GET", "HEAD", "POST"}
CACHEABLE_CODES = {
    codes.ok,
    codes.non_authoritative_info,
    codes.no_content,
    codes.multiple_choices,
    codes.moved_permanently,
    codes.found,
    codes.see_other,
    codes.temporary_redirect,
    codes.permanent_redirect,
    codes.gone,
    codes.request_uri_too_large,
}
REDIRECT_CODES = {
    codes.moved_permanently,
    codes.found,
    codes.see_other,
    codes.temporary_redirect,
    codes.permanent_redirect,
}
CACHE_LOCATION = _CACHE_LOCATION
MAX_AGE = 60 * 60 * 4
EXPIRES = 60 * 60 * 24 * 7
WRAPPER_ASSIGNMENTS = ["__doc__"]
class UrlError(RequestException):
    pass
class MaxRedirects(TooManyRedirects):
    pass
class ContentError(HTTPError):
    pass
class ConnError(ConnectionError):
    pass
class CacheError(RequestException):
    pass
class Response(requests.Response):
    def __init__(self):
        super(Response, self).__init__()
        self.from_cache = False
    def xml(self):
        from xml.etree import ElementTree
        return ElementTree.fromstring(self.content)
    def parse(self, tag=u"", attrs=None):
        tag = tag.decode() if isinstance(tag, bytes) else tag
        parser = HTMLement(tag, attrs)
        parser.feed(self.text)
        return parser.close()
    @classmethod
    def extend_response(cls, response):
        self = cls()
        self.__dict__.update(response.__dict__)
        return self
    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            data = pickle.dumps(self, protocol=pickle.HIGHEST_PROTOCOL)
            return sqlite3.Binary(data)
def to_bytes_string(value):
    return value.encode("utf8") if isinstance(value, type(u"")) else value
def hash_url(req):
    data = to_bytes_string(req.url + req.method)
    body = to_bytes_string(req.body) if req.body else b''
    return hashlib.sha1(b''.join((data, body))).hexdigest()
class CacheRecord(object):
    def __init__(self, record):
        self._response = response = pickle.loads(bytes(record["response"]))
        self._fresh = record["fresh"] or response.status_code in REDIRECT_CODES
        self._response.from_cache = True
    @property
    def response(self):
        return self._response
    @property
    def isfresh(self):
        return self._fresh
    def add_conditional_headers(self, headers):
        cached_headers = self._response.headers
        if "Etag" in cached_headers:
            headers["If-none-match"] = cached_headers["ETag"]
        if "Last-modified" in cached_headers:
            headers["If-modified-since"] = cached_headers["Last-Modified"]
class CacheHTTPAdapter(adapters.HTTPAdapter):
    def __init__(self, cache_location, *args, **kwargs):
        super(CacheHTTPAdapter, self).__init__(*args, **kwargs)
        self._closed = False
        self.cache_file = os.path.join(cache_location, ".urlquick.slite3")
        if not os.path.exists(cache_location):
            os.makedirs(cache_location)
        self.conn = self.connect()
        self.clean()
    def connect(self):
        try:
            conn = sqlite3.connect(self.cache_file, timeout=1)
        except sqlite3.Error as e:
            raise CacheError(str(e))
        else:
            conn.row_factory = sqlite3.Row
            conn.execute("""CREATE TABLE IF NOT EXISTS urlcache(
                key TEXT PRIMARY KEY NOT NULL,
                response BLOB NOT NULL,
                cached_date TIMESTAMP NOT NULL
            )""")
            conn.execute("PRAGMA journal_mode=MEMORY")
        return conn
    def execute(self, query, values=(), repeat=False):
        try:
            with self.conn:
                return self.conn.execute(query, values)
        except (sqlite3.IntegrityError, sqlite3.OperationalError) as e:
            if repeat is False and (str(e).find("file is encrypted") > -1 or str(e).find("not a database") > -1):
                logger.debug("Corrupted database detected, Cleaning...")
                self.conn.cursor().close()
                self.conn.close()
                os.remove(self.cache_file)
                self.conn = self.connect()
                return self.execute(query, values, repeat=True)
            else:
                raise e
    def close(self):
        super(CacheHTTPAdapter, self).close()
        if self._closed is False:
            self.conn.cursor().close()
            self.conn.close()
            self._closed = True
    def get_cache(self, urlhash, max_age):
        result = self.execute("""SELECT key, response,
        strftime('%s', 'now') - strftime('%s', cached_date, 'unixepoch') < ? AS fresh
        FROM urlcache WHERE key = ?""", (max_age, urlhash))
        record = result.fetchone()
        if record is not None:
            try:
                return CacheRecord(record)
            except ValueError as e:
                if "unsupported pickle protocol" in str(e):
                    self.wipe()
                else:
                    self.del_cache(urlhash)
    def set_cache(self, urlhash, resp):
        self.execute(
            "REPLACE INTO urlcache (key, response, cached_date) VALUES (?,?,strftime('%s', 'now'))",
            (urlhash, resp)
        )
        return resp
    def del_cache(self, urlhash):
        self.execute(
            "DELETE FROM urlcache WHERE key = ?",
            (urlhash,)
        )
    def reset_cache(self, urlhash):
        self.execute(
            "UPDATE urlcache SET cached_date=strftime('%s', 'now') WHERE key=?",
            (urlhash,)
        )
    def clean(self, expires=EXPIRES):
        self.execute(
            "DELETE FROM urlcache WHERE strftime('%s', 'now') - strftime('%s', cached_date, 'unixepoch') > ?",
            (expires,)
        )
    def wipe(self):
        self.execute("DELETE FROM urlcache")
    def send(self, request, **kwargs):
        max_age = int(request.headers.pop("x-cache-max-age"))
        urlhash = hash_url(request) if max_age >= 0 else None
        cache = None
        if urlhash and request.method in CACHEABLE_METHODS:
            cache = self.get_cache(urlhash, max_age)
            if cache and cache.isfresh:
                logger.debug("Cache is fresh")
                return cache.response
            elif cache:
                logger.debug("Cache is stale, adding conditional headers to request")
                cache.add_conditional_headers(request.headers)
        response = super(CacheHTTPAdapter, self).send(request, **kwargs)
        return self.process_response(response, cache, urlhash) if urlhash else response
    def build_response(self, req, resp):
        resp = super(CacheHTTPAdapter, self).build_response(req, resp)
        return Response.extend_response(resp)
    def process_response(self, response, cache, urlhash):
        if cache and response.status_code == codes.not_modified:
            logger.debug("Server return 304 Not Modified response, using cached response")
            response.close()
            self.reset_cache(urlhash)
            response = cache.response
        elif response.request.method in CACHEABLE_METHODS and response.status_code in CACHEABLE_CODES:
            logger.debug("Caching %s %s response", response.status_code, response.reason)
            response = self.set_cache(urlhash, response)
        return response
class Session(sessions.Session):
    def __init__(self, cache_location=CACHE_LOCATION, **kwargs):
        super(Session, self).__init__()
        self.raise_for_status = kwargs.get("raise_for_status", _DEFAULT_RAISE_FOR_STATUS)
        self.max_age = kwargs.get("max_age", MAX_AGE)
        self.cache_adapter = adapter = CacheHTTPAdapter(cache_location)
        self.mount("https://", adapter)
        self.mount("http://", adapter)
    def _raise_for_status(self, response, raise_for_status):
        if self.raise_for_status if raise_for_status is None else raise_for_status:
            response.raise_for_status()
    def _merge_max_age(self, max_age):
        return (-1 if self.max_age is None else self.max_age) if max_age is None else max_age
    def request(self, *args, **kwargs):
        if len(args) >= 5:
            headers = args[4] or {}
            args = list(args)
            args[4] = headers
        else:
            headers = kwargs.get("headers") or {}
            kwargs["headers"] = headers
        max_age = self._merge_max_age(kwargs.pop("max_age", None))
        headers["x-cache-max-age"] = str(max_age)
        headers["x-cache-internal"] = "true"
        raise_for_status = kwargs.pop("raise_for_status", None)
        response = super(Session, self).request(*args, **kwargs)
        self._raise_for_status(response, raise_for_status)
        return response
    def send(self, request, **kwargs):
        if request.headers.pop("x-cache-internal", None):
            return super(Session, self).send(request, **kwargs)
        else:
            max_age = self._merge_max_age(kwargs.pop("max_age", None))
            request.headers["x-cache-max-age"] = str(max_age)
            raise_for_status = kwargs.pop("raise_for_status", None)
            response = super(Session, self).send(request, **kwargs)
            self._raise_for_status(response, raise_for_status)
            return response
    def get(self, url, **kwargs):
        return super(Session, self).get(url, **kwargs)
    def options(self, url, **kwargs):
        return super(Session, self).options(url, **kwargs)
    def head(self, url, **kwargs):
        return super(Session, self).head(url, **kwargs)
    def post(self, url, data=None, json=None, **kwargs):
        return super(Session, self).post(url, data, json, **kwargs)
    def put(self, url, data=None, **kwargs):
        return super(Session, self).put(url, data, **kwargs)
    def patch(self, url, data=None, **kwargs):
        return super(Session, self).patch(url, data, **kwargs)
    def delete(self, url, **kwargs):
        return super(Session, self).delete(url, **kwargs)
@wraps(requests.request, assigned=WRAPPER_ASSIGNMENTS)
def request(method, url, **kwargs):
    with Session() as s:
        return s.request(method=method, url=url, **kwargs)
@wraps(requests.get, assigned=WRAPPER_ASSIGNMENTS)
def get(url, params=None, **kwargs):
    kwargs.setdefault('allow_redirects', True)
    return request('get', url, params=params, **kwargs)
@wraps(requests.options, assigned=WRAPPER_ASSIGNMENTS)
def options(url, **kwargs):
    kwargs.setdefault('allow_redirects', True)
    return request('options', url, **kwargs)
@wraps(requests.head, assigned=WRAPPER_ASSIGNMENTS)
def head(url, **kwargs):
    kwargs.setdefault('allow_redirects', False)
    return request('head', url, **kwargs)
@wraps(requests.post, assigned=WRAPPER_ASSIGNMENTS)
def post(url, data=None, json=None, **kwargs):
    return request('post', url, data=data, json=json, **kwargs)
@wraps(requests.put, assigned=WRAPPER_ASSIGNMENTS)
def put(url, data=None, **kwargs):
    return request('put', url, data=data, **kwargs)
@wraps(requests.patch, assigned=WRAPPER_ASSIGNMENTS)
def patch(url, data=None, **kwargs):
    return request('patch', url, data=data, **kwargs)
@wraps(requests.delete, assigned=WRAPPER_ASSIGNMENTS)
def delete(url, **kwargs):
    return request('delete', url, **kwargs)
@wraps(requests.session, assigned=WRAPPER_ASSIGNMENTS)
def session():
    return Session()
def cache_cleanup(max_age=None):
    warnings.warn("No longer Needed", DeprecationWarning)
def auto_cache_cleanup(max_age=None):
    warnings.warn("No longer Needed", DeprecationWarning)
    return True