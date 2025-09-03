from codequick import Route, Listitem, Resolver, Script
from resources.lib.kedon import getlink, quangcao, gioithieu, yeucau, stream, referer
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote_plus
from codequick.utils import color
import re
unc = 'https://phim.nguonc.com'
def get_info_nguonc(x):
	r = getlink(f'{unc}/api/film/{x}', unc,-1)
	try:
		if Script.setting.get_string('kenh18') == 'true':
			if r is not None:
				kq = r.json()['movie']
				try:
					img = kq['thumb_url']
				except:
					img = 'https://raw.githubusercontent.com/kenvnm/kvn/main/nguonc.png'
				try:
					ten = kq['name']
				except:
					pass
				try:
					mota = re.sub('<.*?>', '', kq['description'])
				except:
					mota = ten
				return (ten, img, mota)
			else:
				return None
		else:
			if r is not None and '18+' not in r.text:
				kq = r.json()['movie']
				try:
					img = kq['thumb_url']
				except:
					img = 'https://raw.githubusercontent.com/kenvnm/kvn/main/nguonc.png'
				try:
					ten = kq['name']
				except:
					pass
				try:
					mota = re.sub('<.*?>', '', kq['description'])
				except:
					mota = ten
				return (ten, img, mota)
			else:
				return None
	except:
		return None
def process_url(url):
	try:
		data = get_info_nguonc(url)
		return url, data
	except:
		return url, None
@Route.register
def index_nguonc(plugin):
	yield Listitem.search(ds_nguonc)
	yield yeucau('https://t.me/phimnguonc')
	T = {'Thể loại': nguonc_tl,
	'Quốc gia': nguonc_qg,
	'Năm': nguonc_nam}
	dulieu = {
	'Phim mới': f'{unc}/api/films/phim-moi-cap-nhat',
	'Phim đang chiếu': f'{unc}/api/films/danh-sach/phim-dang-chieu',
	'Phim lẻ': f'{unc}/api/films/danh-sach/phim-le',
	'Phim bộ': f'{unc}/api/films/danh-sach/phim-bo',
	'Hoạt hình': f'{unc}/api/films/the-loai/hoat-hinh',
	'TV Shows': f'{unc}/api/films/danh-sach/tv-shows'
	}
	for b in T:
		i = Listitem()
		i.label = b
		i.info['mediatype'] = 'tvshow'
		i.art['thumb'] = i.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/nguonc.png'
		i.set_callback(T[b])
		yield i
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/nguonc.png'
		item.set_callback(ds_nguonc, dulieu[k], 1)
		yield item
@Route.register
def nguonc_tl(plugin):
	if Script.setting.get_string('kenh18') == 'true':
		dulieu = {
		'Hành Động': f'{unc}/api/films/the-loai/hanh-dong',
		'Phiêu Lưu': f'{unc}/api/films/the-loai/phieu-luu',
		'Hoạt Hình': f'{unc}/api/films/the-loai/hoat-hinh',
		'Hài': f'{unc}/api/films/the-loai/phim-hai',
		'Hình Sự': f'{unc}/api/films/the-loai/hinh-su',
		'Tài Liệu': f'{unc}/api/films/the-loai/tai-lieu',
		'Chính Kịch': f'{unc}/api/films/the-loai/chinh-kich',
		'Gia Đình': f'{unc}/api/films/the-loai/gia-dinh',
		'Giả Tượng': f'{unc}/api/films/the-loai/gia-tuong',
		'Lịch Sử': f'{unc}/api/films/the-loai/lich-su',
		'Kinh Dị': f'{unc}/api/films/the-loai/kinh-di',
		'Nhạc': f'{unc}/api/films/films/the-loai/phim-nhac',
		'Bí Ẩn': f'{unc}/api/films/the-loai/bi-an',
		'Lãng Mạn': f'{unc}/api/films/the-loai/lang-man',
		'Khoa Học Viễn Tưởng': f'{unc}/api/films/the-loai/khoa-hoc-vien-tuong',
		'Gây Cấn': f'{unc}/api/films/the-loai/gay-can',
		'Chiến Tranh': f'{unc}/api/films/the-loai/chien-tranh',
		'Tâm Lý': f'{unc}/api/films/the-loai/tam-ly',
		'Tình Cảm': f'{unc}/api/films/the-loai/tinh-cam',
		'Cổ Trang': f'{unc}/api/films/the-loai/co-trang',
		'Miền Tây': f'{unc}/api/films/the-loai/mien-tay',
		'Phim 18+': f'{unc}/api/films/the-loai/phim-18'
		}
	else:
		dulieu = {
		'Hành Động': f'{unc}/api/films/the-loai/hanh-dong',
		'Phiêu Lưu': f'{unc}/api/films/the-loai/phieu-luu',
		'Hoạt Hình': f'{unc}/api/films/the-loai/hoat-hinh',
		'Hài': f'{unc}/api/films/the-loai/phim-hai',
		'Hình Sự': f'{unc}/api/films/the-loai/hinh-su',
		'Tài Liệu': f'{unc}/api/films/the-loai/tai-lieu',
		'Chính Kịch': f'{unc}/api/films/the-loai/chinh-kich',
		'Gia Đình': f'{unc}/api/films/the-loai/gia-dinh',
		'Giả Tượng': f'{unc}/api/films/the-loai/gia-tuong',
		'Lịch Sử': f'{unc}/api/films/the-loai/lich-su',
		'Kinh Dị': f'{unc}/api/films/the-loai/kinh-di',
		'Nhạc': f'{unc}/api/films/the-loai/phim-nhac',
		'Bí Ẩn': f'{unc}/api/films/the-loai/bi-an',
		'Lãng Mạn': f'{unc}/api/films/the-loai/lang-man',
		'Khoa Học Viễn Tưởng': f'{unc}/api/films/the-loai/khoa-hoc-vien-tuong',
		'Gây Cấn': f'{unc}/api/films/the-loai/gay-can',
		'Chiến Tranh': f'{unc}/api/films/the-loai/chien-tranh',
		'Tâm Lý': f'{unc}/api/films/the-loai/tam-ly',
		'Tình Cảm': f'{unc}/api/films/the-loai/tinh-cam',
		'Cổ Trang': f'{unc}/api/films/the-loai/co-trang',
		'Miền Tây': f'{unc}/api/films/the-loai/mien-tay'
		}
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/nguonc.png'
		item.set_callback(ds_nguonc, dulieu[k], 1)
		yield item
@Route.register
def nguonc_qg(plugin):
	dulieu = {
	'Âu Mỹ': f'{unc}/api/films/quoc-gia/au-my',
	'Anh': f'{unc}/api/films/quoc-gia/anh',
	'Trung Quốc': f'{unc}/api/films/quoc-gia/trung-quoc',
	'Indonesia': f'{unc}/api/films/quoc-gia/indonesia',
	'Việt Nam': f'{unc}/api/films/quoc-gia/viet-nam',
	'Pháp': f'{unc}/api/films/quoc-gia/phap',
	'Hồng Kông': f'{unc}/api/films/quoc-gia/hong-kong',
	'Hàn Quốc': f'{unc}/api/films/quoc-gia/han-quoc',
	'Nhật Bản': f'{unc}/api/films/quoc-gia/nhat-ban',
	'Thái Lan': f'{unc}/api/films/quoc-gia/thai-lan',
	'Đài Loan': f'{unc}/api/films/quoc-gia/dai-loan',
	'Nga': f'{unc}/api/films/quoc-gia/nga',
	'Hà Lan': f'{unc}/api/films/quoc-gia/ha-lan',
	'Philippines': f'{unc}/api/films/films/quoc-gia/philippines',
	'Ấn Độ': f'{unc}/api/films/quoc-gia/an-do',
	'Quốc gia khác': f'{unc}/api/films/quoc-gia/quoc-gia-khac'
	}
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/nguonc.png'
		item.set_callback(ds_nguonc, dulieu[k], 1)
		yield item
@Route.register
def nguonc_nam(plugin):
	dulieu = {
		'2004': f'{unc}/api/films/nam-phat-hanh/2004',
		'2005': f'{unc}/api/films/nam-phat-hanh/2005',
		'2006': f'{unc}/api/films/nam-phat-hanh/2006',
		'2007': f'{unc}/api/films/nam-phat-hanh/2007',
		'2008': f'{unc}/api/films/nam-phat-hanh/2008',
		'2009': f'{unc}/api/films/nam-phat-hanh/2009',
		'2010': f'{unc}/api/films/nam-phat-hanh/2010',
		'2011': f'{unc}/api/films/nam-phat-hanh/2011',
		'2012': f'{unc}/api/films/nam-phat-hanh/2012',
		'2013': f'{unc}/api/films/nam-phat-hanh/2013',
		'2014': f'{unc}/api/films/nam-phat-hanh/2014',
		'2015': f'{unc}/api/films/nam-phat-hanh/2015',
		'2016': f'{unc}/api/films/nam-phat-hanh/2016',
		'2017': f'{unc}/api/films/nam-phat-hanh/2017',
		'2018': f'{unc}/api/films/nam-phat-hanh/2018',
		'2019': f'{unc}/api/films/nam-phat-hanh/2019',
		'2020': f'{unc}/api/films/nam-phat-hanh/2020',
		'2021': f'{unc}/api/films/nam-phat-hanh/2021',
		'2022': f'{unc}/api/films/nam-phat-hanh/2022',
		'2023': f'{unc}/api/films/nam-phat-hanh/2023',
		'2024': f'{unc}/api/films/nam-phat-hanh/2024',
	}
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/nguonc.png'
		item.set_callback(ds_nguonc, dulieu[k], 1)
		yield item
@Route.register
def ds_nguonc(plugin, search_query=None, next_page=None):
	yield []
	try:
		if '://' not in search_query:
			next_page = 1
			sr = quote_plus(search_query)
			match = f'{unc}/api/films/search?keyword={sr}'
		else:
			match = search_query
		n = f'{match}&page={next_page}' if '?' in match else f'{match}?page={next_page}'
		resp = getlink(n, n, 1000)
		if (resp is not None):
			urls = [k['slug'] for k in resp.json()['items']]
			length = len(urls)
			if length>0:
				with ThreadPoolExecutor(length) as ex:
					results = ex.map(process_url, urls)
				for (l, data) in results:
					if data is not None:
						item = Listitem()
						item.label = data[0]
						item.info['plot'] = f'{data[2]}\nNguồn: {unc}'
						item.info['mediatype'] = 'tvshow'
						item.art['thumb'] = item.art['poster'] = data[1]
						item.set_callback(id_nguonc, l)
						yield item
				if next_page < resp.json()['paginate']['total_page']:
					item1 = Listitem()
					item1.label = f'Trang {next_page + 1}'
					item1.info['mediatype'] = 'tvshow'
					item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
					item1.set_callback(ds_nguonc, match, next_page + 1)
					yield item1
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def id_nguonc(plugin, idk=None):
	yield []
	if idk is None:
		pass
	else:
		try:
			t = f'{unc}/api/film/{idk}'
			resp = getlink(t, t, 1000)
			if (resp is not None):
				try:
					kq = resp.json()
					ke = kq['movie']['episodes']
					title = kq['movie']['name']
					title2= kq['movie']['original_name']
					namefilm = f'{title}-{title2}'
					mota = re.sub('<.*?>', '', kq['movie']['description'])
					anh = kq['movie']['thumb_url']
					yield gioithieu(namefilm, mota, anh)
					b = ((k1['server_name'], k2['name'], k2['embed']) for k1 in ke for k2 in k1['items'] if 'm3u8' in k2)
					for k in b:
						item = Listitem()
						tenm = f"{color(k[0], 'yellow')} Tập {k[1]} - {namefilm}"
						item.label = tenm
						item.info['mediatype'] = 'episode'
						item.info['plot'] = f'{mota}\nNguồn: {unc}'
						item.art['thumb'] = item.art['poster'] = anh
						item.set_callback(Resolver.ref('/resources/lib/kedon:play_nc'), k[2], tenm)
						yield item
				except:
					pass
			else:
				yield quangcao()
		except:
			yield quangcao()