from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from calendar import timegm
from time import strftime, strptime, mktime, gmtime, localtime
import re
bd = 'https://bongdainfo.co'
def ct(initial_time):
	struct_time = strptime(initial_time, '%Y-%m-%d %H:%M:%S')
	timestamp = mktime(struct_time) + (7 * 3600)
	new_time = strftime('%H:%M %d/%m', localtime(timestamp))
	return new_time
def get_i():
	ts = timegm(gmtime())
	return getlink(f'{bd}/gf/data/bf_vn_nt.js?{ts}', bd, 400)
def get_l():
	return getlink(f'https://tvlive.vbfast.xyz/tvlive_vn_fb.txt', bd, 400)
def inf():
	with ThreadPoolExecutor(2) as ex:
		f1 = ex.submit(get_i)
		f2 = ex.submit(get_l)
	return (f1.result(),f2.result())
@Route.register
def index_91phut(plugin):
	yield []
	try:
		resp1, resp2 = inf()
		if (resp2 is not None):
			ids = re.findall(r'[$|!](\d+)', resp2.text)
			r1 = resp1.text
			for k in ids:
				try:
					m = re.search(rf"{k}.*?'(.*?)'.*?'(.*?)'.*?'(.*?)'", r1)
					ten = f'{ct(m[3])}: {m[1]} vs {m[2]}'
					item = Listitem()
					item.label = ten
					item.info['plot'] = f'{ten}\nNguồn: {bd}'
					item.info['mediatype'] = 'tvshow'
					item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/mitom.png'
					item.set_callback(list_91phut, k, ten)
					yield item
				except:
					pass
		else:
			yield quangcao()
	except:
		pass
@Route.register
def list_91phut(plugin, k=None, title=None):
	yield []
	if any((k is None,title is None)):
		pass
	else:
		try:
			r = getlink('https://tvlive.vbfast.xyz/tvlive_vn_fb.txt',bd,400)
			if (r is not None) and (k in r.text):
				match = re.search(rf'{k}(.*?)\!', r.text)
				urls = re.findall(r'(https://.*?)\^', match[1])
				for dem, k in enumerate(urls, start=1):
					ten = f'Sv{dem} - {title}'
					item = Listitem()
					item.label = ten
					item.info['plot'] = f'{ten}\nNguồn: {bd}'
					item.info['mediatype'] = 'tvshow'
					item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/mitom.png'
					item.set_callback(sv_91phut, k, ten)
					yield item
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def sv_91phut(plugin, url=None, title=None):
	yield []
	if any((url is None,title is None)):
		pass
	else:
		try:
			resp = getlink(url, url, 400)
			if (resp is not None):
				if 'link-video' in resp.text:
					soup = BeautifulSoup(resp.text, 'html.parser')
					for k in soup.select('div.link-video a'):
						ten = f'{k.get_text(strip=True)} - {title}'
						ep = k['href']
						item = Listitem()
						item.label = ten
						item.info['plot'] = f'{ten}\nNguồn: {bd}'
						item.info['mediatype'] = 'episode'
						item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/mitom.png'
						item.set_callback(Resolver.ref('/resources/lib/kedon:ifr_bongda'), ep, ten)
						yield item
				elif 'tv_links' in resp.text:
					soup = BeautifulSoup(resp.text, 'html.parser')
					for k in soup.select('div#tv_links a'):
						ten = f'{k.get_text(strip=True)} - {title}'
						ep = k['href']
						item = Listitem()
						item.label = ten
						item.info['plot'] = f'{ten}\nNguồn: {bd}'
						item.info['mediatype'] = 'episode'
						item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/mitom.png'
						item.set_callback(Resolver.ref('/resources/lib/kedon:ifr_bongda'), ep, ten)
						yield item
				else:
					item = Listitem()
					item.label = title
					item.info['plot'] = f'{title}\nNguồn: {bd}'
					item.info['mediatype'] = 'episode'
					item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/mitom.png'
					item.set_callback(Resolver.ref('/resources/lib/kedon:ifr_bongda'), url, title)
					yield item
			else:
				yield quangcao()
		except:
			yield quangcao()