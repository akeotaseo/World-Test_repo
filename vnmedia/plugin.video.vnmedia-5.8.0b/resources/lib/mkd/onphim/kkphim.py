from codequick import Route, Listitem, Resolver, Script
from resources.lib.kedon import getlink, quangcao, stream, gioithieu, yeucau
from concurrent.futures import ThreadPoolExecutor
from codequick.utils import color
from urllib.parse import quote_plus
from html import unescape
ukk = 'https://phimapi.com'
kk = 'https://kkphim.com'
def get_info_kkphim(x):
	r = getlink(f'{ukk}/phim/{x}',ukk,-1)
	try:
		if Script.setting.get_string('kenh18') == 'true':
			if r is not None:
				kq = r.json()['movie']
				try:
					img = kq['poster_url']
				except:
					img = 'https://raw.githubusercontent.com/kenvnm/kvn/main/kkphim.png'
				try:
					ten = kq['name']
				except:
					pass
				try:
					mota = unescape(kq['content'])
				except:
					mota = ten
				return (ten, img, mota)
			else:
				return None
		else:
			if r is not None and '18+' not in r.text:
				kq = r.json()['movie']
				try:
					img = kq['poster_url']
				except:
					img = 'https://raw.githubusercontent.com/kenvnm/kvn/main/kkphim.png'
				try:
					ten = kq['name']
				except:
					pass
				try:
					mota = unescape(kq['content'])
				except:
					mota = ten
				return (ten, img, mota)
			else:
				return None
	except:
		return None
def process_url(url):
	try:
		data = get_info_kkphim(url)
		return url, data
	except:
		return url, None
@Route.register
def index_kkphim(plugin):
	yield Listitem.search(ds_kkphim)
	yield yeucau('https://t.me/phimnguon')
	T = {'Thể loại': kk_tl,
	'Quốc gia': kk_qg}
	dulieu = {
	'Phim mới': f'{ukk}/danh-sach/phim-moi-cap-nhat-v2?limit=30',
	'Phim lẻ': f'{ukk}/v1/api/danh-sach/phim-le?limit=30',
	'Phim bộ': f'{ukk}/v1/api/danh-sach/phim-bo?limit=30',
	'Hoạt hình': f'{ukk}/v1/api/danh-sach/hoat-hinh?limit=30',
	'TV Shows': f'{ukk}/v1/api/danh-sach/tv-shows?limit=30'
	}
	for b in T:
		i = Listitem()
		i.label = b
		i.info['mediatype'] = 'tvshow'
		i.art['thumb'] = i.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/kkphim.png'
		i.set_callback(T[b])
		yield i
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/kkphim.png'
		item.set_callback(ds_kkphim, dulieu[k], 1)
		yield item
@Route.register
def kk_tl(plugin):
	yield []
	u = f'{ukk}/the-loai'
	resp = getlink(u, u, 1000)
	if (resp is not None):
		ri = resp.json()
		for k in ri:
			if Script.setting.get_string('kenh18') == 'true':
				item = Listitem()
				item.label = k['name']
				item.info['mediatype'] = 'tvshow'
				item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/kkphim.png'
				item.set_callback(ds_kkphim, f"{ukk}/v1/api/the-loai/{k['slug']}?limit=30", 1)
				yield item
			else:
				if k['slug'] != 'phim-18':
					item = Listitem()
					item.label = k['name']
					item.info['mediatype'] = 'tvshow'
					item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/kkphim.png'
					item.set_callback(ds_kkphim, f"{ukk}/v1/api/the-loai/{k['slug']}?limit=30", 1)
					yield item
@Route.register
def kk_qg(plugin):
	yield []
	u = f'{ukk}/quoc-gia'
	resp = getlink(u, u, 1000)
	if (resp is not None):
		ri = resp.json()
		for k in ri:
			item = Listitem()
			item.label = k['name']
			item.info['mediatype'] = 'tvshow'
			item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/kkphim.png'
			item.set_callback(ds_kkphim, f"{ukk}/v1/api/quoc-gia/{k['slug']}?limit=30", 1)
			yield item
@Route.register
def ds_kkphim(plugin, search_query=None, next_page=None):
	yield []
	try:
		if '://' not in search_query:
			next_page = 1
			sr = quote_plus(search_query)
			match = f'{ukk}/v1/api/tim-kiem?keyword={sr}'
		else:
			match = search_query
		n = f'{match}&page={next_page}' if '?' in match else f'{match}?page={next_page}'
		resp = getlink(n, n, 1000)
		ri = resp.json()['data']['items'] if (resp is not None) and ('"data"' in resp.text) else resp.json()['items']
		urls = [k['slug'] for k in ri]
		length = len(urls)
		if length>0:
			with ThreadPoolExecutor(length) as ex:
				results = ex.map(process_url, urls)
			for (l, data) in results:
				if data is not None:
					item = Listitem()
					item.label = data[0]
					item.info['plot'] = f'{data[2]}\nNguồn: {kk}'
					item.info['mediatype'] = 'tvshow'
					item.art['thumb'] = item.art['poster'] = data[1]
					item.set_callback(id_kkphim, l)
					yield item
			if '://' in search_query:
				item1 = Listitem()
				item1.label = f'Trang {next_page + 1}'
				item1.info['mediatype'] = 'tvshow'
				item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
				item1.set_callback(ds_kkphim, match, next_page + 1)
				yield item1
	except:
		yield quangcao()
@Route.register
def id_kkphim(plugin, idk=None):
	yield []
	if idk is None:
		pass
	else:
		try:
			t = f'{ukk}/phim/{idk}'
			resp = getlink(t, t, 1000)
			if (resp is not None):
				try:
					kq = resp.json()
					ke = kq['episodes']
					title = kq['movie']['name']
					title2= kq['movie']['origin_name']
					namefilm = f'{title}-{title2}'
					mota = unescape(kq['movie']['content'])
					anh = kq['movie']['poster_url']
					yield gioithieu(namefilm, mota, anh)
					b = ((k1['server_name'], k2['name'], k2['link_m3u8']) for k1 in ke for k2 in k1['server_data'] if 'link_m3u8' in k2)
					for k in b:
						item = Listitem()
						tenm = f"{color(k[0], 'yellow')} {k[1]}-{namefilm}"
						item.label = tenm
						item.info['mediatype'] = 'episode'
						item.info['plot'] = f'{mota}\nNguồn: {kk}'
						item.art['thumb'] = item.art['poster'] = anh
						item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), stream(k[2]), tenm)
						yield item
				except:
					pass
			else:
				yield quangcao()
		except:
			yield quangcao()