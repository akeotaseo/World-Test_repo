from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, stream, referer, quangcao
from codequick.utils import color
from itertools import chain
import re
uck = 'https://cakhiaz.link'
@Route.register
def index_cakhia(plugin):
	yield []
	try:
		u = 'https://api.rkdata.xyz/v1/cakhia/home.html'
		r = getlink(u,u, 400)
		if (r is not None):
			kq = r.json()['data']
			m = chain.from_iterable(kq.values())
			for k in m:
				try:
					time = k['timeShort']
					home = k['home']['name']
					away = k['away']['name']
					blv = k['blv']['name']
					tg = color(time, 'red') if k['status']==1 else time
					mau = color(f'{home} vs {away}', 'yellow')
					tenm = f'{tg} {mau} - {blv}' if blv else f'{tg} {home} vs {away}'
					item = Listitem()
					item.label = tenm
					item.info['plot'] = f'{tenm}\nNguồn: {uck}'
					item.info['mediatype'] = 'tvshow'
					item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/cakhia.png'
					item.set_callback(list_cakhia, k['id'], tenm)
					yield item
				except:
					pass
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def list_cakhia(plugin, idck=None, tentran=None):
	yield []
	if any((idck is None,tentran is None)):
		pass
	else:
		try:
			u = f'https://watch.rkplayer.xyz/v1/cakhia/{idck}.html'
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
						item.info['plot'] = f'{tenm}\nNguồn: {uck}'
						item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/cakhia.png'
						item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), linkplay, tenm)
						yield item
			else:
				yield quangcao()
		except:
			yield quangcao()