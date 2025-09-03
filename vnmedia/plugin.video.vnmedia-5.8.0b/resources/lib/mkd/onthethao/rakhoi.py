from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, stream, referer, quangcao
from codequick.utils import color
import re
urk = 'https://rakhoi8.link'
@Route.register
def index_rakhoi(plugin):
	yield []
	try:
		u = 'https://api.rkdata.xyz/v1/rakhoi/home.html'
		r = getlink(u,u, 400)
		if (r is not None):
			kq = r.json()['data']['lives']
			dq = ((k['id'], k['timeShort'], k['home']['name'], k['away']['name'], k['blv']['name'], k['status']) for v in kq for k in v['matchs'])
			for k in dq:
				tg = color(k[1], 'red') if k[5]==1 else k[1]
				mau = color(f'{k[2]} vs {k[3]}', 'yellow')
				tenm = f'{tg} {mau} - {k[4]}' if k[4] else f'{tg} {k[2]} vs {k[3]}'
				item = Listitem()
				item.label = tenm
				item.info['plot'] = f'{tenm}\nNguồn: {urk}'
				item.info['mediatype'] = 'tvshow'
				item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/rakhoi.png'
				item.set_callback(list_rakhoi, k[0], tenm)
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def list_rakhoi(plugin, idck=None, tentran=None):
	yield []
	if any((idck is None,tentran is None)):
		pass
	else:
		try:
			u = f'https://watch.rkplayer.xyz/v1/rakhoi/{idck}.html'
			r = getlink(u,u,400)
			if r is not None:
				s = re.findall(r',name:"(.*?)",url:"(.*?)"', r.text)
				for v in s:
					if 'm3u8' in v[1] or 'flv' in v[1]:
						linkplay = f'{stream(v[1])}{referer(u)}'
						item = Listitem()
						item.info['mediatype'] = 'episode'
						tenm = f'{v[0]} - {tentran}'
						item.label = tenm
						item.info['plot'] = f'{tenm}\nNguồn: {urk}'
						item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/rakhoi.png'
						item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), linkplay, tenm)
						yield item
			else:
				yield quangcao()
		except:
			yield quangcao()