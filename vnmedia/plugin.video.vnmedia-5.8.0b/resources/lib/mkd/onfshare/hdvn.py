from codequick import Route, Listitem, Resolver, Script
from bs4 import BeautifulSoup
from resources.lib.kedon import getlink, fu, yttk, quangcao, get_info_fs
from resources.lib.mkd.onfshare.ifshare import hdvn, likehdvn, loginfhdvn, tkhdvn
from concurrent.futures import ThreadPoolExecutor
from codequick.utils import keyboard
from urllib.parse import quote_plus
import re
def is_not_number(a):
	if not a.isdigit():
		return True
	else:
		return False
def get_info_hdvn(x):
	r = getlink(x,x,-1)
	try:
		soup = BeautifulSoup(r.text, 'html.parser')
		ten = soup.title.get_text(strip=True)
		try:
			anh = soup.select_one('img.bbCodeImage')['src']
		except:
			anh = 'https://raw.githubusercontent.com/kenvnm/kvn/main/thuvienhd.png'
		try:
			soups = soup.select_one('div.messageContent').text.split('\n')
			line = (line for line in soups if line.strip())
			nd = '\n'.join(line)
		except:
			nd = ten
		return (ten, anh, nd)
	except:
		return None
def process_url(url):
	try:
		data = get_info_hdvn(url)
		return url, data
	except:
		return url, None
def process_fs(url):
	try:
		data = get_info_fs(url)
		return url, data
	except:
		return url, None
@Route.register
def search_hdvn(plugin, search_query=None):
	yield []
	if search_query is None:
		pass
	else:
		try:
			s_query = quote_plus(search_query)
			r = tkhdvn(s_query)
			if (r is not None) and ('titleText' in r.text) and ('pageNavHeader' in r.text):
				soup = BeautifulSoup(r.text, 'html.parser')
				tongtrang = re.findall(r"\d+", soup.select_one('span.pageNavHeader').get_text(strip=True))[-1]
				soups = soup.select('div.titleText a')
				urls = [f"{hdvn}/{episode['href']}" for episode in soups if 'titleText' in r.text]
				length = len(urls)
				if length>0:
					idsearch = re.search(r'search/([0-9]+)', r.url)[1]
					with ThreadPoolExecutor(length) as ex:
						results = ex.map(process_url, urls)
					for (l, data) in results:
						if data is not None:
							item = Listitem()
							item.label = data[0]
							item.info['plot'] = f'{data[2]}\nNguồn: {hdvn}'
							item.info['mediatype'] = 'tvshow'
							item.info['trailer'] = yttk(data[0])
							item.art['thumb'] = item.art['poster'] = data[1]
							item.set_callback(hdvn_link, l)
							yield item
					if '>Tiếp' in r.text:
						item1 = Listitem()
						item1.label = f'Trang 2/{tongtrang}'
						item1.info['mediatype'] = 'tvshow'
						item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/nexthdvn.png'
						item1.set_callback(search_hdvnnext, s_query, str('2'), idsearch)
						yield item1
					yield tktrangmoi(search_query, idsearch)
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def search_hdvnnext(plugin, sr=None, next_page=None, idsearch=None):
	yield []
	if any((sr is None, next_page is None, idsearch is None)):
		pass
	else:
		try:
			url = f'{hdvn}/search/{idsearch}/?page={next_page}&q={sr}&o=date'
			r = getlink(url, url, 7200)
			if (r is not None) and ('titleText' in r.text) and ('pageNavHeader' in r.text):
				soup = BeautifulSoup(r.text, 'html.parser')
				tongtrang = re.findall(r"\d+", soup.select_one('span.pageNavHeader').get_text(strip=True))[-1]
				soups = soup.select('div.titleText a')
				urls = [f"{hdvn}/{episode['href']}" for episode in soups if 'titleText' in r.text]
				length = len(urls)
				if length>0:
					with ThreadPoolExecutor(length) as ex:
						results = ex.map(process_url, urls)
					for (l, data) in results:
						if data is not None:
							item = Listitem()
							item.label = data[0]
							item.info['plot'] = f'{data[2]}\nNguồn: {hdvn}'
							item.info['mediatype'] = 'tvshow'
							item.info['trailer'] = yttk(data[0])
							item.art['thumb'] = item.art['poster'] = data[1]
							item.set_callback(hdvn_link, l)
							yield item
					if '>Tiếp' in r.text:
						item1 = Listitem()
						item1.label = f'Trang {str(int(next_page) + 1)}/{tongtrang}'
						item1.info['mediatype'] = 'tvshow'
						item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/nexthdvn.png'
						item1.set_callback(search_hdvnnext, sr, str(int(next_page) + 1), idsearch)
						yield item1
					yield tktrangmoi(sr, idsearch)
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def index_hdvn(plugin):
	H = {
	'4K': f'{hdvn}/forums/4k.337/',
	'WEB-DL, HDTV 4K': f'{hdvn}/forums/web-dl-hdtv-4k.344/',
	'Bluray Remux 4K': f'{hdvn}/forums/bluray-remux-4k.345/',
	'Bluray Nguyên Gốc 4K': f'{hdvn}/forums/bluray-nguyen-goc-4k.346/',
	'Fshare.vn': f'{hdvn}/forums/fshare-vn.33/',
	'Fshare-WEB-DL, HDTV': f'{hdvn}/forums/web-dl-hdtv.271/',
	'Fshare-Bluray Remux': f'{hdvn}/forums/bluray-remux.324/',
	'Fshare-mHD, SD': f'{hdvn}/forums/mhd-sd.77/',
	'Fshare-Bluray nguyên gốc': f'{hdvn}/forums/bluray-nguyen-goc.78/',
	'Thư viện link Phim': f'{hdvn}/forums/thu-vien-link-phim.150/',
	'Phim có audio Việt': f'{hdvn}/forums/phim-co-audio-viet.265/',
	'Phim bộ - Series': f'{hdvn}/forums/phim-bo-series.57/',
	'Phim bộ - mHD, SD': f'{hdvn}/forums/mhd-sd.104/',
	'Phim hoạt hình': f'{hdvn}/forums/phim-hoat-hinh.123/',
	'Phim hoạt hình - mHD, SD': f'{hdvn}/forums/mhd-sd.124/',
	'Phim tài liệu - Documentaries': f'{hdvn}/forums/phim-tai-lieu-documentaries.116/',
	'Phim 3D': f'{hdvn}/forums/3d.110/',
	'Phim cho iOS/Android': f'{hdvn}/forums/phim-cho-ios-android.157/',
	'Music request': f'{hdvn}/forums/music-request.28/',
	'HD Video Clip': f'{hdvn}/forums/hd-video-clip.50/',
	'Video nhạc US-EU': f'{hdvn}/forums/us-eu.189/',
	'Video nhạc Việt Nam': f'{hdvn}/forums/viet-nam.191/',
	'Video nhạc Asia': f'{hdvn}/forums/asia.190/',
	'Soundtrack': f'{hdvn}/forums/soundtrack.73/',
	'Lossless Albums': f'{hdvn}/forums/lossless-albums.26/',
	'Lossless Việt Nam': f'{hdvn}/forums/nhac-viet-nam.183/',
	'Lossless Quốc tế': f'{hdvn}/forums/nhac-quoc-te.184/',
	'Lossless không lời': f'{hdvn}/forums/nhac-khong-loi.185/',
	'Lossy albums': f'{hdvn}/forums/lossy-albums.27/',
	'mHD, SD Video Clips': f'{hdvn}/forums/mhd-sd-video-clips.25/'
	}
	yield Listitem.search(search_hdvn)
	for k in H:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/thuvienhd.png'
		item.set_callback(hdvn_page, H[k], 1, k)
		yield item
	pass
@Route.register
def hdvn_page(plugin, url=None, next_page=None, k=None):
	yield []
	if any((url is None, next_page is None, k is None)):
		pass
	else:
		try:
			trangtiep = f'{url}page-{next_page}'
			r = getlink(trangtiep, trangtiep, 1000)
			if (r is not None) and ('titleText' in r.text) and ('pageNavHeader' in r.text):
				soup = BeautifulSoup(r.text, 'html.parser')
				tongtrang = re.findall(r"\d+", soup.select_one('span.pageNavHeader').get_text(strip=True))[-1]
				soups = soup.select('.discussionListItem')
				urls = [f"{hdvn}/{k.select_one('.titleText a.PreviewTooltip')['href']}" for k in soups if not k.select_one('.iconKey span.sticky')]
				length = len(urls)
				if length>0:
					with ThreadPoolExecutor(length) as ex:
						results = ex.map(process_url, urls)
					for (l, data) in results:
						if data is not None:
							item = Listitem()
							item.label = data[0]
							item.info['plot'] = f'{data[2]}\nNguồn: {hdvn}'
							item.info['mediatype'] = 'tvshow'
							item.info['trailer'] = yttk(data[0])
							item.art['thumb'] = item.art['poster'] = data[1]
							item.set_callback(hdvn_link, l)
							yield item
					if '>Tiếp' in r.text:
						item1 = Listitem()
						item1.label = f'Trang {str(int(next_page) + 1)}/{tongtrang}'
						item1.info['mediatype'] = 'tvshow'
						item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/nexthdvn.png'
						item1.set_callback(hdvn_page, url, str(int(next_page) + 1), k)
						yield item1
					yield trangmoi(url, k)
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def next_pagehdvn(plugin, url=None, k=None):
	yield []
	if any((url is None, k is None)):
		pass
	else:
		next_page = keyboard('Nhập số trang','',False)
		if not next_page or is_not_number(next_page):
			yield quangcao()
		else:
			try:
				trangtiep = f'{url}page-{next_page}'
				r = getlink(trangtiep, trangtiep, 1000)
				if (r is not None) and ('titleText' in r.text) and ('pageNavHeader' in r.text):
					soup = BeautifulSoup(r.text, 'html.parser')
					tongtrang = re.findall(r"\d+", soup.select_one('span.pageNavHeader').get_text(strip=True))[-1]
					soups = soup.select('a.PreviewTooltip')
					urls = [f"{hdvn}/{episode['href']}" for episode in soups]
					length = len(urls)
					if length>0:
						with ThreadPoolExecutor(length) as ex:
							results = ex.map(process_url, urls)
						for (l, data) in results:
							if data is not None:
								item = Listitem()
								item.label = data[0]
								item.info['plot'] = f'{data[2]}\nNguồn: {hdvn}'
								item.info['mediatype'] = 'tvshow'
								item.info['trailer'] = yttk(data[0])
								item.art['thumb'] = item.art['poster'] = data[1]
								item.set_callback(hdvn_link, l)
								yield item
						if '>Tiếp' in r.text:
							item1 = Listitem()
							item1.label = f'Trang {str(int(next_page) + 1)}/{tongtrang}'
							item1.info['mediatype'] = 'tvshow'
							item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/nexthdvn.png'
							item1.set_callback(hdvn_page, url, str(int(next_page) + 1), k)
							yield item1
						yield trangmoi(url, k)
				else:
					yield quangcao()
			except:
				yield quangcao()
@Route.register
def next_searchhdvn(plugin, search_query=None, idsearch=None):
	yield []
	if any((search_query is None, idsearch is None)):
		pass
	else:
		next_page = keyboard('Nhập số trang','',False)
		if not next_page or is_not_number(next_page):
			yield quangcao()
		else:
			try:
				trangtiep = f'{hdvn}/search/{idsearch}/?page={next_page}&q={search_query.replace(" ","+")}&o=date'
				r = getlink(trangtiep, trangtiep, 1000)
				if (r is not None) and ('titleText' in r.text) and ('pageNavHeader' in r.text):
					soup = BeautifulSoup(r.text, 'html.parser')
					tongtrang = re.findall(r"\d+", soup.select_one('span.pageNavHeader').get_text(strip=True))[-1]
					soups = soup.select('div.titleText a')
					urls = [f"{hdvn}/{episode['href']}" for episode in soups if 'titleText' in r.text]
					length = len(urls)
					if length>0:
						with ThreadPoolExecutor(length) as ex:
							results = ex.map(process_url, urls)
						for (l, data) in results:
							if data is not None:
								item = Listitem()
								item.label = data[0]
								item.info['plot'] = f'{data[2]}\nNguồn: {hdvn}'
								item.info['mediatype'] = 'tvshow'
								item.info['trailer'] = yttk(data[0])
								item.art['thumb'] = item.art['poster'] = data[1]
								item.set_callback(hdvn_link, l)
								yield item
						if '>Tiếp' in r.text:
							item1 = Listitem()
							item1.label = f'Trang {str(int(next_page) + 1)}/{tongtrang}'
							item1.info['mediatype'] = 'tvshow'
							item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/nexthdvn.png'
							item1.set_callback(search_hdvnnext, search_query, str(int(next_page) + 1), idsearch)
							yield item1
						yield tktrangmoi(search_query, idsearch)
				else:
					yield quangcao()
			except:
				yield quangcao()
@Route.register
def hdvn_link(plugin, url=None):
	yield []
	if url is None:
		pass
	else:
		try:
			likehdvn(url)
			r = loginfhdvn().get(url)
			if 'fshare.vn' in r.text:
				soup = BeautifulSoup(r.text, 'html.parser')
				soups = soup.select('a.externalLink')
				urls = list(dict.fromkeys([episode['href'] for episode in soups if 'fshare.vn' in episode['href']]))
				length = len(urls)
				if length>0:
					with ThreadPoolExecutor(length) as ex:
						results = ex.map(process_fs, urls)
					for (link, data) in results:
						if data is not None:
							item = Listitem()
							item.label = data[0]
							item.info['trailer'] = yttk(data[0])
							item.info['plot'] = f'{data[0]}\nNguồn: {hdvn}'
							imgfs = 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
							item.art['thumb'] = item.art['poster'] = imgfs
							item.context.script(Script.ref('/resources/lib/mkd/onfshare/ifshare:tfavo'), 'Thêm vào Fshare Favorite', link)
							if 'folder' in link:
								item.info['mediatype'] = 'tvshow'
								item.set_callback(Route.ref('/resources/lib/mkd/onfshare/ifshare:index_fs'), link, 0, imgfs)
							else:
								item.info['mediatype'] = 'episode'
								if Script.setting.get_string('taifshare') == 'true':
									item.context.script(Script.ref('/resources/lib/download:downloadfs'), 'Tải về', link)
								item.set_callback(Resolver.ref('/resources/lib/kedon:play_fs'), link, data[0])
							yield item
			else:
				yield quangcao()
		except:
			yield quangcao()
def trangmoi(url, k):
	item = Listitem()
	item.label = f'Trang khác (nhóm: {k})'
	item.info['mediatype'] = 'tvshow'
	item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/nexthdvn.png'
	item.set_callback(next_pagehdvn, url, k)
	return item
def tktrangmoi(search_query, idsearch):
	item = Listitem()
	item.label = f'Trang khác (từ khoá: {search_query})'
	item.info['mediatype'] = 'tvshow'
	item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/nexthdvn.png'
	item.set_callback(next_searchhdvn, search_query, idsearch)
	return item