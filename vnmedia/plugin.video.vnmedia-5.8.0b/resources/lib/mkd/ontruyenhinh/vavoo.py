from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao
from requests.packages.urllib3.util import connection
from random import choice
from requests import Session
connection.HAS_IPV6 = False
uvv = 'https://vavoo.tv'
ukey = 'https://raw.githubusercontent.com/michaz1988/michaz1988.github.io/master/data.json'
def getAuthSignature():
	veclist=getlink(ukey,ukey,300).json()
	vec = {"vec": choice(veclist)}
	with Session() as s:
		try:
			req = s.post('https://www.vavoo.tv/api/box/ping2', data=vec,timeout=20).json()
		except:
			req = s.post('https://www.vavoo.tv/api/box/ping2', data=vec,timeout=20, verify=False).json()
	if req.get('signed'):
		sig = req['signed']
	elif req.get('data', {}).get('signed'):
		sig = req['data']['signed']
	elif req.get('response', {}).get('signed'):
		sig = req['response']['signed']
	return sig
@Route.register
def index_vavoo(plugin):
	yield []
	try:
		url = f'https://www2.vavoo.to/live2/index'
		resp = getlink(url, url, 1000)
		unique_groups = set()
		if (resp is not None):
			for k in resp.json():
				group = k['group']
				if group not in unique_groups:
					unique_groups.add(group)
					item = Listitem()
					tenm = group
					item.label = tenm
					item.info['plot'] = f'{tenm}\nNguồn: {uvv}'
					item.info['mediatype'] = 'tvshow'
					item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/vavoo.png'
					item.set_callback(list_vavoo, group)
					yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def list_vavoo(plugin, nhom=None):
	yield []
	try:
		if nhom is None:
			pass
		else:
			url = f'https://www2.vavoo.to/live2/index'
			resp = getlink(url, url, 1000)
			sign = getAuthSignature()
			if (resp is not None):
				for k in resp.json():
					group = k['group']
					if group == nhom:
						item = Listitem()
						name = k['name']
						logo = k['logo']
						play = k['url']
						linkplay = f'{play}?n=1&b=5&vavoo_auth={sign}|User-Agent=VAVOO/2.6'
						item.label = name
						item.info['plot'] = f'{name}\nNguồn: {uvv}'
						item.info['mediatype'] = 'episode'
						item.art['thumb'] = item.art['poster'] = logo if 'http' in logo else 'https://raw.githubusercontent.com/kenvnm/kvn/main/vavoo.png'
						item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), linkplay, name)
						yield item
			else:
				yield quangcao()
	except:
		yield quangcao()