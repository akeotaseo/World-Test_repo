from codequick import Route, Listitem, Resolver
from resources.lib.kedon import quangcao, getlink, referer, stream, respphut90, u90
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from codequick.utils import color
import re
def get_list(idk):
	url = f'http://api.vebo.xyz/api/match/{idk}/meta'
	resp = getlink(url, url,-1)
	return resp
def xemlai(pl, page):
	url = f'https://api.vebo.xyz/api/news/mitom/list/{pl}/{page}'
	resp = getlink(url, url, 1000)
	return resp
@Route.register
def index_90p(plugin):
	yield []
	try:
		url90 = 'https://api.vebo.xyz/api/match/featured/mt'
		resp = getlink(url90, url90,-1)
		if (resp is not None):
			rd = resp.json()['data']
			for k in rd:
				item = Listitem()
				time = datetime.fromtimestamp(int(k['timestamp'])/1000).strftime('%H:%M %d/%m')
				tg = color(time, 'red') if 'live' in k['match_status'] else time
				tenm = color(k['name'], 'yellow') if k['commentators'] else k['name']
				tenv = f'{tg} {tenm}'
				item.label = tenv
				item.info['plot'] = f'{tenv}\nNguồn: {u90}'
				item.info['mediatype'] = 'tvshow'
				logotour = k['tournament']['logo']
				item.art['thumb'] = item.art['poster'] = logotour if logotour else 'https://raw.githubusercontent.com/kenvnm/kvn/main/vebo.png'
				item.set_callback(list_90p, k['id'], tenv)
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def list_90p(plugin, idk=None, title=None):
	yield []
	if any((idk is None,title is None)):
		pass
	else:
		try:
			with ThreadPoolExecutor(2) as ex:
				f1 = ex.submit(respphut90)
				f2 = ex.submit(get_list, idk)
				ref = f1.result()
				resp = f2.result()
			if (resp is not None) and ('.m3u8' in resp.text or 'youtube.com' in resp.text):
				kq = resp.json()['data']
				kp = kq['play_urls']
				cm = kq['commentators']
				blv = ' - '.join((h['name'] for h in cm or []))
				for k in kp:
					tenm = f'{k["name"]} - {title} ({blv})' if cm else f'{k["name"]} - {title}'
					item = Listitem()
					item.label = tenm
					item.info['plot'] = f'{tenm}\nNguồn: {u90}'
					item.info['mediatype'] = 'episode'
					item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/90p.png'
					linkplay = k['url']
					if 'youtube.com' in linkplay:
						idvd = re.search(r"\?v=([a-zA-Z0-9_-]+)", linkplay)[1]
						item.set_path(f'plugin://plugin.video.youtube/play/?video_id={idvd}')
					else:
						item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), f'{stream(linkplay)}{referer(ref)}', tenm)
					yield item
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def xemlai_90p(plugin, pl=None, page=None):
	yield []
	if any((pl is None,page is None)):
		pass
	else:
		try:
			with ThreadPoolExecutor(2) as ex:
				f1 = ex.submit(respphut90)
				f2 = ex.submit(xemlai, pl, page)
				ref = f1.result()
				resp = f2.result()
			if (resp is not None):
				kq = resp.json()
				kl = kq['data']['list']
				f = kq['data']['highlight']
				if f:
					item = Listitem()
					tenv = f['name']
					item.label = tenv
					item.info['plot'] = f'{tenv}\nNguồn: {u90}'
					item.info['mediatype'] = 'episode'
					item.art['thumb'] = item.art['poster'] = f['feature_image']
					item.set_callback(Resolver.ref('/resources/lib/kedon:list_re90'), f"https://api.vebo.xyz/api/news/mitom/detail/{f['id']}", ref, f['name'])
					yield item
				for k in kl:
					item1 = Listitem()
					tenm = k['name']
					item1.label = tenm
					item1.info['plot'] = f'{tenm}\nNguồn: {u90}'
					item1.info['mediatype'] = 'episode'
					item1.art['thumb'] = item1.art['poster'] = k['feature_image']
					item1.set_callback(Resolver.ref('/resources/lib/kedon:list_re90'), f"https://api.vebo.xyz/api/news/mitom/detail/{k['id']}", ref, k["name"])
					yield item1
				item2 = Listitem()
				item2.label = f'Trang {page + 1}'
				item2.info['mediatype'] = 'tvshow'
				item2.art['thumb'] = item2.art['poster'] = f'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
				item2.set_callback(xemlai_90p, pl, page + 1)
				yield item2
			else:
				yield quangcao()
		except:
			yield quangcao()