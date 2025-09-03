from codequick import Route, Listitem, Resolver, Script
from resources.lib.kedon import getlink, quangcao, gmt7
from codequick.utils import color
from bs4 import BeautifulSoup
import re
dlhd = 'https://dlhd.sx'
@Route.register
def index_daddy(plugin):
	yield []
	try:
		url = f'{dlhd}/schedule/schedule-generated.json'
		resp = getlink(url, url, 400)
		if (resp is not None):
			for k,l in resp.json().items():
				for n,m in l.items():
					item = Listitem()
					item.label = f'{n} - {k}'
					item.info['mediatype'] = 'tvshow'
					item.art['thumb'] = item.art['poster'] = 'https://mi3s.top/thumb/thethao/daddy-live-hd-channels-list.png'
					item.set_callback(list_daddy, n, k)
					yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def all_daddy(plugin):
	yield []
	try:
		url = f'{dlhd}/24-7-channels.php'
		resp = getlink(url, url, 400)
		if (resp is not None):
			soup = BeautifulSoup(resp.content, 'html.parser')
			sre = re.compile(r'-(\d+)\.')
			for k in soup.select('div.grid-item a'):
				link = k['href']
				tenm = k.get_text(strip=True)
				if '-' in link:
					idk = sre.search(link)
					link = f'{dlhd}/embed/stream-{idk[1]}.php'
					if Script.setting.get_string('kenh18') == 'true':
						item = Listitem()
						item.info['mediatype'] = 'episode'
						item.label = tenm
						item.art['thumb'] = item.art['poster'] = 'https://mi3s.top/thumb/thethao/daddy-live-hd-channels-list.png'
						item.set_callback(Resolver.ref('/resources/lib/kedon:ifr_bongda'), link, tenm)
						yield item
					else:
						if '18+' not in tenm:
							item = Listitem()
							item.info['mediatype'] = 'episode'
							item.label = tenm
							item.art['thumb'] = item.art['poster'] = 'https://mi3s.top/thumb/thethao/daddy-live-hd-channels-list.png'
							item.set_callback(Resolver.ref('/resources/lib/kedon:ifr_bongda'), link, tenm)
							yield item
	except:
		yield quangcao()
@Route.register
def list_daddy(plugin, a=None, b=None):
	yield []
	if any((a is None,b is None)):
		pass
	else:
		try:
			url = f'{dlhd}/schedule/schedule-generated.json'
			resp = getlink(url, url, 400)
			if (resp is not None):
				c = resp.json()[b][a]
				for k in c:
					tg = gmt7(k['time'])
					item = Listitem()
					item.info['mediatype'] = 'tvshow'
					tenm = f'{tg}: {k["event"]}'
					item.label = tenm
					item.art['thumb'] = item.art['poster'] = 'https://mi3s.top/thumb/thethao/daddy-live-hd-channels-list.png'
					item.set_callback(channel_daddy, a, b, k["event"], tenm)
					yield item
		except:
			yield quangcao()
@Route.register
def channel_daddy(plugin, a=None, b=None, event=None, tentran=None):
	yield []
	if any((a is None,b is None,event is None,tentran is None)):
		pass
	else:
		try:
			url = f'{dlhd}/schedule/schedule-generated.json'
			resp = getlink(url, url, 400)
			if (resp is not None):
				c = resp.json()[b][a]
				for k in c:
					for m in k['channels']:
						if k['event'] == event:
							tenkenh = color(m['channel_name'], 'yellow')
							idkenh = m['channel_id']
							link = f'{dlhd}/embed/stream-{idkenh}.php'
							item = Listitem()
							item.info['mediatype'] = 'episode'
							tenm = f'{tenkenh} {tentran}'
							item.label = tenm
							item.art['thumb'] = item.art['poster'] = 'https://mi3s.top/thumb/thethao/daddy-live-hd-channels-list.png'
							item.set_callback(Resolver.ref('/resources/lib/kedon:ifr_bongda'), link, tenm)
							yield item
		except:
			yield quangcao()