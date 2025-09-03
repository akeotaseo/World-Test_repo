from codequick import Route, Listitem, Resolver
from resources.lib.kedon import useragentdf, quangcao, stream, getlink, referer
from requests.packages.urllib3.util import connection
from requests import Session
from json import dumps
from datetime import datetime, timedelta
from codequick.utils import color
connection.HAS_IPV6 = False
ugv = 'https://tructiep1.gavang1.live/'
@Route.register
def index_gavang(plugin):
	yield []
	try:
		u = 'https://api.gavangtv.tech/schedules/graph'
		data = {'limit': 100,'page': 1,'order_asc':'schedule','queries': [{'field': 'is_live','type': 'equal','value': True}]}
		with Session() as s:
			try:
				r = s.post(u, timeout=20, data=dumps(data), headers={'user-agent': useragentdf, 'referer': u.encode('utf-8')})
			except:
				r = s.post(u, timeout=20, data=dumps(data), headers={'user-agent': useragentdf, 'referer': u.encode('utf-8')}, verify=False)
		if r is not None:
			rd = r.json()['data']
			for k in r.json()['data']:
				time = (datetime.fromisoformat(k['schedule']) + timedelta(hours=7)).strftime('%H:%M %d/%m')
				blv = k['commentator']
				team_1 = k['team_1']
				team_2 = k['team_2']
				ten = f'{time}: {team_1} - {team_2}'
				item = Listitem()
				tenm = color(f'{ten} ({blv})', 'yellow') if blv is not None else ten
				item.label = tenm
				item.info['plot'] = f'{tenm}\nNguồn: {ugv}'
				item.info['mediatype'] = 'tvshow'
				item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/gavang.png'
				item.set_callback(list_gavang, k['stream_key'], tenm)
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def list_gavang(plugin, idk=None, title=None):
	yield []
	if any((idk is None,title is None)):
		pass
	else:
		try:
			u = f'https://api.gavangtv.tech/stream/{idk}/live'
			r = getlink(u,u,-1)
			if (r is not None) and ('data' in r.text):
				for key, value in r.json()['data'].items():
					if value is not None and 'http' in value:
						item = Listitem()
						tenm = f'{key.upper()} - {title}'
						linkplay = f'{stream(value)}{referer(ugv)}'
						item.label = tenm
						item.info['plot'] = f'{tenm}\nNguồn: {ugv}'
						item.info['mediatype'] = 'episode'
						item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/gavang.png'
						item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), linkplay, tenm)
						yield item
			else:
				yield quangcao()
		except:
			yield quangcao()