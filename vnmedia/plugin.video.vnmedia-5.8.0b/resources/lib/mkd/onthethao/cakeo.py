from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao, stream, referer, respphut90, u90
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import re
ucakeo = 'https://api.cakeo.xyz/match/live'
def get_list(fansiteId, matchId):
	url = f'https://api.cakeo.xyz/match/matchMeta/{matchId}-rid-{fansiteId}'
	resp = getlink(url, url,-1)
	return resp
@Route.register
def index_cakeo(plugin):
	yield []
	try:
		resp = getlink(ucakeo,ucakeo,-1)
		if (resp is not None):
			rd = resp.json()['data']
			for k in rd:
				for q in k['fansites']:
					item = Listitem()
					time = datetime.fromtimestamp(int(k['timestamp'])/1000).strftime('%H:%M %d/%m')
					tenv = f"{time} {k['name']}"
					item.label = f"{tenv} ({q['name']})"
					item.info['plot'] = f'{tenv}\nNguồn: {u90}'
					item.info['mediatype'] = 'tvshow'
					logotour = k['tournament']['logo']
					item.art['thumb'] = item.art['poster'] = logotour if logotour else 'https://raw.githubusercontent.com/kenvnm/kvn/main/cakeotv.png'
					item.set_callback(list_cakeo, q['model_id'], k['id'], tenv)
					yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def list_cakeo(plugin, fansiteId=None, matchId=None, title=None):
	yield []
	if any((fansiteId is None, matchId is None, title is None)):
		pass
	else:
		try:
			with ThreadPoolExecutor(2) as ex:
				f1 = ex.submit(respphut90)
				f2 = ex.submit(get_list, fansiteId, matchId)
				ref = f1.result()
				resp = f2.result()
			if (resp is not None) and ('.m3u8' in resp.text or 'youtube.com' in resp.text):
				kq = resp.json()['data']['fansiteData']
				kp = kq['play_urls']
				cm = kq['blv']
				blv = ' - '.join((h['name'] for h in cm or []))
				for k in kp:
					item = Listitem()
					tenm = f'{k["name"]} - {title} ({blv})' if cm else f'{k["name"]} - {title}'
					item.label = tenm
					item.info['plot'] = f'{tenm}\nNguồn: {u90}'
					item.info['mediatype'] = 'episode'
					item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/cakeotv.png'
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