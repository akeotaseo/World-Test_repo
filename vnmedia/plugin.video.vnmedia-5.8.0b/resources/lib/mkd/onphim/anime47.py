from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao, yeucau
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from codequick.utils import color
import re
uanm47 = 'https://anime47.link'
def finalurl(u):
	if u.startswith('http'):
		url = u
	else:
		url = f'{uanm47}{u}'
	return url
@Route.register
def index_anime47(plugin):
	yield Listitem.search(ds_anime47)
	yield yeucau('https://www.facebook.com/A47FB/')
	menu = {'Thể loại': anime47_theloai,
	'Trạng thái': anime47_trangthai,
	'Xem nhiều': anime47_xemnhieu,
	'Bình luận nhiều': anime47_binhluannhieu,
	'Lưỡng long nhất thể': anime47_luonglongnhatthe,
	'Năm': anime47_nam
	}
	dulieu = {
	'Phim mới': f'{uanm47}/danh-sach/phim-moi/',
	'Mùa này': f'{uanm47}/danh-sach/anime-mua-moi-update.html/',
	'Mùa trước': f'{uanm47}/danh-sach/anime-mua-truoc-moi-update.html/',
	'Bộ cũ': f'{uanm47}/danh-sach/anime-cu-moi-update.html/',
	'Hoạt hình Trung Quốc': f'{uanm47}/the-loai/hoat-hinh-trung-quoc-75/',
	'Phim dạng người đóng': f'{uanm47}/danh-sach/jpdrama/'
	}
	for k in dulieu:
		i = Listitem()
		i.label = k
		i.info['mediatype'] = 'tvshow'
		i.art['thumb'] = i.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/anime47.png'
		i.set_callback(ds_anime47, dulieu[k], 1)
		yield i
	for m in menu:
		item = Listitem()
		item.label = m
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/anime47.png'
		item.set_callback(menu[m])
		yield item
@Route.register
def anime47_theloai(plugin):
	menu = {
	'Đời Thường': f'{uanm47}/the-loai/doi-thuong-38/',
	'Harem': f'{uanm47}/the-loai/harem-36/',
	'Shounen': f'{uanm47}/the-loai/shounen-35/',
	'Học Đường': f'{uanm47}/the-loai/hoc-duong-33/',
	'Thể Thao': f'{uanm47}/the-loai/the-thao-32/',
	'Drama': f'{uanm47}/the-loai/drama-31/',
	'Trinh Thám': f'{uanm47}/the-loai/trinh-tham-30/',
	'Kinh Dị': f'{uanm47}/the-loai/kinh-di-29/',
	'Mecha': f'{uanm47}/the-loai/mecha-28/',
	'Phép Thuật': f'{uanm47}/the-loai/phep-thuat-27/',
	'Phiêu Lưu': f'{uanm47}/the-loai/phieu-luu-26/',
	'Ecchi': f'{uanm47}/the-loai/ecchi-25/',
	'Hài Hước': f'{uanm47}/the-loai/hai-huoc-24/',
	'Hành Động': f'{uanm47}/the-loai/hanh-dong-23/',
	'Romance': f'{uanm47}/the-loai/romance-40/',
	'Lịch Sử': f'{uanm47}/the-loai/lich-su-41/',
	'Âm Nhạc': f'{uanm47}/the-loai/am-nhac-42/',
	'Tokusatsu': f'{uanm47}/the-loai/tokusatsu-43/',
	'Viễn Tưởng': f'{uanm47}/the-loai/vien-tuong-44/',
	'Fantasy': f'{uanm47}/the-loai/fantasy-45/',
	'Blu-ray': f'{uanm47}/the-loai/blu-ray-46/',
	'Game': f'{uanm47}/the-loai/game-48/',
	'Shoujo': f'{uanm47}/the-loai/shoujo-49/',
	'Seinen': f'{uanm47}/the-loai/seinen-50/',
	'Super Power': f'{uanm47}/the-loai/super-power-51/',
	'Space': f'{uanm47}/the-loai/space-52/',
	'Martial Arts': f'{uanm47}/the-loai/martial-arts-53/',
	'Siêu Nhiên': f'{uanm47}/the-loai/sieu-nhien-54/',
	'Vampire': f'{uanm47}/the-loai/vampire-55/',
	'Mystery': f'{uanm47}/the-loai/mystery-56/',
	'Psychological': f'{uanm47}/the-loai/psychological-57/',
	'Yuri': f'{uanm47}/the-loai/yuri-58/',
	'Shounen Ai': f'{uanm47}/the-loai/shounen-ai-59/',
	'Shoujo Ai': f'{uanm47}/the-loai/shoujo-ai-60/',
	'Josei': f'{uanm47}/the-loai/josei-61/',
	'Parody': f'{uanm47}/the-loai/parody-62/',
	'Coming of Age': f'{uanm47}/the-loai/coming-of-age-63/',
	'Tragedy': f'{uanm47}/the-loai/tragedy-64/',
	'Demons': f'{uanm47}/the-loai/demons-65/',
	'Car': f'{uanm47}/the-loai/car-66/',
	'Dementia': f'{uanm47}/the-loai/dementia-67/',
	'Hentai': f'{uanm47}/the-loai/hentai-68/',
	'Kid': f'{uanm47}/the-loai/kid-69/',
	'Military': f'{uanm47}/the-loai/military-70/',
	'Police': f'{uanm47}/the-loai/police-71/',
	'Samurai': f'{uanm47}/the-loai/samurai-72/',
	'Thriller': f'{uanm47}/the-loai/thriller-73/',
	'Yaoi': f'{uanm47}/the-loai/yaoi-74/',
	'Hoạt hình Trung Quốc': f'{uanm47}/the-loai/hoat-hinh-trung-quoc-75/',
	'Xuyên Không - Chuyển Kiếp': f'{uanm47}/the-loai/xuyen-khong-chuyen-kiep-76/'
	}
	for k in menu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/anime47.png'
		item.set_callback(ds_anime47, menu[k], 1)
		yield item
@Route.register
def anime47_trangthai(plugin):
	menu = {
		'Hoàn thành': f'{uanm47}/tim-nang-cao/?status=complete&season=&year=&sort=popular',
		'Đang tiến hành': f'{uanm47}/tim-nang-cao/?status=ongoing&season=&year=&sort=popular'
	}
	for k in menu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/anime47.png'
		item.set_callback(ds_anime47, menu[k], 1)
		yield item

@Route.register
def anime47_xemnhieu(plugin):
	menu = {
	'Ngày': f'{uanm47}/danh-sach/xem-nhieu-trong-ngay.html',
	'Tuần': f'{uanm47}/danh-sach/xem-nhieu-trong-tuan.html',
	'Tháng': f'{uanm47}/danh-sach/xem-nhieu-trong-thang.html',
	'Mùa Này': f'{uanm47}/danh-sach/xem-nhieu-trong-mua.html',
	'Năm Này': f'{uanm47}/danh-sach/xem-nhieu-trong-nam.html',
	'Năm Trước': f'{uanm47}/tim-nang-cao/?status=&season=&year=2021&sort=popular',
	'Mùa trước': f'{uanm47}/tim-nang-cao/?status=&season=5&year=2022&sort=popular',
	'Tất cả': f'{uanm47}/tim-nang-cao/?status=&season=&year=&sort=popular'
	}
	for k in menu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/anime47.png'
		item.set_callback(ds_anime47, menu[k], 1)
		yield item

@Route.register
def anime47_binhluannhieu(plugin):
	menu = {
	'Mùa Này': f'{uanm47}/tim-nang-cao/?status=&season=6&year=2022&sort=comment',
	'Mùa Trước': f'{uanm47}/tim-nang-cao/?status=&season=5&year=2022&sort=comment',
	'Năm này': f'{uanm47}/tim-nang-cao/?status=&season=&year=2022&sort=comment',
	'Năm trước': f'{uanm47}/tim-nang-cao/?status=&season=&year=2021&sort=comment',
	'Tất cả': f'{uanm47}/tim-nang-cao/?status=&season=&year=&sort=comment'
	}
	for k in menu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/anime47.png'
		item.set_callback(ds_anime47, menu[k], 1)
		yield item
@Route.register
def anime47_luonglongnhatthe(plugin):
	menu = {
	'Hành Động + Hài Hước': f'{uanm47}/tim-nang-cao/?status=&genres=24&genres=23&season=&year=&sort=popular',
	'Lãng Mạn + Hành Động': f'{uanm47}/tim-nang-cao/?status=&genres=23&genres=40&season=&year=&sort=popular',
	'Harem + Hài Hước': f'{uanm47}/tim-nang-cao/?status=&genres=36&genres=24&season=&year=&sort=popular',
	'Ecchi + Harem': f'{uanm47}/tim-nang-cao/?status=&genres=36&genres=25&season=&year=&sort=popular',
	'Đời thường - Học Đường': f'{uanm47}/tim-nang-cao/?status=&genres=38&genres=33&season=&year=&sort=popular',
	'Học Đường - Ecchi': f'{uanm47}/tim-nang-cao/?status=&genres=33&genres=25&season=&year=&sort=popular',
	'Romance - Tragedy': f'{uanm47}/tim-nang-cao/?status=&genres=40&genres=64&season=&year=&sort=popular',
	'Kết hợp ngẫu nhiên': f'{uanm47}/tim-nang-cao/?status=&season=&year=&sort=popular'
	}
	for k in menu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/anime47.png'
		item.set_callback(ds_anime47, menu[k], 1)
		yield item
@Route.register
def anime47_nam(plugin):
	menu = {
	'2015': f'{uanm47}/tim-nang-cao/?status=&season=&year=2015&sort=popular',
	'2016': f'{uanm47}/tim-nang-cao/?status=&season=&year=2016&sort=popular',
	'2017': f'{uanm47}/tim-nang-cao/?status=&season=&year=2017&sort=popular',
	'2018': f'{uanm47}/tim-nang-cao/?status=&season=&year=2018&sort=popular',
	'2019': f'{uanm47}/tim-nang-cao/?status=&season=&year=2019&sort=popular',
	'2020': f'{uanm47}/tim-nang-cao/?status=&season=&year=2020&sort=popular',
	'2021': f'{uanm47}/tim-nang-cao/?status=&season=&year=2021&sort=popular',
	'2022': f'{uanm47}/tim-nang-cao/?status=&season=&year=2022&sort=popular',
	'2023': f'{uanm47}/tim-nang-cao/?status=&season=&year=2023&sort=popular',
	'2024': f'{uanm47}/tim-nang-cao/?status=&season=&year=2024&sort=popular'
	}
	for k in menu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/anime47.png'
		item.set_callback(ds_anime47, menu[k], 1)
		yield item
@Route.register
def ds_anime47(plugin, search_query=None, next_page=None):
	yield []
	try:
		if '://' not in search_query:
			next_page = 1
			sr = quote_plus(search_query)
			url = f'{uanm47}/tim-nang-cao/?keyword={sr}&nam=&season=&status=&sapxep=1'
		else:
			url = search_query 
			trangtiep = f"{url}{next_page}.html" if url.endswith('/') else f"{url}&page={next_page}"
			r = getlink(trangtiep, trangtiep, 1000)
			if (r is not None) and ('last-film-box' in r.text):
				soup = BeautifulSoup(r.text, 'html.parser')
				soups = soup.select('ul.last-film-box a')
				for k in soups:
					tiendo = k.select_one('div.movie-meta span.ribbon').get_text(strip=True)
					if 'trailer' not in tiendo.lower():
						tenm = k['title']
						anh = k.select_one('.movie-thumbnail .public-film-item-thumb')['style']
						img = re.search(r"(http.*?)('|\")", anh)[1]
						fname = f"{color(tiendo, 'yellow')} {tenm}"
						item = Listitem()
						item.label = fname
						item.info['plot'] = f'{fname}\nNguồn: {uanm47}'
						item.info['mediatype'] = 'tvshow'
						item.art['thumb'] = item.art['poster'] = img
						item.set_callback(episode_anime47, k['href'], anh)
						yield item
				if f'/{next_page + 1}.html' in r.text or f'page={next_page + 1}' in r.text:
					item1 = Listitem()
					item1.label = f'Trang {next_page + 1}'
					item1.info['mediatype'] = 'tvshow'
					item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
					item1.set_callback(ds_anime47, url, next_page + 1)
					yield item1
			else:
				yield quangcao()
	except:
		yield quangcao()
@Route.register
def episode_anime47(plugin, url=None, img=None):
	yield []
	if any((url is None, img is None)):
		pass
	else:
		try:
			u1 = finalurl(url)
			r1 = getlink(u1, u1, 1000)
			if (r1 is not None):
				soup1 = BeautifulSoup(r1.text, 'html.parser')
				u2 = soup1.select_one('a[id="btn-film-watch"]')['href']
				detail = soup1.select_one('div.news-article').get_text(strip=True)
				img = soup1.select_one('div.movie-l-img img')['src']
				ux = finalurl(u2)
				r = getlink(ux, ux, 1000)
				if (r is not None):
					soup = BeautifulSoup(r.text, 'html.parser')
					s = soup.select('div.server div.episodes a')
					for k in s:
						tenm = k['data-title']
						idp = k['data-episode-id']
						item = Listitem()
						item.label = tenm
						item.info['mediatype'] = 'episode'
						item.info['plot'] = f'{detail}\nNguồn: {uanm47}'
						item.art['thumb'] = item.art['poster'] = img
						item.set_callback(Resolver.ref('/resources/lib/kedon:play_anime47'), uanm47, idp, tenm)
						yield item
					if '"CSSTableGenerator"' in r1.text or "'CSSTableGenerator'" in r1.text:
						rows = soup1.select('div.CSSTableGenerator tr')
						for row in rows[1:]:
							cells = row.select('td')
							if len(cells) >= 3:
								movie_name = cells[0].get_text(strip=True)
								tap = cells[1].get_text(strip=True)
								movie_url = cells[0].select_one('a')['href']
								year = cells[2].get_text(strip=True)
								fullname = color(f'{movie_name} {tap} - {year}', 'yellow')
								item = Listitem()
								item.label = fullname
								item.info['mediatype'] = 'tvshow'
								item.info['plot'] = f'{detail}\nNguồn: {uanm47}'
								item.art['thumb'] = item.art['poster'] = img
								item.set_callback(episode_anime47, movie_url, img)
								yield item
				else:
					yield quangcao()
			else:
				yield quangcao()
		except:
			yield quangcao()