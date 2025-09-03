from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao, headersnct
from requests.packages.urllib3.util import connection
from bs4 import BeautifulSoup
from requests import Session
import re
connection.HAS_IPV6 = False
unct = 'http://nhaccuatui.com'
@Route.register
def index_amnhac(plugin):
	T = {'Bài hát': index_baihat,
	'Playlist': index_playlist,
	'Tuyển tập': index_tuyentap,
	'Video': index_video,
	'Bảng xếp hạng': index_bxhvn,
	'Chủ đề': index_chude,
	'TOP 100': index_top,
	'Nghe gì': nghegi}
	yield Listitem.youtube('PL4fGSI1pDJn5kI81J1fYWK5eZRl1zJ5kM',label="TOP 100 thế giới")
	for k in T:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/amnhac.png'
		item.set_callback(T[k])
		yield item
	yield videomusic()
@Route.register
def index_baihat(plugin):
	yield []
	try:
		ubaihat = f'{unct}/bai-hat/bai-hat-moi.html'
		r = getlink(ubaihat, unct,-1)
		if r is not None:
			soup = BeautifulSoup(r.text, 'html.parser')
			soups = soup.select('div.box_cata_control ul li a')
			ls = ((l.text, l['href']) for l in soups if 'href' in l.attrs)
			i = Listitem()
			i.label = 'Mới nhất'
			i.info['plot'] = f'Mới nhất\nNguồn: {unct}'
			i.info['mediatype'] = 'tvshow'
			i.art['thumb'] = i.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/amnhac.png'
			i.set_callback(listbai_nct, ubaihat)
			yield i
			for k in ls:
				item = Listitem()
				item.label = k[0]
				item.info['mediatype'] = 'tvshow'
				item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/amnhac.png'
				item.set_callback(listbai_nct, k[1])
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def nghegi(plugin):
	yield []
	try:
		with Session() as s:
			r = s.get('https://graph.nhaccuatui.com/api/v1/song/feed', timeout=15,headers=headersnct)
		if r is not None:
			rl = r.json()['data']['list']
			for k in rl:
				item = Listitem()
				item.label = k['name']
				item.info['plot'] = f'{k["name"]}\nNguồn: {unct}'
				item.info['mediatype'] = 'episode'
				item.art['thumb'] = item.art['poster'] = k['image']
				item.set_path(k['streamURL'][-1]['stream'])
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def index_playlist(plugin):
	yield []
	try:
		uplaylist = f'{unct}/playlist/playlist-moi.html'
		r = getlink(uplaylist, unct,-1)
		if r is not None:
			i = Listitem()
			i.label = 'Mới nhất'
			i.info['plot'] = f'Mới nhất\nNguồn: {unct}'
			i.info['mediatype'] = 'tvshow'
			i.art['thumb'] = i.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/amnhac.png'
			i.set_callback(albumplaylist_nct, uplaylist)
			yield i
			soup = BeautifulSoup(r.text, 'html.parser')
			soups = soup.select('div.box_cata_control ul li a')
			sl = ((l.text, l['href']) for l in soups if 'href' in l.attrs)
			for k in sl:
				item = Listitem()
				item.label = k[0]
				item.info['plot'] = f'{k[0]}\nNguồn: {unct}'
				item.info['mediatype'] = 'tvshow'
				item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/amnhac.png'
				item.set_callback(albumplaylist_nct, k[1])
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def index_tuyentap(plugin):
	yield []
	try:
		utuyentap = f'{unct}/playlist/tags'
		r = getlink(utuyentap, unct,-1)
		if r is not None:
			i = Listitem()
			i.label = 'Mới nhất'
			i.info['plot'] = f'Mới nhất\nNguồn: {unct}'
			i.info['mediatype'] = 'tvshow'
			i.art['thumb'] = i.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/amnhac.png'
			i.set_callback(tuyentapplaylist_nct, utuyentap)
			yield i
			soup = BeautifulSoup(r.text, 'html.parser')
			soups = soup.select('div.box_menu_tag')
			sl = ((k.h3.get_text(strip=True), l.get_text(strip=True),l['href']) for k in soups for l in k.select('a'))
			for k in sl:
				item = Listitem()
				item.label = f'{k[0]}: {k[1]}'
				item.info['plot'] = f'{k[0]}: {k[1]}\nNguồn: {unct}'
				item.info['mediatype'] = 'tvshow'
				item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/amnhac.png'
				item.set_callback(tuyentapplaylist_nct, k[2])
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def index_video(plugin):
	yield []
	try:
		r = getlink(f'{unct}/video.html', unct,-1)
		if r is not None:
			soup = BeautifulSoup(r.text, 'html.parser')
			soups = soup.select('div.box_cata_control ul li a')
			sl = ((l.text, l['href']) for l in soups if 'href' in l.attrs)
			for k in sl:
				item = Listitem()
				item.label = k[0]
				item.info['plot'] = f'{k[0]}\nNguồn: {unct}'
				item.info['mediatype'] = 'tvshow'
				item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/amnhac.png'
				item.set_callback(videoplaylist_nct, k[1])
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def index_bxhvn(plugin):
	yield []
	try:
		r = getlink(f'{unct}/bai-hat/top-20.nhac-viet.html', unct,-1)
		if r is not None:
			soup = BeautifulSoup(r.text, 'html.parser')
			soups = soup.select('ul.search_control_select a')
			for k in soups:
				item = Listitem()
				tenm = k.get_text(strip=True)
				item.label = tenm
				item.info['plot'] = f'{tenm}\nNguồn: {unct}'
				item.info['mediatype'] = 'tvshow'
				item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/amnhac.png'
				item.set_callback(bxhplaylist_nct, k['href'])
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def index_chude(plugin):
	yield []
	try:
		r = getlink(f'{unct}/chu-de.html', unct,-1)
		if r is not None:
			soup = BeautifulSoup(r.text, 'html.parser')
			soups = soup.select('div.fram_select a.name_song')
			for k in soups:
				item = Listitem()
				item.info['mediatype'] = 'tvshow'
				tenm = k.get_text(strip=True)
				item.label = tenm
				item.info['plot'] = f'{tenm}\nNguồn: {unct}'
				item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/1792312.jpg'
				item.set_callback(playlist_nct, k['href'])
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def index_top(plugin):
	yield []
	M = {'Việt Nam': f'{unct}/top100/top-100-nhac-tre.m3liaiy6vVsF.html',
	'Âu Mỹ': f'{unct}/top100/top-100-pop.zE23R7bc8e9X.html',
	'Châu Á': f'{unct}/top100/top-100-nhac-han.iciV0mD8L9Ed.html',
	'Không lời': f'{unct}/top100/top-100-khong-loi.kr9KYNtkzmnA.html'}
	for k in M:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/amnhac.png'
		item.set_callback(index_top100, M[k])
		yield item
@Route.register
def index_top100(plugin, url=None):
	yield []
	if url is None:
		pass
	else:
		try:
			r = getlink(url,url,-1)
			if r is not None:
				soup = BeautifulSoup(r.text, 'html.parser')
				soups = soup.select('ul.detail_menu_browsing_dashboard a')
				for k in soups:
					item = Listitem()
					tenm = k.get_text(strip=True)
					item.label = tenm
					item.info['plot'] = f'{tenm}\nNguồn: {unct}'
					item.info['mediatype'] = 'tvshow'
					item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/amnhac.png'
					item.set_callback(playlist_nct, k['href'])
					yield item
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def playlist_nct(plugin, url=None):
	yield []
	if url is None:
		pass
	else:
		try:
			idk = re.search(r"(?<=\.)([\w-]+)(?=\.\w+$)", url)
			if idk:
				with Session() as s:
					r = s.get(f'https://graph.nhaccuatui.com/api/v1/playlist/detail/{idk[1]}', headers=headersnct,timeout=15)
				rl = r.json()['data']['listSong']
				for k in rl:
					item = Listitem()
					tenm = k['name']
					item.label = tenm
					item.info['plot'] = f'{tenm}\nNguồn: {unct}'
					item.info['mediatype'] = 'episode'
					item.art['thumb'] = item.art['poster'] = k['image']
					item.set_path(k['streamURL'][-1]['stream'])
					yield item
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def albumplaylist_nct(plugin, url=None):
	yield []
	if url is None:
		pass
	else:
		try:
			r = getlink(url,url,-1)
			if r is not None:
				soup = BeautifulSoup(r.text, 'html.parser')
				g = soup.select('div.fram_select ul li')
				if g:
					for k in g:
						item = Listitem()
						a = k.select_one('div.info_album a')
						tenm = a.get_text(strip=True)
						item.label = tenm
						item.info['plot'] = f'{tenm}\nNguồn: {unct}'
						item.info['mediatype'] = 'tvshow'
						item.art['thumb'] = item.art['poster'] = k.img['data-src']
						item.set_callback(playlist_nct, a['href'])
						yield item
					page = soup.select('div.box_pageview')
					if page:
						for k in page:
							i = Listitem()
							a = k.select_one('a[rel="next"]')
							i.label = f'Trang {a.get_text(strip=True)}'
							i.info['mediatype'] = 'tvshow'
							i.art['thumb'] = i.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
							i.set_callback(albumplaylist_nct, a['href'])
							yield i
				else:
					yield quangcao()
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def tuyentapplaylist_nct(plugin, url=None):
	yield []
	if url is None:
		pass
	else:
		try:
			r = getlink(url,url,-1)
			if r is not None:
				soup = BeautifulSoup(r.text, 'html.parser')
				g = soup.select('div.list_album.tag ul li')
				if g:
					for k in g:
						item = Listitem()
						a = k.select_one('div.info_album a')
						tenm = a.get_text(strip=True)
						item.label = tenm
						item.info['plot'] = f'{tenm}\nNguồn: {unct}'
						item.info['mediatype'] = 'tvshow'
						item.art['thumb'] = item.art['poster'] = k.img['data-src']
						item.set_callback(playlist_nct, a['href'])
						yield item
					page = soup.select('div.box_pageview')
					if page:
						for k in page:
							i = Listitem()
							a = k.select_one('a[rel="next"]')
							i.label = f'Trang {a.get_text(strip=True)}'
							i.info['mediatype'] = 'tvshow'
							i.art['thumb'] = i.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
							i.set_callback(tuyentapplaylist_nct, a['href'])
							yield i
				else:
					yield quangcao()
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def videoplaylist_nct(plugin, url=None):
	yield []
	if url is None:
		pass
	else:
		try:
			r = getlink(url,url,-1)
			if r is not None:
				soup = BeautifulSoup(r.text, 'html.parser')
				g = soup.select('div.list_video ul li')
				if g:
					for k in g:
						a = k.select_one('a.name_song')
						item = Listitem()
						tenm = a.get_text(strip=True)
						item.label = tenm
						item.info['plot'] = f'{tenm}\nNguồn: {unct}'
						item.info['mediatype'] = 'episode'
						item.art['thumb'] = item.art['poster'] = k.img['data-src']
						item.set_callback(Resolver.ref('/resources/lib/kedon:playvdnct'), a['href'], tenm)
						yield item
					page = soup.select('div.box_pageview')
					if page:
						for k in page:
							i = Listitem()
							a = k.select_one('a[rel="next"]')
							i.label = f'Trang {a.get_text(strip=True)}'
							i.info['mediatype'] = 'tvshow'
							i.art['thumb'] = i.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
							i.set_callback(videoplaylist_nct, a['href'])
							yield i
				else:
					yield quangcao()
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def bxhplaylist_nct(plugin, url=None):
	yield []
	if url is None:
		pass
	else:
		try:
			idk = re.search(r"(?<=\.)([\w-]+)(?=\.\w+$)", url)
			if idk:
				with Session() as s:
					r = s.get(f'https://graph.nhaccuatui.com/api/v1/playlist/charts/{idk[1]}', headers=headersnct,timeout=15)
				ri = r.json()['data']['items']
				for k in ri:
					item = Listitem()
					tenm = k['name']
					item.label = tenm
					item.info['plot'] = f'{tenm}\nNguồn: {unct}'
					item.info['mediatype'] = 'episode'
					item.art['thumb'] = item.art['poster'] = k['image']
					item.set_callback(Resolver.ref('/resources/lib/kedon:playnct'), k['linkShare'], k['name'])
					yield item
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def listbai_nct(plugin, url=None):
	yield []
	if url is None:
		pass
	else:
		try:
			r = getlink(url,url,-1)
			if r is not None:
				soup = BeautifulSoup(r.text, 'html.parser')
				g = soup.select('div.info_song a.avatar_song')
				if g:
					for k in g:
						item = Listitem()
						tenm = k['title']
						item.label = tenm
						item.info['plot'] = f'{tenm}\nNguồn: {unct}'
						item.info['mediatype'] = 'episode'
						item.art['thumb'] = item.art['poster'] = k.img['src']
						item.set_callback(Resolver.ref('/resources/lib/kedon:playnct'), k['href'], k['title'])
						yield item
					page = soup.select('div.box_pageview')
					if page:
						for k in page:
							i = Listitem()
							a = k.select_one('a[rel="next"]')
							i.label = f'Trang {a.get_text(strip=True)}'
							i.info['mediatype'] = 'tvshow'
							i.art['thumb'] = i.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
							i.set_callback(listbai_nct, a['href'])
							yield i
				else:
					yield quangcao()
			else:
				yield quangcao()
		except:
			yield quangcao()
def videomusic():
	item = Listitem()
	item.label = 'Video nhạc tổng hợp'
	item.info['mediatype'] = 'tvshow'
	item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/amnhac.png'
	item.set_callback(Route.ref('/resources/lib/mkd/ontintuc/mocha:index_mocha'), 4, 0)
	return item