from codequick import Route, Listitem, Script, Resolver
from resources.lib.kedon import getlink, quangcao, yttk, get_info_fs, gioithieu, yeucau
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from concurrent.futures import ThreadPoolExecutor
import re
ufn = 'https://thuvienhd.xyz'
def get_info_tvhd(idk):
	t = f'{ufn}/?feed=fsharejson&id={idk}'
	resp = getlink(t, t, 1000)
	if (resp is not None) and resp.json()['link']:
		try:
			d = resp.json()
			img = d['image']
			mota = d['description']
			ten = d['title'].replace('&&','-')
			return (ten, img, mota)
		except:
			return None
	else:
		return None
def process_url(idk):
	try:
		data = get_info_tvhd(idk)
		return idk, data
	except:
		return idk, None
def process_fs(url):
	try:
		data = get_info_fs(url)
		return url, data
	except:
		return url, None
@Route.register
def search_thuvienhd(plugin, search_query=None):
	yield []
	if search_query is None:
		pass
	else:
		try:
			sr = quote_plus(search_query)
			url = f'{ufn}/?s={sr}'
			resp = getlink(url, ufn, 1000)
			if (resp is not None):
				match = re.search(r'"nonce":"(.*?)"', resp.text)[1]
				urltv = f'{ufn}/wp-json/dooplay/search/?nonce={match}&keyword={sr}'
				r = getlink(urltv, ufn, 1000)
				if 'No results' in r.text:
					yield quangcao()
				else:
					rs = r.json().values()
					for k in rs:
						item = Listitem()
						item.label = k['title']
						item.info['plot'] = f"{k['title']}\nNguồn: {ufn}"
						item.info['mediatype'] = 'tvshow'
						item.info['trailer'] = yttk(k['title'])
						item.art['thumb'] = item.art['poster'] = k['img']
						item.set_callback(thuvienhd_linktk, k['url'])
						yield item
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def index_thuvienhd(plugin):
	yield Listitem.search(search_thuvienhd)
	yield yeucau('https://www.facebook.com/thuvienhd/')
	T = {'Phim lẻ': tvhd_phimle,
	'Phim bộ': tvhd_phimbo,
	'Nhạc': tvhd_nhac}
	if Script.setting.get_string('kenh18') == 'true':
		dulieu = {
		'Phim mới':f'{ufn}/recent',
		'Thịnh hành':f'{ufn}/trending',
		'Thuyết minh':f'{ufn}/genre/thuyet-minh-tieng-viet',
		'Lồng tiếng':f'{ufn}/genre/long-tieng-tieng-viet',
		'H265':f'{ufn}/genre/h265',
		'3D':f'{ufn}/genre/3d',
		'4K':f'{ufn}/genre/4k',
		'ATV':f'{ufn}/genre/atv',
		'Bluray':f'{ufn}/genre/bluray-nguyen-goc',
		'TVB':f'{ufn}/genre/tvb',
		'Bộ sưu tập':f'{ufn}/genre/collection',
		'TV Shows':f'{ufn}/genre/tv-show',
		'TV':f'{ufn}/genre/tv',
		'Phim truyền hình':f'{ufn}/genre/tv-movie',
		'Phim 18':f'{ufn}/genre/18'
		}
	else:
		dulieu = {
		'Phim mới':f'{ufn}/recent',
		'Thịnh hành':f'{ufn}/trending',
		'Thuyết minh':f'{ufn}/genre/thuyet-minh-tieng-viet',
		'Lồng tiếng':f'{ufn}/genre/long-tieng-tieng-viet',
		'H265':f'{ufn}/genre/h265',
		'3D':f'{ufn}/genre/3d',
		'4K':f'{ufn}/genre/4k',
		'ATV':f'{ufn}/genre/atv',
		'Bluray':f'{ufn}/genre/bluray-nguyen-goc',
		'TVB':f'{ufn}/genre/tvb',
		'Bộ sưu tập':f'{ufn}/genre/collection',
		'TV Shows':f'{ufn}/genre/tv-show',
		'TV':f'{ufn}/genre/tv',
		'Phim truyền hình':f'{ufn}/genre/tv-movie'
		}
	for k in T:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/tvhd.png'
		item.set_callback(T[k])
		yield item
	for h in dulieu:
		i1 = Listitem()
		i1.label = h
		i1.info['mediatype'] = 'tvshow'
		i1.art['thumb'] = i1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/tvhd.png'
		i1.set_callback(thuvienhd_page, f'{dulieu[h]}/page/', 1)
		yield i1
@Route.register
def tvhd_phimle(plugin):
	dulieu = {
	'Mới nhất':f'{ufn}/genre/phim-le',
	'3D': f'{ufn}/genre/3d',
	'4K': f'{ufn}/genre/4k',
	'Âm Nhạc': f'{ufn}/genre/am-nhac',
	'Ấn Độ': f'{ufn}/genre/india',
	'Bản quyền': f'{ufn}/genre/copyright',
	'Bí Ẩn': f'{ufn}/genre/bi-an',
	'Cao Bồi': f'{ufn}/genre/western',
	'Chiến Tranh': f'{ufn}/genre/war',
	'Chính Kịch': f'{ufn}/genre/chinh-kich',
	'Cổ Trang': f'{ufn}/genre/co-trang-phim',
	'Gây cấn': f'{ufn}/genre/gay-can',
	'Gia Đình': f'{ufn}/genre/gia-dinh',
	'Hài': f'{ufn}/genre/comedy',
	'Hàn Quốc': f'{ufn}/genre/korean',
	'Hành Động': f'{ufn}/genre/action',
	'Hình Sự': f'{ufn}/genre/crime',
	'Hồi hộp': f'{ufn}/genre/hoi-hop',
	'Hongkong': f'{ufn}/genre/hongkong',
	'Huyền Bí': f'{ufn}/genre/mystery',
	'Kinh Dị': f'{ufn}/genre/horror',
	'Lãng Mạn': f'{ufn}/genre/romance',
	'Lịch Sử': f'{ufn}/genre/history',
	'Nhạc Kịch': f'{ufn}/genre/nhac-kich',
	'Phiêu Lưu': f'{ufn}/genre/adventure',
	'Rùng Rợn': f'{ufn}/genre/thriller',
	'Tâm Lý': f'{ufn}/genre/drama',
	'Thần Thoại': f'{ufn}/genre/fantasy',
	'Thể Thao': f'{ufn}/genre/the-thao',
	'Thiếu Nhi': f'{ufn}/genre/family',
	'Tiểu Sử': f'{ufn}/genre/tieu-su',
	'Tình Cảm': f'{ufn}/genre/tinh-cam',
	'Tội Phạm': f'{ufn}/genre/toi-pham',
	'Trinh Thám': f'{ufn}/genre/trinh-tham',
	'Trung Quốc': f'{ufn}/genre/trung-quoc-series',
	'Viễn Tưởng': f'{ufn}/genre/sci-fi',
	'Việt Nam': f'{ufn}/genre/vietnamese',
	'Võ Thuật': f'{ufn}/genre/vo-thuat-phim-2',
	'Giáng Sinh': f'{ufn}/genre/giang-sinh',
	'Phim Hoạt Hình': f'{ufn}/genre/animation',
	'Phim Tài Liệu': f'{ufn}/genre/documentary',
	'Phim': f'{ufn}/genre/phim'
}
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/tvhd.png'
		item.set_callback(thuvienhd_page, f'{dulieu[k]}/page/', 1)
		yield item
@Route.register
def tvhd_phimbo(plugin):
	dulieu = {
	'Mới nhất':f'{ufn}/genre/series',
	'Phim Bộ Nigeria': f'{ufn}/genre/phi-bo-nigeria',
	'Phim Bộ Ả Rập': f'{ufn}/genre/phim-bo-a-rap',
	'Phim Bộ Ai Cập': f'{ufn}/genre/phim-bo-ai-cap',
	'Phim Bộ Ái Nhĩ Lan (Ireland)': f'{ufn}/genre/phim-bo-ai-nhi-lan-ireland',
	'Phim Bộ Ấn Độ': f'{ufn}/genre/phim-bo-an-do',
	'Phim bộ Anh': f'{ufn}/genre/phim-bo-anh',
	'Phim Bộ Áo': f'{ufn}/genre/phim-bo-ao',
	'Phim Bộ Argentina': f'{ufn}/genre/phim-bo-argentina',
	'Phim Bộ Australia': f'{ufn}/genre/phim-bo-australia',
	'Phim Bộ Ba Lan': f'{ufn}/genre/phim-bo-ba-lan',
	'Phim Bộ Bỉ': f'{ufn}/genre/phim-bo-bi',
	'Phim Bộ Bồ Đào Nha': f'{ufn}/genre/phim-bo-bo-dao-nha',
	'Phim Bộ Brazil': f'{ufn}/genre/phim-bo-brazil',
	'Phim Bộ Canada': f'{ufn}/genre/phim-bo-canada',
	'Phim Bộ Chile': f'{ufn}/genre/phim-bo-chile',
	'Phim Bộ Colombia': f'{ufn}/genre/phim-bo-colombia',
	'Phim Bộ Đài Loan': f'{ufn}/genre/phim-bo-dai-loan',
	'Phim Bộ Đan Mạch': f'{ufn}/genre/phim-bo-dan-mach',
	'Phim Bộ Đức': f'{ufn}/genre/phim-bo-duc',
	'Phim Bộ Hà Lan': f'{ufn}/genre/phim-bo-ha-lan',
	'Phim Bộ Hàn': f'{ufn}/genre/korean-series',
	'Phim Bộ Hongkong': f'{ufn}/genre/hongkong-series',
	'Phim Bộ Iceland': f'{ufn}/genre/phim-bo-iceland',
	'Phim Bộ Ireland': f'{ufn}/genre/phim-bo-ireland',
	'Phim Bộ Israel': f'{ufn}/genre/phim-bo-israel',
	'Phim Bộ Jordan': f'{ufn}/genre/phim-bo-jordan',
	'Phim Bộ Mexico': f'{ufn}/genre/phim-bo-mexico',
	'Phim Bộ Mỹ': f'{ufn}/genre/us-tv-series',
	'Phim Bộ Na Uy': f'{ufn}/genre/phim-bo-na-uy',
	'Phim Bộ Nam Phi': f'{ufn}/genre/phim-bo-nam-phi',
	'Phim Bộ New Zealand': f'{ufn}/genre/phim-bo-new-zealand',
	'Phim Bộ Nga': f'{ufn}/genre/phim-bo-nga',
	'Phim Bộ Nhật Bản': f'{ufn}/genre/phim-bo-nhat-ban',
	'Phim Bộ Phần Lan': f'{ufn}/genre/phim-bo-phan-lan',
	'Phim Bộ Pháp': f'{ufn}/genre/phim-bo-phap',
	'Phim Bộ Philippines': f'{ufn}/genre/phim-bo-philippines',
	'Phim Bộ Romania': f'{ufn}/genre/phim-bo-romania',
	'Phim Bộ Singapo': f'{ufn}/genre/phim-bo-singapo',
	'Phim Bộ Tây Ban Nha': f'{ufn}/genre/phim-bo-tay-ban-nha',
	'Phim Bộ Thái Lan': f'{ufn}/genre/phim-bo-thai-lan',
	'Phim Bộ Thổ Nhĩ Kỳ': f'{ufn}/genre/phim-bo-tho-nhi-ky',
	'Phim Bộ Thụy Điển': f'{ufn}/genre/phim-bo-thuy-dien',
	'Phim Bộ Trung Quốc': f'{ufn}/genre/phim-bo-trung-quoc',
	'Phim Bộ Việt Nam': f'{ufn}/genre/phim-bo-viet-nam',
	'Phim Bộ Ý': f'{ufn}/genre/phim-bo-y'
}
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/tvhd.png'
		item.set_callback(thuvienhd_page, f'{dulieu[k]}/page/', 1)
		yield item
@Route.register
def tvhd_nhac(plugin):
	dulieu = {
	'Mới nhất':f'{ufn}/genre/music',
	'Chương Trình Xuân': f'{ufn}/genre/chuong_trinh-xuan',
	'Lossless': f'{ufn}/genre/lossless',
	'MV Châu Á': f'{ufn}/genre/wp-chau-a',
	'MV Quốc Tế': f'{ufn}/genre/wp-quoc-te',
	'MV Việt Nam': f'{ufn}/genre/wp-viet-nam'
}
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/tvhd.png'
		item.set_callback(thuvienhd_page, f'{dulieu[k]}/page/', 1)
		yield item
@Route.register
def thuvienhd_linktk(plugin, url=None):
	yield []
	if url is None:
		pass
	else:
		try:
			respx = getlink(url, url, 1000)
			if (respx is not None):
				idk = re.search(r"thuvienhd.xyz/\?p=(\d+)", respx.text)
				t = f'{ufn}/?feed=fsharejson&id={idk[1]}'
				resp = getlink(t, t, 1000)
				if (resp is not None) and resp.json()['link']:
					d = resp.json()
					anh = d['image']
					mota = d['description']
					title = d['title']
					yield gioithieu(title, mota, anh)
					dl = d['link']
					urls = [k['link'] for k in dl if 'fshare.vn' in k['link']]
					length = len(urls)
					if length>0:
						with ThreadPoolExecutor(length) as ex:
							results = ex.map(process_fs, urls)
						for (link, data) in results:
							if data is not None:
								item = Listitem()
								item.label = data[0]
								item.info['plot'] = f'{mota}\nNguồn: {ufn}'
								item.info['trailer'] = yttk(title)
								item.art['thumb'] = item.art['poster'] = anh
								item.context.script(Script.ref('/resources/lib/mkd/onfshare/ifshare:tfavo'), 'Thêm vào Fshare Favorite', link)
								if 'folder' in link:
									item.info['mediatype'] = 'tvshow'
									item.set_callback(Route.ref('/resources/lib/mkd/onfshare/ifshare:index_fs'), link, 0, anh)
								else:
									item.info['mediatype'] = 'episode'
									item.info['size'] = data[1]
									if Script.setting.get_string('taifshare') == 'true':
										item.context.script(Script.ref('/resources/lib/download:downloadfs'), 'Tải về', link)
									item.set_callback(Resolver.ref('/resources/lib/kedon:play_fs'), link, data[0])
								yield item
					else:
						yield quangcao()
				else:
					yield quangcao()
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def thuvienhd_page(plugin, url=None, next_page=None):
	yield []
	if any((url is None, next_page is None)):
		pass
	else:
		try:
			trangtiep = f'{url}{next_page}'
			resp = getlink(trangtiep, trangtiep, 1000)
			if (resp is not None):
				soup = BeautifulSoup(resp.text, 'html.parser')
				s1 = [k['id'].split('-')[1] for k in soup.select('div.items article')]
				s2 = soup.select('div.pagination a')
				length = len(s1)
				if length>0:
					with ThreadPoolExecutor(length) as ex:
						results = ex.map(process_url, s1)
					for (l, data) in results:
						if data is not None:
							item = Listitem()
							item.label = data[0]
							item.info['plot'] = f'{data[2]}\nNguồn: {ufn}'
							item.info['mediatype'] = 'tvshow'
							item.info['trailer'] = yttk(data[0])
							item.art['thumb'] = item.art['poster'] = data[1]
							item.set_callback(thuvienhd_link, l)
							yield item
					for checkpage in s2:
						if str(next_page + 1) in checkpage.get_text(strip=True):
							item1 = Listitem()
							item1.label = f'Trang {next_page + 1}'
							item1.info['mediatype'] = 'tvshow'
							item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
							item1.set_callback(thuvienhd_page, url, next_page + 1)
							yield item1
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def thuvienhd_link(plugin, idk=None):
	yield []
	if idk is None:
		pass
	else:
		try:
			t = f'{ufn}/?feed=fsharejson&id={idk}'
			resp = getlink(t, t, 1000)
			if (resp is not None) and resp.json()['link']:
				d = resp.json()
				anh = d['image']
				mota = d['description']
				title = d['title'].replace('&&','-')
				yield gioithieu(title, mota, anh)
				dl = d['link']
				urls = [k['link'] for k in dl if 'fshare.vn' in k['link']]
				length = len(urls)
				if length>0:
					with ThreadPoolExecutor(length) as ex:
						results = ex.map(process_fs, urls)
					for (link, data) in results:
						if data is not None:
							item = Listitem()
							item.label = data[0]
							item.info['plot'] = f'{mota}\nNguồn: {ufn}'
							item.info['trailer'] = yttk(title)
							item.art['thumb'] = item.art['poster'] = anh
							item.context.script(Script.ref('/resources/lib/mkd/onfshare/ifshare:tfavo'), 'Thêm vào Fshare Favorite', link)
							if 'folder' in link:
								item.info['mediatype'] = 'tvshow'
								item.set_callback(Route.ref('/resources/lib/mkd/onfshare/ifshare:index_fs'), link, 0, anh)
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