from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlinkweb, quangcao
from bs4 import BeautifulSoup
from time import gmtime
from calendar import timegm
from urllib.parse import quote_plus
import re
uvgo = 'https://vtvgo.vn'
randstam = timegm(gmtime())
@Route.register
def search_vgo(plugin, search_query=None):
	yield []
	if search_query is None:
		pass
	else:
		try:
			search_query = quote_plus(search_query)
			url = f'{uvgo}/search?time={randstam}&search-keyword={search_query}'
			r = getlinkweb(url, uvgo, 900)
			if (r is not None) and ('news-slide-content-item' in r.text):
				soup = BeautifulSoup(r.text, 'html.parser')
				soups = soup.select('div.news-slide-content-item')
				length = len(soups)
				if length>0:
					for episode in soups:
						item = Listitem()
						tenm = episode.select_one('h2 a').get_text(strip=True)
						item.label = tenm
						item.info['plot'] = f'{tenm}\nNguồn: {uvgo}'
						item.info['mediatype'] = 'episode'
						linkphim = episode.select_one('h2 a')['href'].replace('.html','')
						finallink = f'{linkphim}?time={randstam}'
						item.art['thumb'] = item.art['poster'] = episode.img['src']
						item.set_callback(Resolver.ref('/resources/lib/kedon:ifr_khomuc'), finallink, tenm)
						yield item
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def index_vtvgo(plugin):
	yield Listitem.search(search_vgo)
	T = {'KHO VIDEO': index_khovd,
	'XEM TRỰC TUYẾN': list_truyenhinhvtvgo}
	for b in T:
		i = Listitem()
		i.label = b
		i.info['mediatype'] = 'tvshow'
		i.art['thumb'] = i.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/vtvgo.png'
		i.set_callback(T[b])
		yield i
@Route.register
def list_truyenhinhvtvgo(plugin):
	yield []
	try:
		kqf1 = getlinkweb(f'{uvgo}/xem-truc-tuyen?time={randstam}', uvgo, -1)
		if (kqf1 is not None):
			x = kqf1.cookies.get_dict()
			g = re.findall(r"var (time|token) = '(.*?)'", kqf1.text)
			sre = re.compile(r'\d+')
			timekenh = g[0][1]
			tokenkenh = g[1][1]
			soup = BeautifulSoup(kqf1.text, 'html.parser')
			soups = soup.select('div.list_channel a')
			for episode in soups:
				item = Listitem()
				linkkenh = episode['href']
				idkenh = sre.findall(linkkenh)[-1]
				anh = episode.img['src']
				tenm = episode['alt']
				item.label = tenm
				item.info['plot'] = f'{tenm}\nNguồn: {uvgo}'
				item.info['mediatype'] = 'episode'
				item.art['thumb'] = item.art['poster'] = anh
				item.set_callback(Resolver.ref('/resources/lib/kedon:play_vtvgo'), timekenh, tokenkenh, idkenh, x, episode['alt'])
				yield item
	except:
		yield quangcao()
@Route.register
def index_khovd(plugin):
	yield []
	try:
		url = f'{uvgo}/kho-video?time={randstam}'
		resp = getlinkweb(url, uvgo, -1)
		if (resp is not None):
			sre = re.compile(r'(\d+)\.')
			soup = BeautifulSoup(resp.text, 'html.parser')
			soups = soup.select('a.color-white')
			for episode in soups:
				item = Listitem()
				linkthumuc = episode['href']
				idthumuc = sre.search(linkthumuc)[1].replace('.', '')
				next_page = 1
				tenm = episode.get_text(strip=True)
				item.label = tenm
				item.info['plot'] = f'{tenm}\nNguồn: {uvgo}'
				item.info['mediatype'] = 'tvshow'
				item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/vtvgo.png'
				item.set_callback(list_thumucvd, idthumuc, next_page)
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def list_thumucvd(plugin, idthumuc=None, next_page=None):
	yield []
	if any((idthumuc is None,next_page is None)):
		pass
	else:
		try:
			url = f'{uvgo}/ajax-get-more-item-playlist?next_page={next_page}&channel_id={idthumuc}&time={randstam}'
			resp = getlinkweb(url, uvgo, -1)
			if (resp is not None) and ('http' in resp.text):
				soup = BeautifulSoup(resp.text, 'html.parser')
				soups = soup.select('div.swiper-slide')
				for episode in soups:
					item = Listitem()
					linkclip = episode.select_one('h2 a')['href'].replace('.html','')
					finallink = f'{linkclip}?time={randstam}'
					tenclip = episode.select_one('h2 a').get_text(strip=True)
					anhclip = episode.img['src']
					item.label = tenclip
					item.info['plot'] = f'{tenclip}\nNguồn: {uvgo}'
					item.info['mediatype'] = 'episode'
					item.art['thumb'] = item.art['poster'] = anhclip
					item.set_callback(Resolver.ref('/resources/lib/kedon:ifr_khomuc'), finallink, tenclip)
					yield item
				item1 = Listitem()
				item1.label = f'Trang {next_page + 1}'
				item1.info['mediatype'] = 'tvshow'
				item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
				item1.set_callback(list_thumucvd, idthumuc, next_page + 1)
				yield item1
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def list_vtv(plugin, tg=None, ngay=None):
	yield []
	if any((tg is None,ngay is None)):
		pass
	else:
		try:
			kqf1 = getlinkweb(f'{uvgo}/xem-truc-tuyen?time={randstam}', uvgo, -1)
			if (kqf1 is not None):
				sre = re.compile(r'\d+')
				soup = BeautifulSoup(kqf1.text, 'html.parser')
				soups = soup.select('div.list_channel a')
				for episode in soups:
					item = Listitem()
					linkkenh = episode['href']
					idkenh = sre.findall(linkkenh)[-1]
					anh = episode.img['src']
					tenm = f"{episode['alt']} - {ngay}"
					item.label = tenm
					item.info['plot'] = f'{tenm}\nNguồn: {uvgo}'
					item.info['mediatype'] = 'episode'
					item.art['thumb'] = item.art['poster'] = anh
					item.set_callback(getxl_vtvgo, idkenh, tg, anh)
					yield item
		except:
			yield []
		kenhidx = {
		'THVL1':'thvl1',
		'THVL2':'thvl2',
		'THVL3':'thvl3',
		'THVL4':'thvl4'}
		for l in kenhidx:
			item1 = Listitem()
			tenm = f'{l} - {ngay}'
			item1.label = tenm
			item1.info['plot'] = f'{tenm}\nNguồn: https://thvli.vn'
			item1.info['mediatype'] = 'tvshow'
			item1.art['thumb'] = item1.art['poster'] = 'https://img.websosanh.vn/v10/users/review/images/1yuxgbu89uqkb/lua-cho-tivi-cho-gia-dinh-1.jpg'
			item1.set_callback(Route.ref('/resources/lib/mkd/ontruyenhinh/replaythvl:get_thvl'), kenhidx[l], tg)
			yield item1
@Route.register
def getxl_vtvgo(plugin, idkenh=None, ngay=None, anh=None):
	yield []
	if any((idkenh is None,ngay is None, anh is None)):
		pass
	else:
		try:
			url = f'{uvgo}/ajax-get-list-epg?selected_date_epg={ngay}&channel_id={idkenh}&time={randstam}'
			resp = getlinkweb(url, uvgo, -1)
			if (resp is not None) and ('data-id' in resp.text):
				soup = BeautifulSoup(resp.text, 'html.parser')
				soups = soup.select('li')
				for k in soups:
					dataid = k['data-id']
					tg = k.select_one('div.col-md-3').get_text(strip=True)
					tenct1 = k.select_one('div.col-md-9 h3').get_text(strip=True)
					tenct2 = k.select_one('div.col-md-9 h4').get_text(strip=True)
					item = Listitem()
					tenm = f'{tg} {ngay} {tenct1}: {tenct2}' if tenct2 else f'{tg} {ngay} {tenct1}'
					item.label = tenm
					item.info['plot'] = f'{tenm}\nNguồn: {uvgo}'
					item.info['mediatype'] = 'episode'
					item.art['thumb'] = item.art['poster'] = anh
					item.set_callback(Resolver.ref('/resources/lib/kedon:play_xlvtvgo'), dataid, tenm)
					yield item
			else:
				yield quangcao()
		except:
			yield quangcao()