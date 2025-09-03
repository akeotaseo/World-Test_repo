from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao, stream
from datetime import datetime
@Route.register
def get_thvl(plugin, ten=None, hom=None):
	yield []
	if any((ten is None,hom is None)):
		pass
	else:
		try:
			idk_dict = {'thvl1': 'aab94d1f-44e1-4992-8633-6d46da08db42',
				'thvl2': 'bc60bddb-99ac-416e-be26-eb4d0852f5cc',
				'thvl3': 'f2ad2726-d315-4612-b78d-746721788fc8',
				'thvl4': '442692d6-c296-4835-b060-72c4cd235bd2'}
			idk = idk_dict.get(ten, None)
			url = f'http://api.thvli.vn/backend/cm/epg/?channel_id={idk}&platform=web&schedule_date={hom}'
			resp = getlink(url, url,-1)
			if (resp is not None) and ('items' in resp.text):
				ri = resp.json()['items']
				m = (k for k in ri if '.m3u8' in str(k['link_play']))
				for k in m:
					item = Listitem()
					tg = datetime.fromtimestamp(k['start_at']).strftime('%H:%M')
					tenm = f'{tg} {hom}: {k["title"]}'
					item.label = tenm
					item.info['plot'] = f'{tenm}\nNguồn: https://thvli.vn'
					item.info['mediatype'] = 'episode'
					linkplay = stream(str(k['link_play']))
					item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/lua-cho-tivi-cho-gia-dinh-1.jpg'
					item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), linkplay, tenm)
					yield item
			else:
				yield quangcao()
		except:
			yield quangcao()