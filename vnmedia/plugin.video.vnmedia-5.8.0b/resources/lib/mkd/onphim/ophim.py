from codequick import Route, Listitem, Resolver, Script
from resources.lib.kedon import getlink, quangcao, stream, gioithieu, yeucau
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote_plus
from codequick.utils import color
from html import unescape
import re
o1 = 'https://ophim1.com'
uop = f'{o1}/v1/api'
op = 'https://ophim.live'
def get_info_ophim(x):
	r = getlink(f'{uop}/phim/{x}','https://ophim1.com/',-1)
	try:
		kq = r.json()['data']
		try:
			img = kq['seoOnPage']['seoSchema']['image']
		except:
			img = 'https://raw.githubusercontent.com/kenvnm/kvn/main/ophim.png'
		try:
			ten = kq['item']['name']
		except:
			pass
		try:
			mota = unescape(re.sub('<.*?>', '', kq['item']['content']))
		except:
			mota = ten
		return (ten, img, mota)
	except:
		return None
def process_url(url):
	try:
		data = get_info_ophim(url)
		return url, data
	except:
		return url, None
@Route.register
def index_ophim(plugin):
	yield Listitem.search(ds_ophim)
	yield yeucau('https://t.me/+QMfjBOtNpkZmNTc1')
	T = {'Thể loại': op_tl,
	'Quốc gia': op_qg}
	dulieu = {
	'Phim mới': f'{uop}/home',
	'Phim bộ': f'{uop}/danh-sach/phim-bo',
	'Phim bộ hoàn thành': f'{uop}/danh-sach/phim-bo-hoan-thanh',
	'Phim lẻ': f'{uop}/danh-sach/phim-le',
	'TV shows': f'{uop}/danh-sach/tv-shows',
	'Hoạt hình': f'{uop}/danh-sach/hoat-hinh',
	'Phim thuyết minh': f'{uop}/danh-sach/phim-thuyet-minh',
	'Phim lồng tiếng': f'{uop}/danh-sach/phim-long-tieng',
	'Phim phụ đề': f'{uop}/danh-sach/phim-vietsub',
	'Phim phụ đề độc quyền': f'{uop}/danh-sach/subteam'
	}
	for b in T:
		i = Listitem()
		i.label = b
		i.info['mediatype'] = 'tvshow'
		i.art['thumb'] = i.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/ophim.png'
		i.set_callback(T[b])
		yield i
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/ophim.png'
		item.set_callback(ds_ophim, dulieu[k], 1)
		yield item
@Route.register
def op_tl(plugin):
	yield []
	u = f'{o1}/the-loai'
	resp = getlink(u, u, 1000)
	if (resp is not None):
		ri = resp.json()
		for k in ri:
			if Script.setting.get_string('kenh18') == 'true':
				item = Listitem()
				item.label = k['name']
				item.info['mediatype'] = 'tvshow'
				item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/ophim.png'
				item.set_callback(ds_ophim, f"{uop}/the-loai/{k['slug']}", 1)
				yield item
			else:
				if k['slug'] != 'phim-18':
					item = Listitem()
					item.label = k['name']
					item.info['mediatype'] = 'tvshow'
					item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/ophim.png'
					item.set_callback(ds_ophim, f"{uop}/the-loai/{k['slug']}", 1)
					yield item
@Route.register
def op_qg(plugin):
	yield []
	u = f'{o1}/quoc-gia'
	resp = getlink(u, u, 1000)
	if (resp is not None):
		ri = resp.json()
		for k in ri:
			item = Listitem()
			item.label = k['name']
			item.info['mediatype'] = 'tvshow'
			item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/ophim.png'
			item.set_callback(ds_ophim, f"{uop}/quoc-gia/{k['slug']}", 1)
			yield item
@Route.register
def ds_ophim(plugin, search_query=None, next_page=None):
	yield []
	try:
		if '://' not in search_query:
			next_page = 1
			sr = quote_plus(search_query)
			match = f'{uop}/tim-kiem?keyword={sr}'
		else:
			match = search_query
		n = f'{match}&page={next_page}' if '?' in match else f'{match}?page={next_page}'
		resp = getlink(n, n, 1000)
		if (resp is not None):
			ri = resp.json()['data']['items']
			urls = [k['slug'] for k in ri] if Script.setting.get_string('kenh18') == 'true' else [k['slug'] for k in ri if 'phim-18' not in str(k)]
			length = len(urls)
			if length>0:
				with ThreadPoolExecutor(length) as ex:
					results = ex.map(process_url, urls)
				for (l, data) in results:
					if data is not None:
						item = Listitem()
						item.label = data[0]
						item.info['mediatype'] = 'tvshow'
						item.info['plot'] = f'{data[2]}\nNguồn: {op}'
						item.info['mediatype'] = 'tvshow'
						item.art['thumb'] = item.art['poster'] = data[1]
						item.set_callback(id_ophim, l)
						yield item
				item1 = Listitem()
				item1.label = f'Trang {next_page + 1}'
				item1.info['mediatype'] = 'tvshow'
				item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
				item1.set_callback(ds_ophim, match, next_page + 1)
				yield item1
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def id_ophim(plugin, idk=None):
	yield []
	if idk is None:
		pass
	else:
		try:
			t = f'{uop}/phim/{idk}'
			resp = getlink(t, t, 1000)
			if (resp is not None):
				try:
					kq = resp.json()
					ke = kq['data']['item']['episodes']
					title = kq['data']['seoOnPage']['titleHead']
					mota = unescape(re.sub('<.*?>', '', kq['data']['item']['content']))
					anh = kq['data']['seoOnPage']['seoSchema']['image']
					yield gioithieu(title, mota, anh)
					b = ((k1['server_name'], k2['name'], k2['link_m3u8']) for k1 in ke for k2 in k1['server_data'] if 'link_m3u8' in k2)
					for k in b:
						item = Listitem()
						tenm = f"{color(k[0], 'yellow')} Tập {k[1]} - {title}"
						item.label = tenm
						item.info['mediatype'] = 'episode'
						item.info['plot'] = f'{mota}\nNguồn: {op}'
						item.art['thumb'] = item.art['poster'] = anh
						item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), stream(k[2]), tenm)
						yield item
				except:
					pass
			else:
				yield quangcao()
		except:
			yield quangcao()