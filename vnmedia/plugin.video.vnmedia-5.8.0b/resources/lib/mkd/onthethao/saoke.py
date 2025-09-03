from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, replace_all, stream, referer, quangcao
from datetime import datetime
from json import loads
from codequick.utils import color
import re, sys
def saoke():
	url = 'https://skapi.mediastation.live/sk-web-list.html'
	r = getlink(url, url,-1)
	try:
		return r.json()['data']['webs'][-1]
	except:
		sys.exit()
@Route.register
def index_saoke(plugin):
	yield []
	try:
		url = saoke()
		resp = getlink(url, 'https://www.google.com.vn/', 400)
		if (resp is not None):
			ll = re.search(r'(?<=,lives=)(.*?)(?=<)', resp.text)[1]
			nd = re.sub(r'([{,:])(\w+)([},:])', r'\1"\2"\3',ll)
			thaythe = {
				"'[":"[",
				"]'":"]"
				}
			m = loads(replace_all(thaythe, nd))
			for k in m:
				item = Listitem()
				item.art['thumb'] = item.art['poster'] = k['league']['picture'] if k['league'].get('picture') else 'https://mi3s.top/thumb/unnamed.jpg'
				tenm = color(f"{datetime.fromtimestamp(int(k['time'])/1000).strftime('%H:%M %d/%m')}: {k['title'].split(':')[1].strip()}", 'yellow') if k['blv'] else f"{datetime.fromtimestamp(int(k['time'])/1000).strftime('%H:%M %d/%m')}: {k['title'].split(':')[1].strip()}"
				item.label = tenm
				item.info['plot'] = f'{tenm}\nNguồn: {url}'
				item.info['mediatype'] = 'tvshow'
				item.set_callback(list_saoke, k['_id'], tenm)
				yield item
	except:
		yield quangcao()
@Route.register
def list_saoke(plugin, idsk=None, ten=None):
	yield []
	if any((idsk is None,ten is None)):
		pass
	else:
		try:
			unique_urls = set()
			url = saoke()
			resp = getlink(url, 'https://www.google.com.vn/', 400)
			if (resp is not None) and ('.m3u8' in resp.text):
				hostsPlayer = re.search(r'hostsPlayer:\["(.*?)"', resp.text)
				refplay = f'https://{hostsPlayer[1]}' if hostsPlayer else url
				ll = re.search(r'(?<=,lives=)(.*?)(?=<)', resp.text)[1]
				nd = re.sub(r'([{,:])(\w+)([},:])', r'\1"\2"\3',ll)
				thaythe = {
					"'[":"[",
					"]'":"]"
					}
				m = loads(replace_all(thaythe, nd))
				for k in m:
					try:
						if idsk in str(k):
							streams = [
								('hlsUrls', 'https://raw.githubusercontent.com/kenvnm/kvn/main/saoke.png', 'blv'),
								('hlsUrlsManNhan', 'https://raw.githubusercontent.com/kenvnm/kvn/main/mannhan.png', 'blvManNhan'),
								('hlsUrlsBongNhua', 'https://raw.githubusercontent.com/kenvnm/kvn/main/logo_1.png', 'blvBongNhua')
							]
							for stream_key, banner_key, blv_key in streams:
								if stream_key in k:
									ks = k[stream_key]
									stream_list = (p for p in ks if 'm3u8' in p['url'] or 'flv' in p['url'])
									for stream_item in stream_list:
										if stream_item['name']:
											su = stream_item['url']
											if su not in unique_urls:
												unique_urls.add(su)
												item = Listitem()
												item.info['mediatype'] = 'episode'
												item.art['thumb'] = item.art['poster'] = banner_key
												tenm = f'{stream_item["name"]} - {ten} ({k[blv_key]})' if k[blv_key] else f'{stream_item["name"]} - {ten}'
												item.label = tenm
												item.info['plot'] = f'{tenm}\nNguồn: {url}'
												item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), f'{stream(su)}{referer(refplay)}', tenm)
												yield item
					except:
						pass
			else:
				yield quangcao()
		except:
			yield quangcao()