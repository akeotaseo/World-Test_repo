from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao, yeucau, stream, referer
from urllib.parse import quote_plus
from codequick.utils import color
from html import unescape
avdb = 'https://avdbapi.com'
@Route.register
def index_avdb(plugin):
	yield Listitem.search(ds_avdb)
	yield yeucau('https://t.me/avdb_api')
	item = Listitem()
	item.label = 'Phim mới'
	item.info['mediatype'] = 'tvshow'
	item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kodivietnam/kodivietnam.github.io/main/avdb.jpg'
	item.set_callback(ds_avdb, f'{avdb}/api.php/provide/vod/?ac=detail', 1)
	yield item
@Route.register
def ds_avdb(plugin, search_query=None, next_page=None):
	yield []
	try:
		if '://' not in search_query:
			next_page = 1
			sr = quote_plus(search_query)
			match = f'{avdb}/api.php/provide/vod?ac=detail&wd={sr}'
		else:
			match = search_query
		n = f'{match}&pg={next_page}' if '?' in match else f'{match}?pg={next_page}'
		resp = getlink(n, n, 1000)
		try:
			data = resp.json()['list']
			b = ((episode['server_name'], episode['server_data'][data_key]['slug'], item['name'], item['poster_url'], item['description'], episode['server_data'][data_key]['link_embed'])
				for item in data
				for episode in [item['episodes']] 
				for data_key in episode['server_data'] 
				if 'link_embed' in episode['server_data'][data_key])
			for k in b:
				item = Listitem()
				tenm = f"{color(k[1], 'yellow')} {color(k[0], 'red')} {unescape(k[2])}"
				linkplay = f"{stream(k[5].split('?s=')[1])}{referer(k[5].split('?s=')[0])}"
				item.label = tenm
				item.info['plot'] = f'{unescape(k[4])}\nNguồn: {avdb}'
				item.info['mediatype'] = 'episode'
				item.art['thumb'] = item.art['poster'] = k[3]
				item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), linkplay, tenm)
				yield item
			if next_page < resp.json()['pagecount']:
				item1 = Listitem()
				item1.label = f'Trang {next_page + 1}'
				item1.info['mediatype'] = 'tvshow'
				item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
				item1.set_callback(ds_avdb, match, next_page + 1)
				yield item1
		except:
			pass
	except:
		yield quangcao()