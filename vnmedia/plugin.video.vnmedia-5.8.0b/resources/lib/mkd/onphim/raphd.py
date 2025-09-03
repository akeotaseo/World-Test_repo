from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao, news, qc, listqc
from bs4 import BeautifulSoup
from resolveurl import resolve
from urllib.parse import quote_plus
from codequick.utils import color
import re
@Route.register
def index_raphd(plugin):
	yield Listitem.search(ds_raphd)
	yield Listitem.from_dict(**{'label': 'Categories',
	'art': {'thumb': 'https://raw.githubusercontent.com/kenvnm/kvn/main/raphd.jpg',
	'poster': 'https://raw.githubusercontent.com/kenvnm/kvn/main/raphd.jpg'},
	'info': {'mediatype':'tvshow'},
	'callback': phanloai_raphd})
	yield Listitem.from_dict(**{'label': 'Studio',
	'art': {'thumb': 'https://raw.githubusercontent.com/kenvnm/kvn/main/raphd.jpg',
	'poster': 'https://raw.githubusercontent.com/kenvnm/kvn/main/raphd.jpg'},
	'info': {'mediatype':'tvshow'},
	'callback': studio_raphd})
	dulieu = {
	'Popular':'https://javhd.today/popular/',
	'Releaseday': 'https://javhd.today/releaseday/',
	'Recent': 'https://javhd.today/recent/',
	'Request': 'https://javhd.today/request/',
	'Uncensored':'https://javhd.today/uncensored-jav/',
	'English Sub':'https://javhd.today/eng-sub-jav/',
	'Mosaic':'https://javhd.today/reducing-mosaic/',
	'Beautiful Girl':'https://javhd.today/beautiful-girl/',
	'Big Tits':'https://javhd.today/big-tits/',
	'Creampie':'https://javhd.today/creampie/',
	'Debut':'https://javhd.today/debut-production/'}
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/raphd.jpg'
		item.set_callback(ds_raphd, dulieu[k])
		yield item
@Route.register
def phanloai_raphd(plugin):
	yield []
	try:
		url = 'https://javhd.today/categories/'
		r = getlink(url,url,400)
		if (r is not None) and ('panel-body' in r.text):
			soup = BeautifulSoup(r.text, 'html.parser')
			for k in soup.select('div.panel-body ul a'):
				item = Listitem()
				hr = k['href']
				h = f"https://javhd.today{hr}" if hr.startswith('/') else hr
				ten = k.get_text(strip=True)
				item.label = ten
				item.info['mediatype'] = 'tvshow'
				item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/raphd.jpg'
				item.set_callback(ds_raphd, h)
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def studio_raphd(plugin):
	yield []
	try:
		url = 'https://javhd.today/channels/'
		r = getlink(url,url,400)
		if (r is not None) and ('panel-body' in r.text):
			soup = BeautifulSoup(r.text, 'html.parser')
			for k in soup.select('div.panel-body ul div.video a'):
				item = Listitem()
				hr = k['href']
				h = f"https://javhd.today{hr}" if hr.startswith('/') else hr
				ten = k.get_text(strip=True)
				item.label = ten
				item.info['mediatype'] = 'tvshow'
				item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/raphd.jpg'
				item.set_callback(ds_raphd, h)
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def ds_raphd(plugin, search_query=None):
	yield []
	try:
		if '://' not in search_query:
			sr = quote_plus(search_query)
			url = f'https://javhd.today/search/video/?s={sr}'
		else:
			url = search_query
		r = getlink(url,url,400)
		if (r is not None) and ('class="videos' in r.text):
			soup = BeautifulSoup(r.text, 'html.parser')
			for k in soup.select('div.panel-body ul a.thumbnail'):
				item = Listitem()
				hr = k['href']
				ten = k['title']
				anh = k.select_one('img')['src']
				h = f"https://javhd.today{hr}" if hr.startswith('/') else hr
				item.label = ten
				item.info['mediatype'] = 'tvshow'
				item.art['thumb'] = item.art['poster'] = anh
				item.set_callback(sv_raphd, h, ten, anh)
				yield item
			if 'prevnext' in r.text:
				hr = soup.select_one('a.prevnext:contains("next")')['href']
				num = re.search(r'(\d+)', hr)[1]
				np = f"https://javhd.today{hr}" if hr.startswith('/') else hr
				item1 = Listitem()
				item1.label = f'Trang {num}'
				item1.info['mediatype'] = 'tvshow'
				item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
				item1.set_callback(ds_raphd, np)
				yield item1
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def sv_raphd(plugin, url=None, title=None, anh=None):
	yield []
	if any((url is None,title is None,anh is None)):
		pass
	else:
		try:
			resp = getlink(url, url, 400)
			if (resp is not None) and ('download-container' in resp.text):
				soup = BeautifulSoup(resp.text, 'html.parser')
				for k in soup.select('div#download-container div.btn-group button#download'):
					item = Listitem()
					ep = k['onclick']
					ten = f'{color(k.get_text(strip=True), "yellow")} - {title}'
					m = re.search(r"'(.*?)'", ep)
					item.label = ten
					item.info['mediatype'] = 'episode'
					item.art['thumb'] = item.art['poster'] = anh
					item.set_callback(play_raphd, m[1], title)
					yield item
				for k1 in soup.select('div#related ul div.video a.thumbnail'):
					item1 = Listitem()
					hr = k1['href']
					ten1 = k1['title']
					anh1 = k1.select_one('img')['src']
					h = f"https://javhd.today{hr}" if hr.startswith('/') else hr
					item1.label = ten1
					item1.info['mediatype'] = 'tvshow'
					item1.art['thumb'] = item1.art['poster'] = anh1
					item1.set_callback(sv_raphd, h, ten1, anh1)
					yield item1
			else:
				yield quangcao()
		except:
			yield quangcao()
@Resolver.register
def play_raphd(plugin, href, title):
	try:
		return listqc(title, news, resolve(href))
	except:
		return listqc(title, news, qc)