from codequick import Resolver, Route, Listitem, Script
from resources.lib.kedon import getlinkss, userpassfs, userfs, yttk, get_last_watch_movie, clear_last_watch_movie, quangcao, get_last_modified_time_file, has_file_path, remove_file, read_file, write_file, useragentdf, __addonnoti__
from requests.packages.urllib3.util import connection
from requests import Session
from bs4 import BeautifulSoup
from xbmc import executebuiltin
from xbmcgui import Dialog
from time import time
from datetime import datetime, timedelta
from codequick.utils import color
import re, sys, json, pickle
connection.HAS_IPV6 = False
hdvn = 'https://www.hdvietnam.xyz'
@Route.register
def index_fs(plugin, folderfs=None, next_page=None, img=None):
	yield []
	if any((folderfs is None, next_page is None, img is None)):
		pass
	else:
		try:
			token, session_id = userpassfs()[:2]
			payload = {'token': token, 'url': folderfs, 'dirOnly': 0, 'pageIndex': next_page, 'limit':100}
			headerfsvn = {'user-agent':userfs, 'cookie' :  f'session_id={session_id}', 'content-type': 'application/json; charset=utf-8'}
			with Session() as s:
				try:
					kq = s.post('https://api.fshare.vn/api/fileops/getFolderList', timeout=20, data=json.dumps(payload), headers=headerfsvn)
				except:
					kq = s.post('https://api.fshare.vn/api/fileops/getFolderList', timeout=20, data=json.dumps(payload), headers=headerfsvn, verify=False)
				if (kq is not None) and ('furl' in kq.text):
					kj = kq.json()
					if 'http' in img:
						imgfs = img
					else:
						imgfs = 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
					for k in kj:
						item = Listitem()
						tenm = k['name']
						item.label = tenm
						linkfs = k['furl']
						item.info['plot'] = f'{tenm}\nNguồn: https://fshare.vn'
						item.info['trailer'] = yttk(tenm)
						item.art['thumb'] = item.art['poster'] = imgfs
						item.context.script(tfavo, 'Thêm vào Fshare Favorite', linkfs)
						if 'file' in k['furl']:
							item.info['mediatype'] = 'episode'
							item.info['size'] = k['size']
							if Script.setting.get_string('taifshare') == 'true':
								item.context.script(Script.ref('/resources/lib/download:downloadfs'), 'Tải về', linkfs)
							item.set_callback(Resolver.ref('/resources/lib/kedon:play_fs'), linkfs, tenm)
						else:
							item.info['mediatype'] = 'tvshow'
							item.set_callback(index_fs, linkfs, 0, imgfs)
						yield item
					if len(kq.json())==100:
						item1 = Listitem()
						item1.label = f'Trang {next_page + 2}'
						item1.info['mediatype'] = 'tvshow'
						item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
						item1.set_callback(index_fs, folderfs, next_page + 1, imgfs)
						yield item1
				else:
					yield quangcao()
		except:
			executebuiltin('Container.Refresh()')
@Route.register
def index_daxem(plugin):
	yield []
	b = get_last_watch_movie()
	if b:
		for m in b:
			item = Listitem()
			item.label = m
			item.info['mediatype'] = 'episode'
			item.info['trailer'] = yttk(m)
			item.info['plot'] = f'{m}\nNguồn: https://fshare.vn'
			item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
			if Script.setting.get_string('taifshare') == 'true':
				item.context.script(Script.ref('/resources/lib/download:downloadfs'), 'Tải về', b[m])
			item.context.script(Script.ref('/resources/lib/kedon:remove_search_watch_movie'), 'Xoá khỏi lịch sử xem', m)
			item.context.script(Resolver.ref('/resources/lib/kedon:play_fs'), 'Thêm vào Fshare Favorite', b[m])
			item.set_callback(Resolver.ref('/resources/lib/kedon:play_fs'), b[m], m)
			yield item
		Fshareplaydel = {'label': 'Xoá lịch sử xem',
		'art': {'thumb': 'https://apkmodo.net/wp-content/uploads/2022/01/WATCHED-APK.jpg'},
		'callback': clear_last_watch_movie}
		yield Listitem.from_dict(**Fshareplaydel)
@Route.register
def fs_favorite(plugin):
	yield []
	try:
		headerfsvn = {'user-agent':userfs, 'cookie' : f'session_id={userpassfs()[1]}'}
		r = getlinkss('https://api.fshare.vn/api/fileops/listFavorite', headerfsvn)
		if 'linkcode' in r.text:
			rj = r.json()
			v = (k for k in rj if k['linkcode'])
			imgfs = 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
			for k in v:
				item = Listitem()
				item.label = k['name']
				item.info['plot'] = f'{k["name"]}\nNguồn: https://fshare.vn'
				item.info['trailer'] = yttk(k['name'])
				item.art['thumb'] = item.art['poster'] = imgfs
				if k['type'] == '0':
					item.info['mediatype'] = 'tvshow'
					item.context.script(xfavo, 'Xoá khỏi Fshare Favorite', f"http://fshare.vn/folder/{k['linkcode']}")
					item.set_callback(index_fs, f'https://fshare.vn/folder/{k["linkcode"]}', 0, imgfs)
				else:
					item.info['size'] = k['size']
					item.info['mediatype'] = 'episode'
					if Script.setting.get_string('taifshare') == 'true':
						item.context.script(Script.ref('/resources/lib/download:downloadfs'), 'Tải về', f'https://fshare.vn/file/{k["linkcode"]}')
					item.context.script(xfavo, 'Xoá khỏi Fshare Favorite', f'https://fshare.vn/file/{k["linkcode"]}')
					item.set_callback(Resolver.ref('/resources/lib/kedon:play_fs'), f'https://fshare.vn/file/{k["linkcode"]}', k['name'])
				yield item
	except:
		executebuiltin('Container.Refresh()')
@Route.register
def fs_topfollow(plugin):
	yield []
	try:
		headerfsvn = {'user-agent':userfs, 'cookie' : f'session_id={userpassfs()[1]}'}
		r = getlinkss('https://api.fshare.vn/api/fileops/getTopFollowMovie', headerfsvn)
		rj = r.json()
		for k in rj:
			item = Listitem()
			item.label = k['name']
			linkfs = f'https://fshare.vn/folder/{k["linkcode"]}'
			item.info['mediatype'] = 'tvshow'
			item.info['plot'] = f'{k["name"]}\nNguồn: https://fshare.vn'
			item.info['trailer'] = yttk(k['name'])
			imgfs = 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
			item.art['thumb'] = item.art['poster'] = imgfs
			item.context.script(tfavo, 'Thêm vào Fshare Favorite', linkfs)
			item.set_callback(index_fs, linkfs, 0, imgfs)
			yield item
	except:
		executebuiltin('Container.Refresh()')
@Script.register
def fs_info(plugin):
	try:
		headerfsvn = {'user-agent':userfs, 'cookie' : f'session_id={userpassfs()[1]}'}
		c = getlinkss('https://api.fshare.vn/api/user/get', headerfsvn).json()
		try:
			timestamp = int(c['expire_vip'])
			epoch = datetime(1970, 1, 1)
			dt_object = epoch + timedelta(seconds=timestamp)
			timei = dt_object.strftime("%d/%m/%Y")
		except:
			timei = c['expire_vip']
		Dialog().ok(__addonnoti__, f"{c['name']}-{c['id']} {color(c['email'], 'yellow')}\nLoại tài khoản: {color(c['account_type'], 'yellow')}\nNgày hết hạn: {timei}\nĐiểm thưởng: {c['totalpoints']}")
	except:
		Dialog().ok(__addonnoti__, 'Lỗi đăng nhập')
@Script.register
def tfavo(plugin, x):
	try:
		idfd = re.search(r'(file|folder)/([A-Z0-9]+)', x)[2]
		token, session_id = userpassfs()[:2]
		headerfsvn = {'user-agent':userfs, 'cookie' : f'session_id={session_id}', 'content-type': 'application/json; charset=utf-8'}
		payload = f'{{"token": "{token}", "items": ["{idfd}"], "status": 1}}'
		with Session() as s:
			try:
				r = s.post('https://api.fshare.vn/api/fileops/ChangeFavorite', timeout=30, data=payload, headers=headerfsvn)
			except:
				r = s.post('https://api.fshare.vn/api/fileops/ChangeFavorite', timeout=30, data=payload, headers=headerfsvn, verify=False)
			Script.notify(__addonnoti__, 'Đã thêm vào Fshare Favorite') if '200' in r.text else Script.notify(__addonnoti__, 'Không thêm được vào Fshare Favorite')
	except:
		Script.notify(__addonnoti__, 'Không thêm được vào Fshare Favorite')
		sys.exit()
@Script.register
def xfavo(plugin, x):
	try:
		idfd = re.search(r'(file|folder)/([A-Z0-9]+)', x)[2]
		token, session_id = userpassfs()[:2]
		headerfsvn = {'user-agent':userfs, 'cookie' : f'session_id={session_id}', 'content-type': 'application/json; charset=utf-8'}
		payload = f'{{"token": "{token}", "items": ["{idfd}"], "status": 0}}'
		with Session() as s:
			try:
				s.post('https://api.fshare.vn/api/fileops/ChangeFavorite', timeout=30, data=payload, headers=headerfsvn)
			except:
				s.post('https://api.fshare.vn/api/fileops/ChangeFavorite', timeout=30, data=payload, headers=headerfsvn, verify=False)
			Script.notify(__addonnoti__, 'Đã xoá khỏi Fshare Favorite')
			executebuiltin('Container.Refresh()')
	except:
		sys.exit()
def loginfhdvn():
	if has_file_path('hdvietnam.bin') and get_last_modified_time_file('hdvietnam.bin') + 3600 < int(time()):
		remove_file('hdvietnam.bin')
	if has_file_path('hdvietnam.bin'):
		return pickle.loads(read_file('hdvietnam.bin', True))
	else:
		with Session() as s:
			headers = {'user-agent':useragentdf,'origin':hdvn,'referer':f'{hdvn}/'}
			try:
				site = s.get(f'{hdvn}/forums/', headers=headers, timeout=20)
			except:
				site = s.get(f'{hdvn}/forums/', headers=headers, timeout=20, verify=False)
			login_data = {'login':'romvemot@gmail.com','register':0,'password':'bimozie','remember':1,'cookie_check':1,'_xfToken':'','redirect':'/forums/'}
			try:
				s.post(f'{hdvn}/login/login', data=login_data, headers=headers)
			except:
				s.post(f'{hdvn}/login/login', data=login_data, headers=headers, verify=False)
			write_file('hdvietnam.bin', pickle.dumps(s), True)
			return s
def likehdvn(url):
	s = loginfhdvn()
	soup = BeautifulSoup(s.get(url).text, 'html.parser')
	token = soup.select_one('input[name="_xfToken"]')['value']
	like = f'{hdvn}/{soup.select_one("div.publicControls a.LikeLink.item.control")["href"]}'
	if 'like' in like:
		data_like = {'_xfRequestUri':f'/{url}','_xfToken':token,'_xfNoRedirect':1,'_xfResponseType': 'json'}
		s.post(like, data=data_like)
		return
def tkhdvn(x):
	params = {
			'keywords': x,
			'nodes[]': [337, 344, 345, 346, 33, 271, 324, 77, 78, 116, 150, 57, 123],
			'child_nodes': 1
		}
	url = f'{hdvn}/search/search'
	with Session() as s:
		try:
			uf = s.post(url, timeout=30, data=params, headers={'user-agent': useragentdf,'referer': url.encode('utf-8')})
		except:
			uf = s.post(url, timeout=30, data=params, headers={'user-agent': useragentdf,'referer': url.encode('utf-8')}, verify=False)
		return uf
