from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, getlinkss, useragentdf, quangcao, stream, referer
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import re
phim_nhanh = 'https://xphim1080.com'
def dm(hr):
	if hr.startswith('/'):
		b= f'{phim_nhanh}{hr}'
	elif hr.startswith('http'):
		b= hr
	else:
		b= f'{phim_nhanh}/{hr}'
	return b
def get_info_1080(x, img):
	r = getlink(x,x,-1)
	try:
		soup = BeautifulSoup(r.content, 'html.parser')
		soups = soup.select('div.film-info')
		idp = soup.select_one('div.container')['data-id']
		for k in soups:
			try:
				ten = k.select_one('h1.film-info-title').get_text(strip=True)
			except:
				pass
			try:
				mota = k.select_one('div.film-info-description').get_text(strip=True)
			except:
				mota = ten
			return (ten, img, mota, idp)
	except:
		return None
def process_url(url, img):
	try:
		data = get_info_1080(url, img)
		return url, data
	except:
		return url, None
def decode_1080(e, t):
	a = ''
	for i in range(len(e)):
		r = ord(e[i])
		o = r ^ t
		a += chr(o)
	return a
def extract_opt(r):
	try:
		opt_encode_match = re.search(r'"opt":"([^"]+)"', r.text)
		deo = decode_1080(opt_encode_match[1], 69).strip()
		opt = deo.replace("0uut$", "_").replace("index.m3u8", "3000k/hls/mixed.m3u8")
		return opt
	except:
		return ''
def extract_hls(r):
	try:
		hls_encode_match = re.search(r'{"hls":"([^"]+)"', r.text)
		deh = decode_1080(hls_encode_match[1], 69).strip()
		return deh
	except:
		return ''
def extract_fb_src(r):
	try:
		fb_match = re.search(r'"fb":\[{"src":"([^"]+)"', r.text)
		fb = fb_match[1].replace("\\/", "/")
		return fb
	except:
		return ''
@Route.register
def search_1080(plugin, search_query=None):
	yield []
	if search_query is None:
		pass
	else:
		try:
			next_page = 1
			sr = quote_plus(search_query)
			url = f'{phim_nhanh}/tim-kiem/{sr}'
			trangtiep = f'{url}?page={next_page}'
			r = getlink(trangtiep, url, 1800)
			if (r is not None) and ('tray-item' in r.text):
				soup = BeautifulSoup(r.content, 'html.parser')
				soups = soup.select('div.tray-item a')
				urls = [(dm(k['href']), k.select_one('img')['data-src']) for k in soups]
				length = len(urls)
				if length>0:
					with ThreadPoolExecutor(length) as ex:
						results = ex.map(process_url, [k[0] for k in urls], [k[1] for k in urls])
					for (l, data) in results:
						if data is not None:
							item = Listitem()
							anhphim = data[1]
							motaphim = data[2]
							idp = data[3]
							item.label = data[0]
							item.info['plot'] = motaphim
							item.info['mediatype'] = 'tvshow'
							item.art['thumb'] = item.art['poster'] = anhphim
							item.set_callback(episode_1080, idp, anhphim, motaphim, l)
							yield item
					if f'?page={str(int(next_page) + 1)}' in r.text:
						item1 = Listitem()
						item1.label = f'Trang {str(int(next_page) + 1)}'
						item1.info['mediatype'] = 'tvshow'
						item1.art['thumb'] = item1.art['poster'] = 'https://mi3s.top/thumb/next.png'
						item1.set_callback(ds_1080, url, str(int(next_page) + 1))
						yield item1
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def index_1080(plugin):
	yield Listitem.search(search_1080)
	T = {'Thể loại': tl_1080,
	'Quốc gia': qg_1080}
	dulieu = {
	'Phim mới': f'{phim_nhanh}/tap-moi-nhat',
	'Phim đề cử': f'{phim_nhanh}/phim-de-cu',
	'Phim lẻ': f'{phim_nhanh}/phim-le',
	'Phim bộ': f'{phim_nhanh}/phim-bo',
	'Chiếu rạp': f'{phim_nhanh}/phim-chieu-rap',
	'Hoạt hình': f'{phim_nhanh}/the-loai/hoat-hinh',
	'Hôm nay xem gì': f'{phim_nhanh}/hom-nay-xem-gi'
	}
	for b in T:
		i = Listitem()
		i.label = b
		i.info['mediatype'] = 'tvshow'
		i.art['thumb'] = i.art['poster'] = 'https://mi3s.top/thumb/phim/phim1080.png'
		i.set_callback(T[b])
		yield i
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://mi3s.top/thumb/phim/phim1080.png'
		item.set_callback(ds_1080, dulieu[k], 1)
		yield item
@Route.register
def tl_1080(plugin):
	dulieu = {
	'Hành động': f'{phim_nhanh}/the-loai/hanh-dong',
	'Phiêu lưu': f'{phim_nhanh}/the-loai/phieu-luu',
	'Kinh dị': f'{phim_nhanh}/the-loai/kinh-di',
	'Tình cảm': f'{phim_nhanh}/the-loai/tinh-cam',
	'Hoạt hình': f'{phim_nhanh}/the-loai/hoat-hinh',
	'Võ thuật': f'{phim_nhanh}/the-loai/vo-thuat',
	'Hài hước': f'{phim_nhanh}/the-loai/hai-huoc',
	'Tâm lý': f'{phim_nhanh}/the-loai/tam-ly',
	'Viễn tưởng': f'{phim_nhanh}/the-loai/vien-tuong',
	'Thần thoại': f'{phim_nhanh}/the-loai/than-thoai',
	'Chiến tranh': f'{phim_nhanh}/the-loai/chien-tranh',
	'Cổ trang': f'{phim_nhanh}/the-loai/co-trang',
	'Âm nhạc': f'{phim_nhanh}/the-loai/am-nhac',
	'Hình sự': f'{phim_nhanh}/the-loai/hinh-su',
	'TV Show': f'{phim_nhanh}/the-loai/tv-show',
	'Khoa học': f'{phim_nhanh}/the-loai/khoa-hoc',
	'Tài liệu': f'{phim_nhanh}/the-loai/tai-lieu',
	'Other': f'{phim_nhanh}/the-loai/other',
	'Lịch sử': f'{phim_nhanh}/the-loai/lich-su',
	'Gia đình': f'{phim_nhanh}/the-loai/gia-dinh',
	'Thể thao': f'{phim_nhanh}/the-loai/the-thao',
	'Kiếm hiệp': f'{phim_nhanh}/the-loai/kiem-hiep',
	'Kịch tính': f'{phim_nhanh}/the-loai/kich-tinh',
	'Bí ẩn': f'{phim_nhanh}/the-loai/bi-an',
	'Tiểu sử': f'{phim_nhanh}/the-loai/tieu-su',
	'Thanh xuân': f'{phim_nhanh}/the-loai/thanh-xuan',
	'Học đường': f'{phim_nhanh}/the-loai/hoc-duong',
	'Huyền huyễn': f'{phim_nhanh}/the-loai/huyen-huyen',
	'Tiên hiệp': f'{phim_nhanh}/the-loai/tien-hiep',
	'Đam mỹ': f'{phim_nhanh}/the-loai/dam-my',
	'Trinh thám': f'{phim_nhanh}/the-loai/trinh-tham',
	'Gay căng': f'{phim_nhanh}/the-loai/gay-can',
	'Động vật': f'{phim_nhanh}/the-loai/dong-vat',
}
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://mi3s.top/thumb/phim/phim1080.png'
		item.set_callback(ds_1080, dulieu[k], 1)
		yield item
@Route.register
def qg_1080(plugin):
	dulieu = {
	'Trung Quốc': f'{phim_nhanh}/phim-trung-quoc',
	'Hàn Quốc': f'{phim_nhanh}/phim-han-quoc',
	'Đài Loan': f'{phim_nhanh}/phim-dai-loan',
	'Mỹ': f'{phim_nhanh}/phim-my',
	'Châu Âu': f'{phim_nhanh}/phim-chau-au',
	'Nhật Bản': f'{phim_nhanh}/phim-nhat-ban',
	'Hồng Kông': f'{phim_nhanh}/phim-hong-kong',
	'Thái Lan': f'{phim_nhanh}/phim-thai-lan',
	'Châu Á': f'{phim_nhanh}/phim-chau-a',
	'Ấn Độ': f'{phim_nhanh}/phim-an-do',
	'Pháp': f'{phim_nhanh}/phim-phap',
	'Anh': f'{phim_nhanh}/phim-anh',
	'Canada': f'{phim_nhanh}/phim-canada',
	'Đức': f'{phim_nhanh}/phim-duc',
	'Tây Ban Nha': f'{phim_nhanh}/phim-tay-ban-nha',
	'Nga': f'{phim_nhanh}/phim-nga',
	'Úc': f'{phim_nhanh}/phim-uc',
	'Khác': f'{phim_nhanh}/phim-khac',
}
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://mi3s.top/thumb/phim/phim1080.png'
		item.set_callback(ds_1080, dulieu[k], 1)
		yield item
@Route.register
def ds_1080(plugin, url=None, next_page=None):
	yield []
	if any((url is None,next_page is None)):
		pass
	else:
		try:
			trangtiep = f'{url}&page={next_page}' if '?' in url else f'{url}?page={next_page}'
			r = getlink(trangtiep, url, 1000)
			if (r is not None) and ('tray-item' in r.text):
				soup = BeautifulSoup(r.content, 'html.parser')
				soups = soup.select('div.tray-item a')
				urls = [(dm(k['href']), k.select_one('img')['data-src']) for k in soups]
				length = len(urls)
				if length>0:
					with ThreadPoolExecutor(length) as ex:
						results = ex.map(process_url, [k[0] for k in urls], [k[1] for k in urls])
					for (l, data) in results:
						if data is not None:
							item = Listitem()
							anhphim = data[1]
							motaphim = data[2]
							idp = data[3]
							item.label = data[0]
							item.info['plot'] = motaphim
							item.info['mediatype'] = 'tvshow'
							item.art['thumb'] = item.art['poster'] = anhphim
							item.set_callback(episode_1080, idp, anhphim, motaphim, l)
							yield item
					if f'?page={str(int(next_page) + 1)}' in r.text:
						item1 = Listitem()
						item1.label = f'Trang {str(int(next_page) + 1)}'
						item1.info['mediatype'] = 'tvshow'
						item1.art['thumb'] = item1.art['poster'] = 'https://mi3s.top/thumb/next.png'
						item1.set_callback(ds_1080, url, str(int(next_page) + 1))
						yield item1
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def episode_1080(plugin, idp=None, img=None, info=None, dm=None):
	yield []
	if any((idp is None,img is None,info is None,dm is None)):
		pass
	else:
		try:
			headers = {'Referer':dm,'User-Agent': useragentdf,'Content-Type':'application/json','Cookie': 'phimnhanh=%3D','X-Requested-With': 'XMLHttpRequest'}
			r = getlinkss(f'{phim_nhanh}/api/v2/films/{idp}/episodes?sort=name', headers)
			if 'id' in r.text:
				for k in r.json()['data']:
					edp = k['id']
					tap = k['full_name']
					phim = k['film_name']
					tenm = f'{tap} - {phim}'
					item = Listitem()
					item.label = tenm
					item.info['mediatype'] = 'tvshow'
					item.info['plot'] = info
					item.art['thumb'] = item.art['poster'] = img
					item.set_callback(play_1080, idp, edp, tenm, dm, img, info)
					yield item
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def play_1080(plugin, idp=None, eid=None, title=None, dm=None, img=None, info=None):
	yield []
	if any((idp is None,eid is None,title is None,dm is None,img is None,info is None)):
		pass
	else:
		try:
			headers = {'Referer':dm,'User-Agent': useragentdf,'Content-Type':'application/json','Cookie': 'phimnhanh=%3D','X-Requested-With': 'XMLHttpRequest'}
			r = getlinkss(f'{phim_nhanh}/api/v2/films/{idp}/episodes/{eid}', headers)
			with ThreadPoolExecutor(3) as ex:
				f1 = ex.submit(extract_hls, r)
				f2 = ex.submit(extract_opt, r)
				f3 = ex.submit(extract_fb_src, r)
				h = f1.result()
				o = f2.result()
				f = f3.result()
			dulieu = {
				f'HS - {title}': h,
				f'OP - {title}': o,
				f'FB - {title}': f
				}
			for k in dulieu:
				if 'http' in dulieu[k]:
					i = Listitem()
					i.label = k
					i.info['plot'] = info
					i.info['mediatype'] = 'episode'
					i.art['thumb'] = i.art['poster'] = img
					i.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), f'{stream(dulieu[k])}{referer(dm)}', k)
					yield i
		except:
			yield quangcao()