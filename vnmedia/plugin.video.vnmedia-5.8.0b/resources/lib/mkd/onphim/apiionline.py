from codequick import Route, Listitem, Resolver, Script
from resources.lib.kedon import getlink, quangcao, stream, gioithieu
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote_plus
from codequick.utils import color
from html import unescape
import re
apii = 'https://apii.online'
uapi = f'{apii}/apii'
def get_info_apiionline(x):
	r = getlink(f'{uapi}/phim/{x}',apii,-1)
	try:
		kq = r.json()['movie']
		try:
			img = kq['thumb_url']
		except:
			img = 'https://raw.githubusercontent.com/kenvnm/kvn/main/apiionline.png'
		try:
			ten = unescape(kq['name'])
		except:
			pass
		try:
			mota = unescape(re.sub('<.*?>', '', kq['content']))
		except:
			mota = ten
		return (ten, img, mota)
	except:
		return None
def process_url(url):
	try:
		data = get_info_apiionline(url)
		return url, data
	except:
		return url, None
@Route.register
def index_apiionline(plugin):
	yield Listitem.search(ds_apiionline)
	item = Listitem()
	item.label = 'Phim mới'
	item.info['mediatype'] = 'tvshow'
	item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/apiionline.png'
	item.set_callback(ds_apiionline, f'{uapi}/danh-sach/phim-moi-cap-nhat', 1)
	yield item
	T = {'Thể loại': apii_tl,
	'Quốc gia': apii_qg}
	for b in T:
		i = Listitem()
		i.label = b
		i.info['mediatype'] = 'tvshow'
		i.art['thumb'] = i.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/apiionline.png'
		i.set_callback(T[b])
		yield i
@Route.register
def apii_tl(plugin):
	yield []
	u = f'{uapi}/the-loai'
	resp = getlink(u, u, 1000)
	if (resp is not None):
		ri = resp.json()
		for k in ri:
			if Script.setting.get_string('kenh18') == 'true':
				item = Listitem()
				item.label = k['name']
				item.info['mediatype'] = 'tvshow'
				item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/apiionline.png'
				item.set_callback(ds_apiionline, f"{uapi}/danh-sach?category={k['slug']}", 1)
				yield item
			else:
				if k['slug'] != 'phim-18':
					item = Listitem()
					item.label = k['name']
					item.info['mediatype'] = 'tvshow'
					item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/apiionline.png'
					item.set_callback(ds_apiionline, f"{uapi}/danh-sach?category={k['slug']}", 1)
					yield item
@Route.register
def apii_qg(plugin):
	yield []
	u = f'{uapi}/quoc-gia'
	resp = getlink(u, u, 1000)
	if (resp is not None):
		ri = resp.json()
		for k in ri:
			item = Listitem()
			item.label = k['name']
			item.info['mediatype'] = 'tvshow'
			item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/apiionline.png'
			item.set_callback(ds_apiionline, f"{uapi}/danh-sach?country={k['slug']}", 1)
			yield item
@Route.register
def ds_apiionline(plugin, search_query=None, next_page=None):
	yield []
	try:
		if '://' not in search_query:
			next_page = 1
			sr = quote_plus(search_query)
			match = f'{uapi}/danh-sach?search={sr}'
		else:
			match = search_query
		n = f'{match}&page={next_page}' if '?' in match else f'{match}?page={next_page}'
		resp = getlink(n, n, 1000)
		if (resp is not None):
			ri = resp.json()['items']
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
						item.info['plot'] = f'{data[2]}\nNguồn: {apii}'
						item.info['mediatype'] = 'tvshow'
						item.art['thumb'] = item.art['poster'] = data[1]
						item.set_callback(id_apiionline, l)
						yield item
				item1 = Listitem()
				item1.label = f'Trang {next_page + 1}'
				item1.info['mediatype'] = 'tvshow'
				item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
				item1.set_callback(ds_apiionline, match, next_page + 1)
				yield item1
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def id_apiionline(plugin, idk=None):
	yield []
	if idk is None:
		pass
	else:
		try:
			t = f'{uapi}/phim/{idk}'
			resp = getlink(t, t, 1000)
			if (resp is not None):
				try:
					kq = resp.json()
					title = kq['movie']['name']
					mota = unescape(re.sub('<.*?>', '', kq['movie']['content']))
					anh = kq['movie']['thumb_url']
					yield gioithieu(title, mota, anh)
					b = ((k1['server_name'], k2['name'], k2['link_m3u8']) for k1 in kq['episodes'] for k2 in k1['server_data'] if 'link_m3u8' in k2)
					for k in b:
						item = Listitem()
						tenm = f"{color(k[0], 'yellow')} Tập {k[1]} - {title}"
						item.label = tenm
						item.info['mediatype'] = 'episode'
						item.info['plot'] = f'{mota}\nNguồn: {apii}'
						item.art['thumb'] = item.art['poster'] = anh
						if '[nc]' in k[0].lower():
							item.set_callback(Resolver.ref('/resources/lib/kedon:play_nc'), k[2], tenm)
						else:
							item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), stream(k[2]), tenm)
						yield item
				except:
					pass
			else:
				yield quangcao()
		except:
			yield quangcao()