from codequick import Route, Listitem, Script, Resolver
from resources.lib.kedon import getlink, quangcao, yttk, get_info_fs, yeucau
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from concurrent.futures import ThreadPoolExecutor
from codequick.utils import color
import re
ufc = 'https://thuviencine.com'
def process_url(url):
	try:
		data = get_info_fs(url)
		return url, data
	except:
		return url, None
@Route.register
def search_thuviencine(plugin, search_query=None):
	yield []
	if search_query is None:
		pass
	else:
		try:
			resp = getlink(ufc, ufc, 1000)
			if (resp is not None):
				match = re.search(r'"nonce":"(.*?)"', resp.text)[1]
				urltv = f'{ufc}/wp-json/moviewp/search/?nonce={match}&keyword={quote_plus(search_query)}'
				r = getlink(urltv, ufc, 1000)
				if 'No results' in r.text:
					yield quangcao()
				else:
					rs = r.json().values()
					for k in rs:
						item = Listitem()
						item.label = k['title']
						item.info['plot'] = f"{k['title']}\nNguồn: {ufc}"
						item.info['mediatype'] = 'tvshow'
						item.info['trailer'] = yttk(k['title'])
						item.art['thumb'] = item.art['poster'] = k['img']
						item.set_callback(thuviencine_link, k['url'])
						yield item
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def index_thuviencine(plugin):
	yield []
	yield Listitem.search(search_thuviencine)
	yield yeucau('https://www.facebook.com/thuviencine/')
	resp = getlink(ufc, ufc, 1000)
	if (resp is not None):
		soup = BeautifulSoup(resp.text, 'html.parser')
		s1 = soup.select('div.sidebar.sb-left a')
		s2 = soup.select('nav.filters a')
		for episode in s1:
			item = Listitem()
			phim = episode['href']
			tenmm = episode.get_text(strip=True)
			item.label = tenmm
			item.info['mediatype'] = 'tvshow'
			item.info['plot'] = f"{tenmm}\nNguồn: {ufc}"
			item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/thuviencine.png'
			item.set_callback(thuviencine_page, phim, 1)
			yield item
		for nhomtheloai in s2:
			item1 = Listitem()
			nhom = nhomtheloai['href']
			tennhom = nhomtheloai.get_text(strip=True)
			if tennhom:
				item1.label = tennhom
				item1.info['mediatype'] = 'tvshow'
				item1.info['plot'] = f"{tennhom}\nNguồn: {ufc}"
				item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/thuviencine.png'
				item1.set_callback(thuviencine_page, nhom, 1)
				yield item1
	else:
		yield quangcao()
@Route.register
def thuviencine_page(plugin, url=None, next_page=None):
	yield []
	if any((url is None, next_page is None)):
		pass
	else:
		try:
			trangtiep = f'{url}page/{next_page}'
			resp = getlink(trangtiep, trangtiep, 1000)
			if (resp is not None):
				soup = BeautifulSoup(resp.text, 'html.parser')
				soups = soup.select('div.item-container a[rel="bookmark"]')
				for episode in soups:
					item = Listitem()
					anh = episode.select('img')
					ndp = episode.select('p.movie-description')
					try:
						diem = episode.select_one('div.imdb-rating').get_text(strip=True)
					except:
						diem = 'N/A'
					for inf in ndp:
						noidung = f'Điểm IMDb: {color(diem, "yellow")}\n{inf.get_text(strip=True)}'
					linkphim = episode['href']
					for poster in anh:
						linkanh = poster['data-src']
					ten = episode.select_one('h2.movie-title').get_text(strip=True)
					if ten:
						item.label = ten
						item.info['plot'] = f'{noidung}\nNguồn: {ufc}'
						item.info['mediatype'] = 'tvshow'
						item.info['trailer'] = yttk(ten)
						item.art['thumb'] = item.art['poster'] = linkanh
						item.set_callback(thuviencine_link, linkphim)
						yield item
				if 'resppages' in resp.text:
					item1 = Listitem()
					item1.label = f'Trang {next_page + 1}'
					item1.info['mediatype'] = 'tvshow'
					item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
					item1.set_callback(thuviencine_page, url, next_page + 1)
					yield item1
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def thuviencine_link(plugin, url=None):
	yield []
	if url is None:
		pass
	else:
		try:
			resp = getlink(url, url, 1000)
			if (resp is not None):
				soup = BeautifulSoup(resp.text, 'html.parser')
				us = soup.select_one('li#download-button a')['href']
				rs = getlink(us, url, 1000).text
				urls = re.findall(r'https?://(?:www\.)?fshare\.vn/(?:file|folder)/[^\s\'"]+', rs)
				length = len(urls)
				if length>0:
					with ThreadPoolExecutor(length) as ex:
						results = ex.map(process_url, urls)
					for (link, data) in results:
						if data is not None:
							item = Listitem()
							item.label = data[0]
							item.info['plot'] = f'{data[0]}\nNguồn: {ufc}'
							item.info['trailer'] = yttk(data[0])
							imgfs = 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
							item.art['thumb'] = item.art['poster'] = imgfs
							item.context.script(Script.ref('/resources/lib/mkd/onfshare/ifshare:tfavo'), 'Thêm vào Fshare Favorite', link)
							if 'folder' in link:
								item.info['mediatype'] = 'tvshow'
								item.set_callback(Route.ref('/resources/lib/mkd/onfshare/ifshare:index_fs'), link, 0, imgfs)
							else:
								item.info['mediatype'] = 'episode'
								item.info['size'] = data[1]
								if Script.setting.get_string('taifshare') == 'true':
									item.context.script(Script.ref('/resources/lib/download:downloadfs'), 'Tải về', link)
								item.set_callback(Resolver.ref('/resources/lib/kedon:play_fs'), link, data[0])
							yield item
			else:
				yield quangcao()
		except:
			yield quangcao()