from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao, gmt7
from bs4 import BeautifulSoup
from json import loads
import re
def getchannel(idk):
	r = getlink('https://usport.pro/channels.json', 'https://usport.pro/',-1).json()
	for k in r:
		if k['id'] == idk:
			return k['url']
@Route.register
def index_ustream(plugin):
	yield []
	try:
		resp = getlink('https://meciuri.tv/', 'https://meciuri.tv/', 400)
		if (resp is not None):
			soup = BeautifulSoup(resp.content, 'html.parser')
			soups = soup.select('div.w-full.flex.justify-between.flex-wrap.gap-4')
			for k in soups:
				item = Listitem()
				players = k.select_one('div.flex.flex-col.items-start p').get_text(strip=True)
				event_info = k.select_one('div:nth-child(2)').get_text(strip=True)
				time_str = k.select_one('astro-island')['props']
				uid = k.select_one('div:nth-child(2) astro-island')['uid']
				s = re.search(r',"(.*?)"', time_str)[1]
				tenm = f'{gmt7(s)}: {players} ({event_info})'
				item.label = tenm
				item.info['mediatype'] = 'tvshow'
				item.art['thumb'] = item.art['poster'] = 'https://mi3s.top/thumb/thethao/sports-channels.png'
				item.set_callback(list_ustream, uid, tenm)
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def list_ustream(plugin, uid=None, title=None):
	yield []
	if any((uid is None,title is None)):
		pass
	else:
		try:
			resp = getlink('https://meciuri.tv/', 'https://meciuri.tv/', 400)
			if resp is not None:
				soup = BeautifulSoup(resp.content, 'html.parser')
				props_value = soup.select_one(f"astro-island[uid='{uid}']")['props']
				props_dict = loads(props_value)
				channels_list = loads(props_dict['channels'][1])
				for k in channels_list:
					item = Listitem()
					tenm = f'{k[1]} - {title}'
					item.label = tenm
					item.info['mediatype'] = 'episode'
					item.art['thumb'] = item.art['poster'] = 'https://mi3s.top/thumb/thethao/sports-channels.png'
					item.set_callback(Resolver.ref('/resources/lib/kedon:ifr_khomuc'), getchannel(k[1]), tenm)
					yield item
			else:
				yield quangcao()
		except:
			yield quangcao()