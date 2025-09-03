from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao, yeucau
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from codequick.utils import italic, color
import re
bl = 'https://bluphim.art'
def get_info_bluphim(x):
	u = x if x.startswith('http') else f'{bl}{x}'
	r = getlink(u,u,-1)
	try:
		soup = BeautifulSoup(r.text, 'html.parser')
		soups = soup.select('div.blockbody')
		for k in soups:
			try:
				img = k.select_one('div.poster img')['src'] if k.select_one('div.poster img')['src'].startswith('http') else f"{bl}{k.select_one('div.poster img')['src']}"
			except:
				img = 'https://raw.githubusercontent.com/kenvnm/kvn/main/bluphim.png'
			try:
				title = k.select_one('h1 span.title').get_text(strip=True)
				name2 = k.select_one('h2 span.real-name').get_text(strip=True)
				ten = f'{title} - {name2}'
			except:
				pass
			try:
				mota = k.select_one('div#info-film p').get_text(strip=True)
			except:
				mota = ten
			return (ten, img, mota)
	except:
		return None
def process_url(url):
	try:
		data = get_info_bluphim(url)
		return url, data
	except:
		return url, None
@Route.register
def index_bluphim(plugin):
	yield Listitem.search(ds_bluphim)
	yield yeucau('https://www.facebook.com/groups/bluphim')
	T = {'Thể loại': bluphim_tl,
	'Quốc gia': bluphim_qg}
	dulieu = {
	'Phim mới': f'{bl}/the-loai/phim-moi',
	'Cập nhật': f'{bl}/the-loai/phim-cap-nhat',
	'Phim lẻ': f'{bl}/the-loai/phim-le',
	'Phim bộ': f'{bl}/the-loai/phim-bo',
	'Phim chiếu rạp': f'{bl}/the-loai/phim-chieu-rap',
	'Hoạt hình': f'{bl}/the-loai/hoat-hinh'
	}
	for b in T:
		i = Listitem()
		i.label = b
		i.info['mediatype'] = 'tvshow'
		i.art['thumb'] = i.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/bluphim.png'
		i.set_callback(T[b])
		yield i
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/bluphim.png'
		item.set_callback(ds_bluphim, dulieu[k], 1)
		yield item
@Route.register
def bluphim_tl(plugin):
	dulieu = {
		'Thần thoại - Cổ trang': f'{bl}/the-loai/than-thoai-co-trang',
		'Hành động': f'{bl}/the-loai/hanh-dong',
		'Tâm lý': f'{bl}/the-loai/tam-ly',
		'Chiến tranh': f'{bl}/the-loai/chien-tranh',
		'Võ thuật - Kiếm hiệp': f'{bl}/the-loai/vo-thuat-kiem-hiep',
		'Nhạc kịch': f'{bl}/the-loai/nhac-kich',
		'Kinh dị': f'{bl}/the-loai/kinh-di',
		'Tội phạm - Hình sự': f'{bl}/the-loai/toi-pham-hinh-su',
		'Phiêu lưu': f'{bl}/the-loai/phieu-luu',
		'Hài hước': f'{bl}/the-loai/hai-huoc',
		'Viễn tưởng': f'{bl}/the-loai/vien-tuong',
		'Khoa học - Tài liệu': f'{bl}/the-loai/khoa-hoc-tai-lieu',
		'Hoạt hình': f'{bl}/the-loai/hoat-hinh',
		'Thể thao': f'{bl}/the-loai/the-thao',
		'Tình cảm - Lãng mạn': f'{bl}/the-loai/tinh-cam-lang-man',
		'Kỳ ảo': f'{bl}/the-loai/ky-ao',
		'Giật gân': f'{bl}/the-loai/giat-gan',
		'Gia đình': f'{bl}/the-loai/gia-dinh',
		'Bí ẩn': f'{bl}/the-loai/bi-an',
		'Lịch sử': f'{bl}/the-loai/lich-su',
		'Viễn Tây': f'{bl}/the-loai/vien-tay',
		'Tiểu sử': f'{bl}/the-loai/tieu-su',
		'GameShow': f'{bl}/the-loai/chuong-trinh-truyen-hinh',
	}
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/bluphim.png'
		item.set_callback(ds_bluphim, dulieu[k], 1)
		yield item
@Route.register
def bluphim_qg(plugin):
	dulieu = {
		'Âu - Mỹ': f'{bl}/quoc-gia/au-my',
		'Trung Quốc - Hồng Kông': f'{bl}/quoc-gia/trung-quoc-hong-kong',
		'Hàn Quốc': f'{bl}/quoc-gia/han-quoc',
		'Nhật Bản': f'{bl}/quoc-gia/nhat-ban',
		'Ấn Độ': f'{bl}/quoc-gia/an-do',
		'Việt Nam': f'{bl}/quoc-gia/viet-nam',
		'Tổng hợp': f'{bl}/quoc-gia/tong-hop',
	}
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/bluphim.png'
		item.set_callback(ds_bluphim, dulieu[k], 1)
		yield item
@Route.register
def ds_bluphim(plugin, search_query=None, next_page=None):
	yield []
	try:
		if '://' not in search_query:
			next_page = 1
			sr = quote_plus(search_query)
			url = f'{bl}/search?k={sr}'
		else:
			url = search_query
		trangtiep = f'{url}-{next_page}'
		r = getlink(trangtiep, trangtiep, 1000)
		if (r is not None) and ('list-films' in r.text):
			soup = BeautifulSoup(r.text, 'html.parser')
			soups = soup.select('div#page-info div.list-films ul li.item a')
			urls = [k['href'] for k in soups]
			length = len(urls)
			if length>0:
				with ThreadPoolExecutor(length) as ex:
					results = ex.map(process_url, urls)
				for (l, data) in results:
					if data is not None:
						item = Listitem()
						item.label = data[0]
						item.info['plot'] = f'{data[2]}\nNguồn: {bl}'
						item.info['mediatype'] = 'tvshow'
						item.art['thumb'] = item.art['poster'] = data[1]
						item.set_callback(episode_bluphim, l, data[0], data[2], data[1])
						yield item
				if f'-{next_page + 1}' in r.text:
					item1 = Listitem()
					item1.label = f'Trang {next_page + 1}'
					item1.info['mediatype'] = 'tvshow'
					item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
					item1.set_callback(ds_bluphim, url, next_page + 1)
					yield item1
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def episode_bluphim(plugin, url=None, title=None, info=None, img=None):
	yield []
	if any((url is None,title is None,info is None,img is None)):
		pass
	else:
		try:
			url = url if url.startswith('http') else f'{bl}{url}'
			r = getlink(url, url, 1000)
			if (r is not None) and 'style="display' in r.text:
				if 'youtube.com/' in r.text:
					idvd = re.search(r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)', r.text)[1]
					item1 = Listitem()
					item1.label = f'TRAILER: {italic(title)}'
					item1.info['mediatype'] = 'episode'
					item1.art['thumb'] = item1.art['poster'] = f'https://i.ytimg.com/vi/{idvd}/sddefault.jpg'
					item1.set_path(f'plugin://plugin.video.youtube/play/?video_id={idvd}')
					yield item1
				soupx = BeautifulSoup(r.text, 'html.parser')
				uplay = soupx.select_one('li[style*="display"] a')['href']
				urlplay = uplay if uplay.startswith('http') else f"{bl}{uplay}"
				resp = getlink(urlplay, url, 1000)
				if (resp is not None):
					if 'list-episode' in resp.text:
						soup = BeautifulSoup(resp.text, 'html.parser')
						soups = soup.select('.control-box .list-episode a')
						for e in soups:
							item = Listitem()
							tenm = f'{e.get_text(strip=True)} - {title}'
							item.label = tenm
							item.info['mediatype'] = 'episode'
							item.info['plot'] = f'{info}\nNguồn: {bl}'
							item.art['thumb'] = item.art['poster'] = img
							item.set_callback(Resolver.ref('/resources/lib/kedon:play_bluphim'), e['href'], tenm, bl)
							yield item
				else:
					yield quangcao()
			else:
				yield quangcao()
		except:
			yield quangcao()