from __future__ import absolute_import
import re
import xbmc
import urllib.parse as urlparse
unicode_type = type(u"")
string_map = {}
def keyboard(heading, default="", hidden=False):
    heading = ensure_native_str(heading)
    default = ensure_native_str(default)
    kb = xbmc.Keyboard(default, heading, hidden)
    kb.doModal()
    if kb.isConfirmed():
        text = kb.getText()
        return text.decode("utf8") if isinstance(text, bytes) else text
    else:
        return u""
def parse_qs(qs, keep_blank_values=False, strict_parsing=False):
    params = {}
    qs = ensure_native_str(qs)
    parsed = urlparse.parse_qsl(qs.split("?", 1)[-1], keep_blank_values, strict_parsing)
    for key, value in parsed:
        if key not in params:
            params[key] = value
        else:
            raise ValueError(f"encountered duplicate param field name: '{key}'")
    return params
def urljoin_partial(base_url):
    base_url = ensure_unicode(base_url)
    def wrapper(url):
        return urlparse.urljoin(base_url, ensure_unicode(url))
    return wrapper
def strip_tags(html):
    return re.sub("<[^<]+?>", "", html)
def ensure_native_str(data, encoding="utf8"):
    if isinstance(data, str):
        return data
    elif isinstance(data, unicode_type):
        return data.encode(encoding)
    elif isinstance(data, bytes):
        return data.decode(encoding)
    else:
        return str(data)
def ensure_unicode(data, encoding="utf8"):
    return data.decode(encoding) if isinstance(data, bytes) else unicode_type(data)
def bold(text):
    return f'[B]{text}[/B]'
def italic(text):
    return f'[I]{text}[/I]'
def color(text, color_code):
    return f'[COLOR {color_code}]{text}[/COLOR]'