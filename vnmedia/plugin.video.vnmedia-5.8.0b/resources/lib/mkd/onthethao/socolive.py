from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao
from json import loads
from datetime import datetime
from calendar import timegm
from time import gmtime
from codequick.utils import color
import re
usc = 'http://bit.ly/socolive'
@Route.register
def index_socolive(plugin):
	yield []
	yield Listitem.from_dict(**{'label': 'EVENT',
	'art': {'thumb': 'https://raw.githubusercontent.com/kenvnm/kvn/main/soco.png',
	'poster': 'https://raw.githubusercontent.com/kenvnm/kvn/main/soco.png'},
	'callback': live_socolive})
	timestamp = timegm(gmtime())
	url = f'https://json.vnres.co/matches.json?v={timestamp}'
	resp = getlink(url, url, 400)
	if (resp is not None):
		nd = re.search(r'(\{.*\})', resp.text, re.DOTALL)[1]
		m = loads(nd)
		mh = m['data']['0']
		for k in mh:
			tg = datetime.fromtimestamp(int(k['matchTime'])/1000).strftime('%H:%M %d/%m')
			item = Listitem()
			tenm = f"{tg} {k['hostName']} vs {k['guestName']}"
			item.label = tenm
			item.info['plot'] = f'{tenm}\nNguồn: {usc}'
			item.info['mediatype'] = 'tvshow'
			item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/soco.png'
			item.set_callback(room_soco, k['scheduleId'], tenm, timestamp)
			yield item
	else:
		yield quangcao()
@Route.register
def room_soco(plugin, roomnum=None, title=None, timestamp=None):
	yield []
	if any((roomnum is None,title is None,timestamp is None)):
		pass
	else:
		try:
			url = f'https://json.vnres.co/matches.json?v={timestamp}'
			resp = getlink(url, url, 400)
			if (resp is not None):
				nd = re.search(r'(\{.*\})', resp.text, re.DOTALL)[1]
				m = loads(nd)
				mh = m['data']['0']
				v = ((l['nickName'], l['icon'], l['anchor']['roomNum']) for k in mh for l in k['anchors'] if k['scheduleId'] == roomnum)
				for k in v:
					tenm = f'{title} {color(k[0], "yellow")}'
					item = Listitem()
					item.label = tenm
					item.info['plot'] = f'{tenm}\nNguồn: {usc}'
					item.info['mediatype'] = 'episode'
					item.art['thumb'] = item.art['poster'] = k[1]
					item.set_callback(Resolver.ref('/resources/lib/kedon:playsocolive'), k[2], timestamp, tenm)
					yield item
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def live_socolive(plugin):
	yield []
	try:
		timestamp = timegm(gmtime())
		url = f'http://json.vnres.co/all_live_rooms.json?v={timestamp}'
		resp = getlink(url, url, 400)
		if (resp is not None):
			nd = re.search(r'(\{.*\})', resp.text, re.DOTALL)[1]
			m = loads(nd)
			mh = m['data']['hot']
			for k in mh:
				item = Listitem()
				tenm = f'{k["title"]} ({k["anchor"]["nickName"]})'
				item.label = tenm
				item.info['plot'] = f'{k["notice"]}\nNguồn: {usc}'
				item.info['mediatype'] = 'episode'
				item.art['thumb'] = item.art['poster'] = k['cover']
				item.set_callback(Resolver.ref('/resources/lib/kedon:playsocolive'), k['roomNum'], timestamp, tenm)
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()