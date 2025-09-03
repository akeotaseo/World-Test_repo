from codequick import Resolver,Listitem,Script
from urllib.parse import urlparse,quote,unquote,quote_plus,urlencode
from requests import Session
from bs4 import BeautifulSoup
from collections import OrderedDict
from urlquick import get,post,cache_cleanup
from xbmc import executebuiltin
from xbmcvfs import translatePath
from cloudscraper import create_scraper
from os import remove,makedirs
from os.path import join,exists,getmtime
from base64 import b64encode
from json import loads,dumps
from random import randint
from time import time, localtime
from shutil import rmtree
from resolveurl import resolve
from codequick.utils import italic
from datetime import datetime, timedelta
import re,sys
__addonname__ = Script.get_info('name')
__version__ = Script.get_info('version')
__icon__ = Script.get_info('icon')
__addonnoti__ = f'{__addonname__} v{__version__}'
chrome = 123
rannum = randint(chrome, 199)
veruser = f'{chrome}{rannum}'
verpix = f'{veruser}.{rannum}'
verchr = f'{chrome}.{chrome}.{verpix}'
addon_data_dir = join(translatePath('special://userdata/addon_data'),'plugin.video.vnmedia')
userpix = f'(Linux; Android 14; Pixel 8 Pro Build/AP1A.{verpix})'
userios = f'AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/{verchr}'
useragentdf = f'Mozilla/5.0 {userpix} {userios} Mobile Safari/605.1.15 EdgA/{verchr}'
useragentweb = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) {userios} Safari/605.1.15 Edg/{verchr}'
useragentott = f'OTT Navigator/1.7.1.4 {userpix} ExoPlayerLib/2.19.1'
userfs = 'FshareiOSApp-saCP7ssw2u7w'
keyfs = 'MkywVt2UBRHcJXUUcfsZ7XXzBSJV3dwE'
news ='https://mi3s.top/thumb/qc.ass'
qc = 'https://mi3s.top/thumb/nolink.mp4'
headersnct = {'x-nct-token': 'eyJhbGciOiJIUzI1NiJ9.eyJsb2dpbk1ldGhvZCI6IjUiLCJleHAiOjE2ODMyMDYyNzEsImV4cGlyZWREYXRlIjoiMCIsIm5iZiI6MTY4MDYxNDI3MSwiZGV2aWNlaW5mbyI6IntcIkRldmljZUlEXCI6XCIzQjBGNDUyNUJDOEQ0NUI0QUQxNjZDNzdBMDQ1NjlFNlwiLFwiT3NOYW1lXCI6XCJBTkRST0lEXCIsXCJPc1ZlcnNpb25cIjpcIjIyXCIsXCJBcHBOYW1lXCI6XCJOQ1RNb2JpbGVcIixcIkFwcFZlcnNpb25cIjpcIjguMS4yXCIsXCJVc2VyTmFtZVwiOlwiXCIsXCJQcm92aWRlclwiOlwiTkNUQ29ycFwiLFwiRGV2aWNlTmFtZVwiOlwiQVNVU19aMDFRRFwiLFwiUXVhbGl0eVBsYXlcIjpcIlwiLFwiUXVhbGl0eURvd25sb2FkXCI6XCJcIixcIlF1YWxpdHlDbG91ZFwiOlwiXCIsXCJOZXR3b3JrXCI6XCJXSUZJXCIsXCJRdWFsaXR5TVZQbGF5XCI6XCJcIixcIlF1YWxpdHlNVkRvd25sb2FkXCI6XCJcIixcIkFkSURcIjpcIlwiLFwiRGV2aWNlVHlwZVwiOlwiU01BUlRfUEhPTkVcIixcImlzVk5cIjp0cnVlfSIsImlhdCI6MTY4MDYxNDI3MSwiZGV2aWNlSWQiOiIzQjBGNDUyNUJDOEQ0NUI0QUQxNjZDNzdBMDQ1NjlFNiJ9.4GAMSL6i72oG52XlpLo0VckBEe37bKjqR5jIuSqSqoo',
'user-agent':'okhttp/4.12.0',
'x-nct-deviceid': '3B0F4525BC8D45B4AD166C77A04569E6',
'x-nct-version':'8.1.2',
'x-nct-language':'vi',
'x-nct-uuid':'a48d89a4d33e9a3c',
'x-nct-checksum':'ab6eb574836879df6bcb204ea3e3e655121521cfbf21a8959edbd9136d13bd30',
'x-nct-userid':'33007211',
'x-nct-os':'android',
'accept-encoding':'gzip'}
def ace(kenh, tenkenh):
	if 'acestream' in kenh:
		tach = kenh.split('//')
		p = tach[1]
	else:
		p = re.search(r'id=(.*?)&', kenh)[1] if '&' in kenh else kenh.split('id=')[1]
	kenhace = ''.join(("{'label': '", tenkenh.strip(),"', 'action': 'play', 'fanart': '', 'icon': '', 'id': '", p.strip(), "'}"))
	return f"plugin://script.module.horus/?{quote(b64encode(kenhace.encode('utf-8')).decode('utf-8'))}"
def getlink(url, ref, luu):
	try:
		try:
			r = get(url, timeout=20, max_age=luu, headers={'user-agent': useragentdf,'referer': ref.encode('utf-8')})
		except:
			r = get(url, timeout=20, max_age=luu, headers={'user-agent': useragentdf,'referer': ref.encode('utf-8')}, verify=False)
		if 'Cloudf' in r.text or 'CloudF' in r.text:
			scraper = create_scraper(delay=20, disableCloudflareV1=True, browser={'browser':'chrome','platform':'windows','mobile':False})
			rcf = scraper.get(url,headers={'Referer': url})
			rcf.encoding = 'utf-8'
			return rcf
		else:
			r.encoding = 'utf-8'
			return r
	except:
		try:
			ref = f'https://mi3s.top/web?trang={quote(url)}'
			try:
				r = get(ref, max_age=luu, timeout=20, headers={'user-agent': useragentdf,'referer': ref.encode('utf-8')})
			except:
				r = get(ref, max_age=luu, timeout=20, headers={'user-agent': useragentdf,'referer': ref.encode('utf-8')}, verify=False)
			r.encoding = 'utf-8'
			return r
		except:
			pass
def getlinkss(url, bien):
	with Session() as s:
		try:
			r = s.get(url, timeout=30, headers=bien)
		except:
			r = s.get(url, timeout=30, headers=bien, verify=False)
	return r
def getlinkweb(url, ref, luu):
	try:
		try:
			r = get(url, timeout=20, max_age=luu, headers={'sec-fetch-site': 'same-origin','user-agent': useragentweb,'referer': ref.encode('utf-8')})
		except:
			r = get(url, timeout=20, max_age=luu, headers={'sec-fetch-site': 'same-origin','user-agent': useragentweb,'referer': ref.encode('utf-8')}, verify=False)
		if 'Cloudf' in r.text or 'CloudF' in r.text:
			scraper = create_scraper(delay=20, disableCloudflareV1=True, browser={'browser':'chrome','platform':'windows','mobile':False})
			rcf = scraper.get(url,headers={'Referer': url})
			rcf.encoding = 'utf-8'
			return rcf
		else:
			r.encoding = 'utf-8'
			return r
	except:
		try:
			ref = f'https://mi3s.top/web?trang={quote(url)}'
			try:
				r = get(ref, max_age=luu, timeout=20, headers={'user-agent': useragentdf,'referer': ref.encode('utf-8')})
			except:
				r = get(ref, max_age=luu, timeout=20, headers={'user-agent': useragentdf,'referer': ref.encode('utf-8')}, verify=False)
			r.encoding = 'utf-8'
			return r
		except:
			pass
def getlinkphongblack(urlvmf, ref, luu):
	try:
		try:
			r = get(urlvmf, timeout=20, max_age=luu, headers={'user-agent': f'{useragentweb} VietMedia/1.0','referer': ref.encode('utf-8')})
		except:
			r = get(urlvmf, timeout=20, max_age=luu, headers={'user-agent': f'{useragentweb} VietMedia/1.0','referer': ref.encode('utf-8')}, verify=False)
		r.encoding = 'utf-8'
		return r
	except:
		pass
def getlinkip(url, ref):
	try:
		return getlinkss(url, {'user-agent': useragentott,'accept-encoding':'gzip','referer': ref.encode('utf-8')})
	except:
		try:
			return getlinkss(f'https://mi3s.top/web?trang={quote(url)}', {'user-agent': useragentott,'accept-encoding':'gzip','referer': ref.encode('utf-8')})
		except:
			pass
def postlinktimfs(url, ref, luu):
	try:
		try:
			r = post(url, timeout=20, max_age=luu, headers={'user-agent': useragentdf, 'referer': ref.encode('utf-8'), 'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiZnNoYXJlIiwidXVpZCI6IjcxZjU1NjFkMTUiLCJ0eXBlIjoicGFydG5lciIsImV4cGlyZXMiOjAsImV4cGlyZSI6MH0.WBWRKbFf7nJ7gDn1rOgENh1_doPc07MNsKwiKCJg40U'})
		except:
			r = post(url, timeout=20, max_age=luu, headers={'user-agent': useragentdf, 'referer': ref.encode('utf-8'), 'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiZnNoYXJlIiwidXVpZCI6IjcxZjU1NjFkMTUiLCJ0eXBlIjoicGFydG5lciIsImV4cGlyZXMiOjAsImV4cGlyZSI6MH0.WBWRKbFf7nJ7gDn1rOgENh1_doPc07MNsKwiKCJg40U'}, verify=False)
		r.encoding = 'utf-8'
		return r
	except:
		pass
def fu(url):
	try:
		r = getlinkss(url, {'user-agent':useragentdf,'referer':'https://www.google.com.vn/'})
		return r.url
	except:
		f = getlink(url,url,-1).url
		if '?trang=' in f:
			s = f.split('?trang=')[1]
		else:
			s = quote(url)
		r = getlink(f'http://thunghiem.x10.mx/final.php?trang={s}',f'http://thunghiem.x10.mx/final.php?trang={s}',-1)
		return r.text
def stream(url):
	c = re.sub(r'\s+', '%20', url.strip(), flags=re.UNICODE)
	return f'{c}&User-Agent={useragentdf}' if '|' in url else f'{c}|User-Agent={useragentdf}'
def streamiptv(url, user):
	b = f'User-Agent={user.strip()}'
	c = re.sub(r'\s+', '%20', url.strip(), flags=re.UNICODE)
	return f'{c}&{b}' if '|' in url else f'{c}|{b}'
def referer(url):
	a = urlparse(url.strip())
	ref = f'&Origin={a.scheme}://{a.netloc}&Referer={a.scheme}://{a.netloc}/&verifypeer=false'
	return ref
def replace_all(dict, str):
	pattern = re.compile('|'.join(re.escape(key) for key in dict.keys()))
	return pattern.sub(lambda match: dict[match.group()], str)
def get_file_path(filename):
	return join(addon_data_dir, filename)
def has_file_path(filename):
	return exists(get_file_path(filename))
def get_last_modified_time_file(filename):
	return int(getmtime(get_file_path(filename)))
def remove_file(filename):
	if has_file_path(filename):
		remove(get_file_path(filename))
def remove_folder(path):
	try:
		rmtree(path, ignore_errors=True, onerror=None)
	except:
		return False
def write_file(name, content, binary=False):
	if not exists(addon_data_dir):
		makedirs(addon_data_dir)
	path = get_file_path(name)
	try:
		write_mode = 'wb+' if binary else 'w+'
		f = open(path, mode=write_mode)
		f.write(content)
		f.close()
	except:
		pass
	return path
def read_file(name, binary=False):
	content = None
	read_mode = 'rb' if binary else 'r'
	try:
		path = get_file_path(name)
		f = open(path, mode=read_mode)
		content = f.read()
		f.close()
	except:
		pass
	return content
def ttfs(x):
	try:
		idfd = re.search(r'(file|folder)/([A-Z0-9]+)', x)[2]
		ufs = f'https://www.fshare.vn/api/v3/files/folder?linkcode={idfd}&sort=type%2Cname&page=1&per-page=50'
		r = getlinkss(ufs, {'user-agent':useragentdf,'origin':x,'referer':x})
		return r
	except:
		cache_cleanup(-1)
		remove_file('.urlquick.slite3')
		sys.exit()
def get_info_fs(x):
	try:
		r = ttfs(x)
		if 'current' in r.text:
			l = r.json()['current']
			return (l['name'], l['size'])
		else:
			return ('Dữ liệu này bị hỏng...', 0)
	except:
		return None
def userpassfs():
	username = Script.setting.get_string('username')
	password = Script.setting.get_string('password')
	if username and password:
		payload = {'user_email':username,'password':password,'app_key':keyfs}
		head = {'user-agent':userfs, 'content-type': 'application/json; charset=utf-8'}
		try:
			try:
				response = post('https://api.fshare.vn/api/user/login',data=dumps(payload),headers=head,timeout=20,max_age=7200)
			except:
				response = post('https://api.fshare.vn/api/user/login',data=dumps(payload),headers=head,timeout=20,max_age=7200, verify=False)
			headerfsvn = {'user-agent':userfs, 'cookie' : f"session_id={response.json()['session_id']}"}
			r = getlinkss('https://api.fshare.vn/api/user/get', headerfsvn)
			if r.status_code == 200:
				return (response.json()['token'], response.json()['session_id'])
			else:
				cache_cleanup(-1)
				remove_file('.urlquick.slite3')
				userpassfs()
		except:
			cache_cleanup(-1)
			remove_file('.urlquick.slite3')
			Script.notify(__addonnoti__, 'Đăng nhập thất bại')
			sys.exit()
	else:
		Script.notify(__addonnoti__, 'Vui lòng nhập tài khoản Fshare trong cài đặt của VN Media')
		sys.exit()
def getfs(x):
	try:
		j = userpassfs()
		payload = {'zipflag':0, 'url':x, 'password':'', 'token': j[0]}
		headerfsvn = {'user-agent':userfs, 'cookie' : f'session_id={j[1]}', 'content-type': 'application/json; charset=utf-8'}
		with Session() as s:
			try:
				uf = s.post('https://api.fshare.vn/api/session/download', timeout=20,data=dumps(payload),headers=headerfsvn)
			except:
				uf = s.post('https://api.fshare.vn/api/session/download', timeout=20,data=dumps(payload),headers=headerfsvn, verify=False)
		if 'location' in uf.text:
			return uf.json()['location']
		else:
			Script.notify(__addonnoti__, uf.json()['msg'])
			sys.exit()
	except:
		sys.exit()
def basicfs(x):
	try:
		j = userpassfs()
		idfd = re.search(r'(file|folder)/([A-Z0-9]+)', x)[2]
		payload = {'token': j[0], 'linkcode':idfd}
		headerfsvn = {'user-agent':userfs, 'cookie' : f'session_id={j[1]}', 'content-type': 'application/json; charset=utf-8'}
		with Session() as s:
			try:
				uf = s.post('https://api.fshare.vn/api/fileops/getBasicInfo', timeout=20, data=dumps(payload), headers=headerfsvn)
			except:
				uf = s.post('https://api.fshare.vn/api/fileops/getBasicInfo', timeout=20, data=dumps(payload), headers=headerfsvn, verify=False)
			return uf.json()['name']
	except:
		return 'Lỗi đăng nhập'
def getrow(row):
	return row['v'] if (row is not None) and (row['v'] is not None) else ''
def subdmtodm(url):
	r = getlink(f'{url}/bc/js/custom.js',url,-1).text
	match = re.search(r"url\s*:\s*'([^']+)'", r)[1]
	v = urlparse(match)
	bc = f'{v.scheme}://{v.netloc}'
	return bc
def quangcao():
	now = localtime()
	i = Listitem()
	i.label = 'Đang cập nhật. Hãy dành thời gian này cho gia đình và trở lại sau ít phút nữa nhé!'
	i.info['mediatype'] = 'episode'
	i.art['thumb'] = i.art['poster'] = f'https://www.xemlicham.com/images/ngay/lich-am-ngay-{now.tm_mday}-thang-{now.tm_mon}-nam-{now.tm_year}.png'
	i.path = qc
	return i
def ggdich(tk):
	r = getlink(f'https://translate.googleapis.com/translate_a/single?ie=UTF-8&oe=UTF-8&client=gtx&sl=en&tl=vi&dt=t&q={tk}', 'https://translate.google.com/', 1000)
	return r.json()[0][0][0]
def u90(x):
	url = 'http://bit.ly/tiengruoi'
	r = getlink(url, 'https://www.google.com.vn/',-1)
	soup = BeautifulSoup(r.content, 'html.parser')
	veno_links = soup.select('a[target="_blank"]')
	for link in veno_links:
		if re.search(x, link.get_text(), re.IGNORECASE):
			b = urlparse(link['href']).netloc
			bc = b if 'http' in b else f'https://{b}'
			return bc
def respphut90():
	tr = 'https://vebo.tv'
	resp90 = getlink(tr, tr,-1)
	if (resp90 is not None):
		html_content = re.sub(r"(\n\s*//.*)", "", resp90.text)
		ref = re.search(r'base_embed_url.*?("|\')([^"\s]+)("|\')', html_content)[2]
	else:
		ref = tr
	return ref
def yttk(tk):
	tim = re.sub(r"[\W_]+"," ", tk)
	return f'plugin://plugin.video.vnmedia/resources/lib/mkd/onyoutube/tim/trailer_youtube/?search_query={tim}'
def search_history_save(search_key):
	if not search_key:
		return
	content = read_file('historys.json')
	content = loads(content) if content else []
	idx = next((content.index(i) for i in content if search_key == i), -1)
	if (idx >= 0) and (len(content) > 0):
		del content[idx]
	elif len(content) >= 20:
		content.pop()
	content.insert(0, search_key)
	write_file('historys.json', dumps(content))
def search_history_clear():
	write_file('historys.json', dumps([]))
def search_history_get():
	content = read_file('historys.json')
	content = loads(content) if content else []
	return content
def save_last_watch_movie(data):
	if not data:
		return
	content = read_file('watcheds.json')
	content = loads(content, object_pairs_hook=OrderedDict) if content else OrderedDict()
	cache_id, query = data
	content.update({cache_id: query})
	content.move_to_end(cache_id, last=False)
	write_file('watcheds.json', dumps(content))
def get_last_watch_movie():
	content = read_file('watcheds.json')
	content = loads(content) if content else {}
	return content
def save_last_watch_play(data):
	if not data:
		return
	content = read_file('played.json')
	content = loads(content, object_pairs_hook=OrderedDict) if content else OrderedDict()
	cache_id, query = data
	content.update({cache_id: query})
	content.move_to_end(cache_id, last=False)
	write_file('played.json', dumps(content))
def get_last_play():
	content = read_file('played.json')
	content = loads(content) if content else {}
	return content
def gioithieu(title, mota, anh):
	item = Listitem()
	item.label = f'TRAILER: {italic(title)}'
	item.info['mediatype'] = 'episode'
	item.info['plot'] = mota
	item.art['thumb'] = item.art['poster'] = anh
	item.set_callback(Resolver.ref('/resources/lib/mkd/onyoutube/tim:trailer_youtube'), title)
	return item
def gmt7(time_str):
	try:
		time_obj = datetime.strptime(time_str, '%H:%M')
		gmp = time_obj + timedelta(hours=7)
		return gmp.strftime('%H:%M')
	except:
		return time_str
@Script.register
def remove_search_watch_movie(plugin, search_key):
	content = read_file('watcheds.json')
	content = loads(content, object_pairs_hook=OrderedDict) if content else OrderedDict()
	if search_key in content:
		del content[search_key]
		write_file('watcheds.json', dumps(content))
	executebuiltin('Container.Refresh()')
@Script.register
def remove_last_played(plugin, search_key):
	content = read_file('played.json')
	content = loads(content, object_pairs_hook=OrderedDict) if content else OrderedDict()
	if search_key in content:
		del content[search_key]
		write_file('played.json', dumps(content))
	executebuiltin('Container.Refresh()')
@Script.register
def remove_search_history(plugin, search_key):
	content = read_file('historys.json')
	content = loads(content) if content else []
	if search_key in content:
		content.remove(search_key)
		write_file('historys.json', dumps(content))
	executebuiltin('Container.Refresh()')
@Script.register
def search_history_clear(plugin):
	write_file('historys.json', dumps([]))
	executebuiltin('Container.Refresh()')
@Script.register
def clear_last_watch_movie(plugin):
	write_file('watcheds.json', '')
	executebuiltin('Container.Refresh()')
@Script.register
def clear_last_played(plugin):
	write_file('played.json', '')
	executebuiltin('Container.Refresh()')
def listqc(x, y, qc):
	i = Listitem()
	i.label = x
	i.path = qc.strip()
	i.subtitles = [y.strip()]
	return i
@Resolver.register
def play_vnm(plugin, url, title):
	save_last_watch_play((title, url))
	return listqc(title, news, url)
@Resolver.register
def ifr_bongda(plugin, url, title):
	headu = {'user-agent': useragentdf,'referer': url}
	resp = getlink(url, url, -1)
	if (resp is not None) and ('allowfullscreen' in resp.text):
		m = urlparse(url)
		linkweb = f'{m.scheme}://{m.netloc}'
		soup = BeautifulSoup(resp.content, 'html.parser')
		frame = soup.select_one('iframe[allowfullscreen]')['src']
		ifr = frame if 'http' in frame else f'{linkweb}{ifr}'
		r = getlink(ifr, url, -1)
		sre = re.compile(r'(https?://[^\s"]+\.m3u8[^"\']*)')
		if (r is not None) and ('.m3u8' in r.text):
			linkstream = sre.search(r.text)[1]
			d = getlink(linkstream, linkstream, -1)
			a = sre.search(d.text)[1] if (d is not None) and ('.m3u8' in d.text) and ('http' in d.text) else linkstream
			linkplay = f'{stream(a)}{referer(ifr)}'
			return listqc(title, news, linkplay)
		else:
			return listqc(title, news, qc)
	else:
		return listqc(title, news, qc)
@Resolver.register
def play_fs(plugin, url, title):
	if Script.setting.get_string('block_play_fs') == 'true':
		return listqc(title, news, qc)
	else:
		save_last_watch_movie((title, url))
		return listqc(title, news, getfs(url))
@Resolver.register
def playsocolive(plugin, numroom, timestamp, linkref, title):
	url = f'https://json.vnres.co/room/{numroom}/detail.json?v={timestamp}'
	r = getlink(url, url,-1)
	if r is not None:
		nd = re.search(r'(\{.*\})', r.text, re.DOTALL)[1]
		d = f"{stream(loads(nd)['data']['stream']['hdM3u8'])}{referer(linkref)}"
		return listqc(title, news, d)
	else:
		return listqc(title, news, qc)
@Resolver.register
def ifr_khomuc(plugin, url, title):
	r = getlink(url, url, -1)
	if (r is not None) and ('.m3u8' in r.text):
		match = re.search(r'(https?://[^\s"]+\.m3u8[^"\']*)', r.text)
		d = f'{stream(match[1])}{referer(url)}'
		return listqc(title, news, d)
	else:
		return listqc(title, news, qc)
@Resolver.register
def play_vtvgo(plugin, timekenh, tokenkenh, idkenh, x, title):
	payload = {'type_id': '1','id': idkenh,'time': timekenh,'token': tokenkenh}
	headx = {'user-agent': useragentweb,
	'x-requested-with': 'XMLHttpRequest',
	'referer': f'https://vtvgo.vn/xem-truc-tuyen-kenh-vtv-{idkenh}.html',
	'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'sec-fetch-site': 'same-origin'}
	with Session() as s:
		try:
			p = s.post('https://vtvgo.vn/ajax-get-stream', timeout=20, data=urlencode(payload, quote_via=quote), cookies=x, headers=headx)
		except:
			p = s.post('https://vtvgo.vn/ajax-get-stream', timeout=20, data=urlencode(payload, quote_via=quote), cookies=x, headers=headx, verify=False)
	if (p is not None) and ('.m3u8' in p.text):
		d = f'{stream(p.json()["chromecast_url"])}{referer("https://vtvgo.vn")}'
		return listqc(title, news, d)
	else:
		return listqc(title, news, qc)
@Resolver.register
def play_xlvtvgo(plugin, idkenh, title):
	u = f'https://vtvgo.vn/ajax-get-epg-detail?epg_id={idkenh}&time={veruser}'
	p = getlinkweb(u, u, -1)
	if (p is not None) and ('data' in p.text):
		d = f'{stream(p.json()["data"])}{referer("https://vtvgo.vn")}'
		return listqc(title, news, d)
	else:
		return listqc(title, news, qc)
@Resolver.register
def play_bm(plugin, url, title):
	r = getlink(url, url,-1)
	if (r is not None) and ('streamingUrl' in r.text):
		match = re.search(r'streamingUrl":"(.*?)"}', r.text)
		linkplay = f'{stream(match[1])}{referer(url)}'
		return listqc(title, news, linkplay)
	else:
		return listqc(title, news, qc)
@Resolver.register
def list_re90(plugin, url, ref, title):
	r = getlink(url, url, 1000)
	if (r is not None) and ('.m3u8' in r.text):
		match = re.search(r'(https?://[^\s"]+\.m3u8[^"\']*)', r.text)
		if '=http' in match[1]:
			try:
				m = re.search(r'=(.*?)&', match[1])
				lp = unquote(m[1])
			except:
				m = match[1].split('=http')
				lp = unquote(f'http{m[1]}')
			dp1 = f'{stream(lp)}{referer(ref)}'
			return listqc(title, news, dp1)
		else:
			dp2 = f'{stream(match[1])}{referer(ref)}'
			return listqc(title, news, dp2)
	else:
		return listqc(title, news, qc)
@Resolver.register
def playnct(plugin, url, title):
	idk = re.search(r'\.(\w+)\.html', url)
	if idk:
		r = getlinkss(f'https://graph.nhaccuatui.com/v7/songs/detail/{idk[1]}?iscloud=false&isDailyMix=false', headersnct)
		v= r.json()['data']['streamURL']
		linkplay = qc if not r.json()['data']['streamURL'] else v[-1]['stream']
		return listqc(title, news, linkplay)
	else:
		return listqc(title, news, qc)
@Resolver.register
def playvdnct(plugin, url, title):
	idk = re.search(r"(?<=\.)([\w-]+)(?=\.\w+$)", url)
	if idk:
		r = getlinkss(f'https://graph.nhaccuatui.com/v7/videos/detail/{idk[1]}?isFirst=false', headersnct)
		v= r.json()['data']['streamURL']
		linkplay = qc if not r.json()['data']['streamURL'] else v[-1]['stream']
		return listqc(title, news, linkplay)
	else:
		return listqc(title, news, qc)
@Resolver.register
def play123embed(plugin, url, title):
	try:
		if 'ajax' in url:
			r = getlink(url,url,-1).json()
		else:
			r1 = getlink(url,url,-1).text
			idk = re.search(r"loadSerieEpisode\('(.*?)'.*?'(.*?)'", r1)
			u2 = f'https://play.123embed.net/ajax/serie/get_sources/{idk[1]}/{idk[2]}/grab'
			r = getlink(u2, u2,-1).json()
		linkplay = loads(r['sources'])[0]['file']
		dp = f'{stream(linkplay)}{referer(url)}'
		sub = ''.join(k['file'] for k in loads(r['tracks']) if 'vietnam' in k['label'].lower())
		if 'http' in sub:
			return listqc(title, sub, dp)
		else:
			return listqc(title, news, dp)

	except:
		return listqc(title, news, qc)