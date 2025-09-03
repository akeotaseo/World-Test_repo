from codequick import Route, Listitem
from resources.lib.kedon import getlink, ace, quangcao
from datetime import datetime, timedelta
from json import loads
import re
@Route.register
def index_streamthunder(plugin):
	yield []
	try:
		url = 'http://widget.streamthunder.org/list.php?id=21&sport=&sp=&r=&l=&l2='
		resp = getlink(url, url, 400)
		if (resp is not None) and ('acestream' in resp.text):
			m1 = loads(re.search(r'var chan_arr = (.*?);\n', resp.text)[1])
			m2 = loads(re.search(r'var ev_arr = (.*?);\n', resp.text)[1])
			a1, a2 = (((m,x['link'], a) for m in m1 for a, x in enumerate(m1[m]) if 'acestream' in x['link']),((v['id'], v['date'], v['match']) for v in m2))
			listm = ((l,k) for k in a1 for l in a2 if k[0] == l[0])
			for l, k in listm:
				item = Listitem()
				z = (datetime.fromisoformat(l[1]) + timedelta(hours=6)).strftime('%H:%M')
				tenm = f'Link {k[2]+1}-{z} {l[2]}'
				item.label = tenm
				item.info['plot'] = f'{tenm}\nNguồn: https://streamthunder.org'
				item.info['mediatype'] = 'episode'
				item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/acestream.png'
				item.set_callback(ace(k[1], tenm))
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()