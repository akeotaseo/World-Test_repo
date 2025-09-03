from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao, stream
from urllib.parse import quote_plus
import re
unx = 'https://api.sexnguon.com'
@Route.register
def search_nguonx(plugin, search_query=None):
	yield []
	if search_query is None:
		pass
	else:
		try:
			next_page = 1
			sr = quote_plus(search_query)
			url = f'{unx}/api.php/provide/vod/?ac=detail&wd={sr}'
			trangtiep = f'{url}&pg={next_page}'
			sr = quote_plus(search_query)
			r = getlink(trangtiep, url, 1800)
			if (r is not None) and ('vod_play_url' in r.text):
				for k in r.json()['list']:
					name = k['vod_name']
					ref = k['vod_blurb']
					p1 = k['vod_play_url']
					p2 = re.search(r'(http.*)', p1)[1]
					play = f'{stream(p2)}{referer(ref)}'
					item = Listitem()
					item.label = name
					item.info['mediatype'] = 'episode'
					item.art['thumb'] = item.art['poster'] = k['vod_pic']
					item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), play, name)
					yield item
				if r.json()['pagecount'] > 1:
					item1 = Listitem()
					item1.label = f'Trang {next_page + 1}'
					item1.info['mediatype'] = 'tvshow'
					item1.art['thumb'] = item1.art['poster'] = 'https://mi3s.top/thumb/next.png'
					item1.set_callback(ds_nguonx, url, next_page + 1)
					yield item1
		except:
			yield quangcao()
@Route.register
def index_nguonx(plugin):
	yield Listitem.search(search_nguonx)
	dulieu = {
	'Mới nhất': f'{unx}/api.php/provide/vod/?ac=detail',
	'TokyoHot': f'{unx}/api.php/provide/vod/?ac=detail&t=20',
	'Phim Nhật Bản': f'{unx}/api.php/provide/vod/?ac=detail&t=1',
	'Japan HDV': f'{unx}/api.php/provide/vod/?ac=detail&t=6',
	'Phim Trung Quốc': f'{unx}/api.php/provide/vod/?ac=detail&t=13',
	'China Live': f'{unx}/api.php/provide/vod/?ac=detail&t=2',
	'Âu Mỹ': f'{unx}/api.php/provide/vod/?ac=detail&t=3',
	'Nhật Bản': f'{unx}/api.php/provide/vod/?ac=detail&t=14',
	'Hoạt hình': f'{unx}/api.php/provide/vod/?ac=detail&t=7',
	'Japan HV': f'{unx}/api.php/provide/vod/?ac=detail&t=8',
	'Jui Hatano': f'{unx}/api.php/provide/vod/?ac=detail&t=22',
	'Cencored': f'{unx}/api.php/provide/vod/?ac=detail&t=21'
	}
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://mi3s.top/thumb/phim/nguonx.png'
		item.set_callback(ds_nguonx, dulieu[k], 1)
		yield item
@Route.register
def ds_nguonx(plugin, match=None, next_page=None):
	yield []
	if any((match is None,next_page is None)):
		pass
	else:
		try:
			n = f'{match}&pg={next_page}'
			r = getlink(n, n, 1800)
			if (r is not None) and ('vod_play_url' in r.text):
				for k in r.json()['list']:
					name = k['vod_name']
					p1 = k['vod_play_url']
					p2 = re.search(r'(http.*)', p1)[1]
					item = Listitem()
					item.label = name
					item.info['mediatype'] = 'episode'
					item.art['thumb'] = item.art['poster'] = k['vod_pic']
					item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), stream(p2), name)
					yield item
				if next_page < r.json()['pagecount']:
					item1 = Listitem()
					item1.label = f'Trang {next_page + 1}'
					item1.info['mediatype'] = 'tvshow'
					item1.art['thumb'] = item1.art['poster'] = 'https://mi3s.top/thumb/next.png'
					item1.set_callback(ds_nguonx, match, next_page + 1)
					yield item1
			else:
				yield quangcao()
		except:
			yield quangcao()