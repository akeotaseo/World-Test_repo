from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao, stream, referer, respphut90, u90
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from codequick.utils import color
import re
uthapcam = 'https://api.thapcam.xyz/api/match/featured/mt'
def get_list(idk):
	url = f'http://api.thapcam.xyz/api/match/{idk}/meta'
	resp = getlink(url, url,-1)
	return resp
def xemlai(page):
	url = f'https://api.thapcam.xyz/api/news/thapcam/list/xemlai/{page}'
	resp = getlink(url, url, 1000)
	return resp
@Route.register
def index_thapcam(plugin):
	yield []
	try:
		resp = getlink(uthapcam,uthapcam,-1)
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
				item.art['thumb'] = item.art['poster'] = logotour if logotour else 'https://raw.githubusercontent.com/kenvnm/kvn/main/thapcamtv.png'
				item.set_callback(list_thapcam, k['id'], tenv)
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def list_thapcam(plugin, idk=None, title=None):
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
					item = Listitem()
					tenm = f'{k["name"]} - {title} ({blv})' if cm else f'{k["name"]} - {title}'
					item.label = tenm
					item.info['plot'] = f'{tenm}\nNguồn: {u90}'
					item.info['mediatype'] = 'episode'
					item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/thapcamtv.png'
					linkplay = k['url']
					if 'youtube.com' in linkplay:
						idvd = re.search(r"\?v=([a-zA-Z0-9_-]+)", linkplay)[1]
						item.set_path(f'plugin://plugin.video.youtube/play/?video_id={idvd}')
					else:
						linktrandau = f'{stream(linkplay)}{referer(ref)}'
						item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), linktrandau, tenm)
					yield item
			else:
				yield quangcao()
		except:
			pass
@Route.register
def xemlai_tc(plugin, page=None):
	yield []
	if page is None:
		pass
	else:
		try:
			with ThreadPoolExecutor(2) as ex:
				f1 = ex.submit(respphut90)
				f2 = ex.submit(xemlai, page)
				ref = f1.result()
				resp = f2.result()
			if (resp is not None):
				kq = resp.json()
				kl = kq['data']['list']
				for k in kl:
					item1 = Listitem()
					tenv = k['name']
					item1.label = tenv
					item1.info['plot'] = f'{tenv}\nNguồn: {u90}'
					item1.info['mediatype'] = 'episode'
					item1.art['thumb'] = item1.art['poster'] = k['feature_image']
					item1.set_callback(Resolver.ref('/resources/lib/kedon:list_re90'), f"https://api.thapcam.xyz/api/news/thapcam/detail/{k['id']}", ref, k["name"])
					yield item1
				item2 = Listitem()
				item2.label = f'Trang {page + 1}'
				item2.info['mediatype'] = 'tvshow'
				item2.art['thumb'] = item2.art['poster'] = f'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
				item2.set_callback(xemlai_tc, page + 1)
				yield item2
			else:
				yield quangcao()
		except:
			yield quangcao()