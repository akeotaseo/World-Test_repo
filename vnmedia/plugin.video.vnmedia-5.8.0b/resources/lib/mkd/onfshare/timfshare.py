from codequick import Script, Route, Listitem, Resolver
from resources.lib.kedon import veruser, postlinktimfs, getlink, quangcao, yttk
from resources.lib.mkd.onfshare.thuvienhd import ufn
from resources.lib.mkd.onfshare.thuviencine import ufc
from resources.lib.mkd.onfshare.ifshare import hdvn
from resources.lib.mkd.onphim.ophim import uop, op
from resources.lib.mkd.onphim.nguonc import unc
from resources.lib.mkd.onphim.kkphim import ukk, kk
from resources.lib.mkd.onphim.fmovies import fmo
from resources.lib.mkd.onphim.phimmoi import pm
from resources.lib.mkd.onphim.anime47 import uanm47
from resources.lib.mkd.onphim.bluphim import bl
from resources.lib.mkd.onphim.apiionline import apii, uapi
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from json import loads
from codequick.utils import color
import re
def get_tkfs1(search_query):
	r = getlink(f'http://phongblack.online/search-tungbui.php?author=phongblack&search={search_query}', 'http://www.google.com', 1000)
	return ((m['label'], re.search(r"url=(\S+)", m['path'])[1], m['info']['plot']) for m in (k for k in r.json()['items'] if k.get('is_playable', False) is False) if 'fshare' in m['path'])
def get_tkfs2(search_query):
	r = postlinktimfs(f'https://api.timfshare.com/v1/string-query-search?query={search_query}', 'https://timfshare.com/', 1000)
	return ((k['name'], k['url'], k['size']) for k in r.json().get('data', []))
def get_tkfs3(search_query):
	return ((t['title'].replace('&&','-'), t['image'], t['id']) for t in getlink(f'{ufn}/?feed=fsharejson&search={search_query}', ufn, 1000).json() if getlink(f'{ufn}/?feed=fsharejson&search={search_query}', ufn, 1000).content != getlink(f'{ufn}/?feed=fsharejson&search=', ufn, 1000).content)
def get_tkfs4():
	return ((t['title'].replace('&&','-'), t['image'], t['id']) for t in loads(re.sub(r'<(.*?)\n','',getlink(f'{ufn}/?feed=fsharejson&search={search_query}', ufn, 1000).text)) if getlink(f'{ufn}/?feed=fsharejson&search={search_query}', ufn, 1000).content != getlink(f'{ufn}/?feed=fsharejson&search=', ufn, 1000).content)
def get_tkfs6(search_query):
	r = getlink(f'{ufc}/?s={search_query}', ufc, 1000)
	soup = BeautifulSoup(r.text, 'html.parser')
	return ((k['title'], k.select_one('img.lazy')['data-src'], k.select_one('p.movie-description').get_text(strip=True), k['href']) for k in soup.select('div.item.normal a'))
def get_tkfs7(search_query):
	r = getlink(f'{ufn}/?s={search_query}', ufn, 1000)
	soup = BeautifulSoup(r.text, 'html.parser')
	return ((k.select_one('div.title a').get_text(strip=True), k.select_one('div.image img')['src'], k.select_one('div.contenido p').get_text(strip=True), k.select_one('a')['href']) for k in soup.select('div.result-item article'))
def get_mp5(search_query, next_page):
	r = getlink(f'{pm}?search={search_query}&page={next_page}', pm, 1000)
	soup = BeautifulSoup(r.text, 'html.parser')
	s = soup.select('ul.last-film-box li a.movie-item')
	return ((k['title'], re.search(r"background-image:url\('(.*?)'", k.select_one('div.public-film-item-thumb')['style'])[1], k['href']) for k in s if 'sắp chiếu' not in k.get_text(strip=True).lower())
def get_mp7(search_query):
	r = getlink(f'{bl}/search?k={search_query}', bl, 1000)
	soup = BeautifulSoup(r.text, 'html.parser')
	s = soup.select('div#page-info div.list-films ul li.item a')
	return ((k.select_one('.name').get_text(strip=True), k.select_one('img')['src'], k['href']) for k in s)
def get_mp8(search_query, next_page):
	r = getlink(f'{uapi}/danh-sach?search={search_query}&page={next_page}', uapi, 1000)
	return ((k['name'], k['thumb_url'], k['slug']) for k in r.json()['items'])
@Route.register
def searchfs(plugin, search_query=None):
	yield []
	if search_query is None:
		pass
	else:
		try:
			search_query = quote_plus(search_query)
			with ThreadPoolExecutor(4) as ex:
				f1 = ex.submit(get_tkfs1, search_query)
				f2 = ex.submit(get_tkfs2, search_query)
				f3 = ex.submit(get_tkfs3, search_query)
				f4 = ex.submit(get_tkfs4, search_query)
			try:
				for t in f3.result():
					item = Listitem()
					item.label = t[0]
					item.info['mediatype'] = 'tvshow'
					item.info['plot'] = f"{t[0]}\nNguồn: {ufn}"
					item.info['trailer'] = yttk(t[0])
					item.art['thumb'] = item.art['poster'] = t[1]
					item.set_callback(Route.ref('/resources/lib/mkd/onfshare/thuvienhd:thuvienhd_link'), t[2])
					yield item
			except:
				for t in f4.result():
					item = Listitem()
					item.label = t[0]
					item.info['mediatype'] = 'tvshow'
					item.info['plot'] = f"{t[0]}\nNguồn: {ufn}"
					item.info['trailer'] = yttk(t[0])
					item.art['thumb'] = item.art['poster'] = t[1]
					item.set_callback(Route.ref('/resources/lib/mkd/onfshare/thuvienhd:thuvienhd_link'), t[2])
					yield item
			try:
				imgfs = 'https://raw.githubusercontent.com/kenvnm/kvn/main/gocchiase.png'
				for m in f1.result():
					item = Listitem()
					item.label = m[0]
					item.info['trailer'] = yttk(m[0])
					item.art['thumb'] = item.art['poster'] = imgfs
					item.info['plot'] = f"{m[2]}\nNguồn: Google Trang tính" if m[2] is not None else f"{m[0]}\nNguồn: Google Trang tính"
					item.context.script(Script.ref('/resources/lib/mkd/onfshare/ifshare:tfavo'), 'Thêm vào Fshare Favorite', m[1])
					if '/file/' in m[1]:
						if Script.setting.get_string('taifshare') == 'true':
							item.context.script(Script.ref('/resources/lib/download:downloadfs'), 'Tải về', m[1])
						item.info['mediatype'] = 'episode'
						item.set_callback(Resolver.ref('/resources/lib/kedon:play_fs'), m[1], m[0])
					else:
						item.info['mediatype'] = 'tvshow'
						item.set_callback(Route.ref('/resources/lib/mkd/onfshare/ifshare:index_fs'), m[1], 0, imgfs)
					yield item
			except:
				pass
			try:
				imgfs = 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
				for k in f2.result():
					item = Listitem()
					item.label = k[0]
					item.info['plot'] = f"{k[0]}\nNguồn: https://timfshare.com"
					item.info['trailer'] = yttk(k[0])
					item.art['thumb'] = item.art['poster'] = imgfs
					item.context.script(Script.ref('/resources/lib/mkd/onfshare/ifshare:tfavo'), 'Thêm vào Fshare Favorite', k[1])
					if 'folder' in k[1]:
						item.info['mediatype'] = 'tvshow'
						item.set_callback(Route.ref('/resources/lib/mkd/onfshare/ifshare:index_fs'), k[1], 0, imgfs)
					else:
						item.info['mediatype'] = 'episode'
						item.info['size'] = k[2]
						if Script.setting.get_string('taifshare') == 'true':
							item.context.script(Script.ref('/resources/lib/download:downloadfs'), 'Tải về', k[1])
						item.set_callback(Resolver.ref('/resources/lib/kedon:play_fs'), k[1], k[0])
					yield item
			except:
				pass
		except:
			yield quangcao()
@Route.register
def searchvnm(plugin, search_query=None):
	yield []
	if search_query is None:
		pass
	else:
		try:
			search_query = quote_plus(search_query)
			with ThreadPoolExecutor(7) as ex:
				f1 = ex.submit(get_tkfs1, search_query)
				f2 = ex.submit(get_tkfs2, search_query)
				f6 = ex.submit(get_tkfs6, search_query)
				f7 = ex.submit(get_tkfs7, search_query)
				m5 = ex.submit(get_mp5, search_query, 1)
				m7 = ex.submit(get_mp7, search_query)
				m8 = ex.submit(get_mp8, search_query, 1)
			try:
				for k in f7.result():
					item = Listitem()
					item.label = f"{color('thuvienhd', 'yellow')} {k[0]}"
					item.info['plot'] = f"{k[2]}\nNguồn: {ufn}"
					item.info['mediatype'] = 'tvshow'
					item.art['thumb'] = item.art['poster'] = k[1]
					item.set_callback(Route.ref('/resources/lib/mkd/onfshare/thuvienhd:thuvienhd_linktk'), k[3])
					yield item
			except:
				pass
			try:
				for k in f6.result():
					item = Listitem()
					item.label = f"{color('thuviencine', 'yellow')} {k[0]}"
					item.info['plot'] = f"{k[2]}\nNguồn: {ufc}"
					item.info['mediatype'] = 'tvshow'
					item.art['thumb'] = item.art['poster'] = k[1]
					item.set_callback(Route.ref('/resources/lib/mkd/onfshare/thuviencine:thuviencine_link'), k[3])
					yield item
			except:
				pass
			try:
				imgfs = 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
				for m in f1.result():
					item = Listitem()
					item.label = f"{color('gsheet', 'yellow')} {m[0]}"
					item.info['trailer'] = yttk(m[0])
					item.art['thumb'] = item.art['poster'] = imgfs
					item.info['plot'] = f"{m[2]}\nNguồn: Google Trang tính" if m[2] is not None else f"{m[0]}\nNguồn: Google Trang tính"
					item.context.script(Script.ref('/resources/lib/mkd/onfshare/ifshare:tfavo'), 'Thêm vào Fshare Favorite', m[1])
					if '/file/' in m[1]:
						item.info['mediatype'] = 'episode'
						if Script.setting.get_string('taifshare') == 'true':
							item.context.script(Script.ref('/resources/lib/download:downloadfs'), 'Tải về', m[1])
						item.set_callback(Resolver.ref('/resources/lib/kedon:play_fs'), m[1], m[0])
					else:
						item.info['mediatype'] = 'tvshow'
						item.set_callback(Route.ref('/resources/lib/mkd/onfshare/ifshare:index_fs'), m[1], 0, imgfs)
					yield item
			except:
				pass
			try:
				for k in f2.result():
					item = Listitem()
					item.label = f"{color('timfshare', 'yellow')} {k[0]}"
					item.info['plot'] = f"{k[0]}\nNguồn: https://timfshare.com"
					item.info['trailer'] = yttk(k[0])
					imgfs = 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
					item.art['thumb'] = item.art['poster'] = imgfs
					item.context.script(Script.ref('/resources/lib/mkd/onfshare/ifshare:tfavo'), 'Thêm vào Fshare Favorite', k[1])
					if 'folder' in k[1]:
						item.info['mediatype'] = 'tvshow'
						item.set_callback(Route.ref('/resources/lib/mkd/onfshare/ifshare:index_fs'), k['url'], 0, imgfs)
					else:
						item.info['mediatype'] = 'episode'
						item.info['size'] = k[2]
						if Script.setting.get_string('taifshare') == 'true':
							item.context.script(Script.ref('/resources/lib/download:downloadfs'), 'Tải về', k[1])
						item.set_callback(Resolver.ref('/resources/lib/kedon:play_fs'), k[1], k[0])
					yield item
			except:
				pass
			try:
				for k in m8.result():
					item = Listitem()
					item.label = f"{color('apiionline', 'yellow')} {k[0]}"
					item.info['plot'] = f"{k[0]}\nNguồn: {apii}"
					item.art['thumb'] = item.art['poster'] = f"{apii}/image/{k[1]}"
					item.info['mediatype'] = 'tvshow'
					item.set_callback(Route.ref('/resources/lib/mkd/onphim/apiionline:id_apiionline'), k[2])
					yield item
			except:
				pass
			try:
				for k in m5.result():
					item = Listitem()
					item.label = f"{color('phimmoi', 'yellow')} {k[0]}"
					item.info['mediatype'] = 'tvshow'
					item.info['plot'] = f'{k[0]}\nNguồn: {pm}'
					item.art['thumb'] = item.art['poster'] = k[1] if k[1].startswith('http') else f'{pm}{k[1]}'
					item.set_callback(Route.ref('/resources/lib/mkd/onphim/phimmoi:episode_phimmoi'), k[2], k[0], k[0], k[1])
					yield item
			except:
				pass
			try:
				for k in m7.result():
					item = Listitem()
					item.label = f"{color('bluphim', 'yellow')} {k[0]}"
					item.info['mediatype'] = 'tvshow'
					item.info['plot'] = f'{k[0]}\nNguồn: {bl}'
					item.art['thumb'] = item.art['poster'] = k[1] if k[1].startswith('http') else f'{bl}{k[1]}'
					item.set_callback(Route.ref('/resources/lib/mkd/onphim/bluphim:episode_bluphim'), k[2], k[0], k[0], k[1])
					yield item
			except:
				pass
		except:
			yield quangcao()
@Route.register
def search_freefilm(plugin, search_query=None, next_page=None):
	yield []
	try:
		if search_query is None:
			search_query = quote_plus(search_query)
		if next_page is None:
			next_page = 1
			with ThreadPoolExecutor(3) as ex:
				m5 = ex.submit(get_mp5, search_query, next_page)
				m7 = ex.submit(get_mp7, search_query)
				m8 = ex.submit(get_mp8, search_query, next_page)
		else:
			with ThreadPoolExecutor(2) as ex:
				m5 = ex.submit(get_mp5, search_query, next_page)
				m8 = ex.submit(get_mp8, search_query, next_page)
		try:
			for k in m8.result():
				item = Listitem()
				item.label = f"{color('apiionline', 'yellow')} {k[0]}"
				item.info['plot'] = f"{k[0]}\nNguồn: {apii}"
				item.art['thumb'] = item.art['poster'] = f"{apii}/image/{k[1]}"
				item.info['mediatype'] = 'tvshow'
				item.set_callback(Route.ref('/resources/lib/mkd/onphim/apiionline:id_apiionline'), k[2])
				yield item
		except:
			yield []
		try:
			for k in m5.result():
				item = Listitem()
				item.label = f"{color('phimmoi', 'yellow')} {k[0]}"
				item.info['mediatype'] = 'tvshow'
				item.info['plot'] = f'{k[0]}\nNguồn: {pm}'
				item.art['thumb'] = item.art['poster'] = k[1] if k[1].startswith('http') else f'{pm}{k[1]}'
				item.set_callback(Route.ref('/resources/lib/mkd/onphim/phimmoi:episode_phimmoi'), k[2], k[0], k[0], k[1])
				yield item
		except:
			yield []
		try:
			for k in m7.result():
				item = Listitem()
				item.label = f"{color('bluphim', 'yellow')} {k[0]}"
				item.info['mediatype'] = 'tvshow'
				item.info['plot'] = f'{k[0]}\nNguồn: {bl}'
				item.art['thumb'] = item.art['poster'] = k[1] if k[1].startswith('http') else f'{bl}{k[1]}'
				item.set_callback(Route.ref('/resources/lib/mkd/onphim/bluphim:episode_bluphim'), k[2], k[0], k[0], k[1])
				yield item
		except:
			yield []
		item1 = Listitem()
		item1.label = f'Trang {next_page + 1}'
		item1.info['mediatype'] = 'tvshow'
		item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
		item1.set_callback(search_freefilm, search_query, next_page + 1)
		yield item1
	except:
		yield quangcao()
@Route.register
def index_pdx(plugin):
	streams = [
		('Đề xuất', 'https://raw.githubusercontent.com/kenvnm/kvn/main/dexuat.png', index_hn),
		('BXH Thế giới', 'https://raw.githubusercontent.com/kenvnm/kvn/main/on.png', Route.ref('/resources/lib/mkd/onfshare/fsmdb:index_fsmdb'))
	]
	for name_key, banner_key, route_key in streams:
		i = Listitem()
		i.label = name_key
		i.info['mediatype'] = 'tvshow'
		i.art['thumb'] = i.art['poster'] = banner_key
		i.set_callback(route_key)
		yield i
	dulieu = {
	'Đặc sắc': -1,
	'Hành động': 76,
	'Phiêu lưu': 86,
	'Hình sự': 77,
	'Trinh thám': 106,
	'Võ thuật': 111,
	'Rùng rợn': 98,
	'Huyền bí': 80,
	'Kinh dị': 81,
	'Viễn tưởng': 109,
	'Hài hước': 74,
	'Lãng mạn': 82,
	'Thần thoại': 100,
	'Cổ trang': 71,
	'Phim TVB': 108,
	'Phim bộ Hàn': 89,
	'Phim bộ Mỹ': 91,
	'Lồng tiếng': 84,
	'Hoạt hình': 78
	}
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = f'https://raw.githubusercontent.com/kenvnm/kvn/main/dexuat.png'
		item.set_callback(hdo_page, dulieu[k])
		yield item
@Route.register
def index_hn(plugin):
	yield []
	try:
		resptvhd = get_tkfs3('')
		try:
			kqtvhd = resptvhd.json()
			for t in kqtvhd:
				tenmm = t['title'].replace('&&','-')
				item = Listitem()
				item.label = tenmm
				item.info['plot'] = f'{tenmm}\nNguồn: {ufn}'
				item.info['mediatype'] = 'tvshow'
				item.info['trailer'] = yttk(tenmm)
				item.art['thumb'] = item.art['poster'] = t['image']
				item.set_callback(Route.ref('/resources/lib/mkd/onfshare/thuvienhd:thuvienhd_link'), t['id'])
				yield item
		except:
			text = resptvhd.text
			data = re.sub(r'<(.*?)\n','',text)
			jsm = loads(data)
			for t in jsm:
				tenmm = t['title'].replace('&&','-')
				item = Listitem()
				item.label = tenmm
				item.info['plot'] = f'{tenmm}\nNguồn: {ufn}'
				item.info['mediatype'] = 'tvshow'
				item.info['trailer'] = yttk(tenmm)
				item.art['thumb'] = item.art['poster'] = t['image']
				item.set_callback(Route.ref('/resources/lib/mkd/onfshare/thuvienhd:thuvienhd_link'), t['id'])
				yield item
	except:
		yield quangcao()
@Route.register
def hdo_page(plugin, idp=None):
	yield []
	if idp is None:
		pass
	else:
		try:
			trangtiep = f'{ufn}/?feed=rss&exclude_cats=250004&category={idp}&posts_per_page=100'
			resp = getlink(trangtiep, trangtiep, 1000)
			if (resp is not None):
				soup = BeautifulSoup(resp.text, 'html.parser')
				it = soup.select('item')
				for k in it:
					item = Listitem()
					tenb = k.select_one('title').get_text(strip=True)
					tenm = tenb.replace('&&','-')
					item.label = tenm
					mota = k.select_one('description').get_text(strip=True)
					anh = k.select_one('enclosure')['url']
					kid = k.select_one('id').get_text(strip=True)
					item.info['plot'] = f'{mota}\nNguồn: {ufn}'
					item.info['trailer'] = yttk(tenm)
					item.info['mediatype'] = 'tvshow'
					item.art['thumb'] = item.art['poster'] = anh
					item.set_callback(Route.ref('/resources/lib/mkd/onfshare/thuvienhd:thuvienhd_link'), kid)
					yield item
			else:
				yield quangcao()
		except:
			yield quangcao()