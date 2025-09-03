from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao, yeucau
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from codequick.utils import italic, color
import re
pm = 'https://phimmoi.onl'
def get_info_phimmoi(x):
	r = getlink(x,x,-1)
	try:
		soup = BeautifulSoup(r.text, 'html.parser')
		soups = soup.select('div.movie-info')
		for k in soups:
			try:
				img = k.select_one('div.movie-l-img img')['src']
			except:
				img = 'https://raw.githubusercontent.com/kenvnm/kvn/main/phimmoi.png'
			try:
				title = k.select_one('span.title-1').get_text(strip=True)
				name2 = k.select_one('span.title-2').get_text(strip=True)
				ten = f'{title} - {name2}'
			except:
				pass
			try:
				mota = k.select_one('div#film-content p').get_text(strip=True)
			except:
				mota = ten
			return (ten, img, mota)
	except:
		return None
def process_url(url):
	try:
		data = get_info_phimmoi(url)
		return url, data
	except:
		return url, None
@Route.register
def index_phimmoi(plugin):
	yield Listitem.search(ds_phimmoi)
	yield yeucau('https://t.me/+hC2J0oUMdMYwYTdl')
	T = {'Thể loại': phimmoi_tl,
	'Quốc gia': phimmoi_qg}
	dulieu = {
	'Phim mới': f'{pm}/danh-sach/phim-moi.html',
	'Phim lẻ': f'{pm}/danh-sach/phim-le.html',
	'Phim bộ': f'{pm}/danh-sach/phim-bo.html'
	}
	for b in T:
		i = Listitem()
		i.label = b
		i.info['mediatype'] = 'tvshow'
		i.art['thumb'] = i.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/phimmoi.png'
		i.set_callback(T[b])
		yield i
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/phimmoi.png'
		item.set_callback(ds_phimmoi, dulieu[k], 1)
		yield item
@Route.register
def phimmoi_tl(plugin):
	dulieu = {
		'Boys Love': f'{pm}/the-loai/boys-love.html',
		'Gia đình': f'{pm}/the-loai/gia-dinh.html',
		'Thần Thoại': f'{pm}/the-loai/than-thoai.html',
		'Hài Hước': f'{pm}/the-loai/hai-huoc.html',
		'Kinh Dị': f'{pm}/the-loai/kinh-di.html',
		'Lãng mạn': f'{pm}/the-loai/lang-man.html',
		'Viễn Tưởng': f'{pm}/the-loai/vien-tuong.html',
		'Võ Thuật': f'{pm}/the-loai/vo-thuat.html',
		'Cổ Trang': f'{pm}/the-loai/co-trang.html',
		'Hoạt Hình': f'{pm}/the-loai/hoat-hinh.html',
		'Hình Sự': f'{pm}/the-loai/hinh-su.html',
		'Tâm Lý': f'{pm}/the-loai/tam-ly.html',
		'Thể thao-Âm nhạc': f'{pm}/the-loai/the-thao-am-nhac.html',
		'Tình Cảm': f'{pm}/the-loai/tinh-cam.html',
		'Truyền hình': f'{pm}/the-loai/truyen-hinh.html',
		'Chính kịch': f'{pm}/the-loai/chinh-kich.html',
		'Hành Động': f'{pm}/the-loai/hanh-dong.html',
		'Phim 18+': f'{pm}/the-loai/phim-18.html',
		'Chiến Tranh': f'{pm}/the-loai/chien-tranh.html',
		'Dã Sữ': f'{pm}/the-loai/da-su.html',
		'Tài liệu': f'{pm}/the-loai/tai-lieu.html',
		'Shows': f'{pm}/the-loai/shows.html',
		'Phiêu Lưu': f'{pm}/the-loai/phieu-luu.html',
	}

	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/phimmoi.png'
		item.set_callback(ds_phimmoi, dulieu[k], 1)
		yield item
@Route.register
def phimmoi_qg(plugin):
	dulieu = {
		'Hồng Kông': f'{pm}/quoc-gia/hong-kong.html',
		'Hàn Quốc': f'{pm}/quoc-gia/han-quoc.html',
		'Trung Quốc': f'{pm}/quoc-gia/china.html',
		'Châu Á': f'{pm}/quoc-gia/chau-a.html',
		'Mỹ': f'{pm}/quoc-gia/my.html',
		'Đài Loan': f'{pm}/quoc-gia/dai-loan.html',
		'Nhật Bản': f'{pm}/quoc-gia/nhat-ban.html',
		'Châu Âu': f'{pm}/quoc-gia/chau-au.html',
		'Thái Lan': f'{pm}/quoc-gia/thai-lan.html',
		'Quốc gia khác': f'{pm}/quoc-gia/quoc-gia-khac.html',
		'Úc': f'{pm}/quoc-gia/uc.html',
		'Anh': f'{pm}/quoc-gia/anh.html',
		'Indonesia': f'{pm}/quoc-gia/indonesia.html',
		'Ấn Độ': f'{pm}/quoc-gia/an-do.html',
	}
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/phimmoi.png'
		item.set_callback(ds_phimmoi, dulieu[k], 1)
		yield item
@Route.register
def ds_phimmoi(plugin, search_query=None, next_page=None):
	yield []
	try:
		if '://' not in search_query:
			next_page = 1
			sr = quote_plus(search_query)
			url = f'{pm}?search={sr}'
		else:
			url = search_query
		trangtiep = f'{url}&page={next_page}' if '?' in url else f'{url}?page={next_page}'
		r = getlink(trangtiep, trangtiep, 1000)
		if (r is not None) and ('last-film-box' in r.text):
			soup = BeautifulSoup(r.text, 'html.parser')
			soups = soup.select('ul.last-film-box li a.movie-item')
			urls = [k['href'] for k in soups if 'sắp chiếu' not in k.get_text(strip=True).lower()]
			length = len(urls)
			if length>0:
				with ThreadPoolExecutor(length) as ex:
					results = ex.map(process_url, urls)
				for (l, data) in results:
					if data is not None:
						item = Listitem()
						item.label = data[0]
						img = data[1] if data[1].startswith('http') else f'{pm}{data[1]}'
						item.info['plot'] = f'{data[2]}\nNguồn: {pm}'
						item.info['mediatype'] = 'tvshow'
						item.art['thumb'] = item.art['poster'] = img
						item.set_callback(episode_phimmoi, l, data[0], data[2], img)
						yield item
				if f'page={next_page + 1}' in r.text:
					item1 = Listitem()
					item1.label = f'Trang {next_page + 1}'
					item1.info['mediatype'] = 'tvshow'
					item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
					item1.set_callback(ds_phimmoi, url, next_page + 1)
					yield item1
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def episode_phimmoi(plugin, url=None, title=None, info=None, img=None):
	yield []
	if any((url is None,title is None,info is None,img is None)):
		pass
	else:
		try:
			r = getlink(url, url, 1000)
			if (r is not None) and 'btn-film-watch' in r.text:
				if 'youtube.com/' in r.text:
					idvd = re.search(r'youtube\.com/embed\/([a-zA-Z0-9_-]+)', r.text)[1]
					item1 = Listitem()
					item1.label = f'TRAILER: {italic(title)}'
					item1.info['mediatype'] = 'episode'
					item1.art['thumb'] = item1.art['poster'] = f'https://i.ytimg.com/vi/{idvd}/sddefault.jpg'
					item1.set_path(f'plugin://plugin.video.youtube/play/?video_id={idvd}')
					yield item1
				soupx = BeautifulSoup(r.text, 'html.parser')
				urlplay = soupx.select_one('a#btn-film-watch')['href']
				resp = getlink(urlplay, url, 1000)
				if (resp is not None):
					if 'list-server' in resp.text:
						soup = BeautifulSoup(resp.text, 'html.parser')
						soups = soup.select('div.list-server div.server')
						s = [(' '.join(k.select_one('h3.server-name').get_text(strip=True).split()), m.get_text(strip=True), m['href']) for k in soups for m in k.select('li.episode a')]
						for e in s:
							item = Listitem()
							tenm = f'{color(e[0], "yellow")} {e[1]} - {title}'
							item.label = tenm
							item.info['mediatype'] = 'episode'
							item.info['plot'] = f'{info}\nNguồn: {pm}'
							item.art['thumb'] = item.art['poster'] = img
							item.set_callback(Resolver.ref('/resources/lib/kedon:play_phimmoi'), e[2], tenm, pm)
							yield item
				else:
					yield quangcao()
			else:
				yield quangcao()
		except:
			yield quangcao()