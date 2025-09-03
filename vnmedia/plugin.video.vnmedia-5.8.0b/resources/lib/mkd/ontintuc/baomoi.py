from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao
from concurrent.futures import ThreadPoolExecutor
import re
ubm = 'http://lite.baomoi.com'
def get_info_baomoi(idbm, idp):
	url = f'{ubm}/_next/data/{idbm}/content/detail/{idp}.json'
	r = getlink(url, url, -1)
	try:
		k = r.json()['pageProps']['resp']['data']['content']
		name = k['title']
		info = k['description']
		img = k['thumb']
		linkplay = k['speechs'][0]['streamingUrl']
		return (name, info, img, linkplay)
	except:
		return None
def process_url(idbm, idp):
	try:
		data = get_info_baomoi(idbm, idp)
		return data
	except:
		return None
@Route.register
def index_baomoi(plugin):
	dulieu = {'Tin Nóng':'home',
	'Tin mới':'new',
	'Thế giới':'the-gioi',
	'Xã hội':'xa-hoi',
	'Văn hoá':'van-hoa',
	'Kinh tế':'kinh-te',
	'Giáo dục':'giao-duc',
	'Thể thao':'the-thao',
	'Giải trí':'giai-tri',
	'Pháp luật':'phap-luat',
	'Công nghệ':'khoa-hoc-cong-nghe',
	'Khoa học':'khoa-hoc',
	'Đời sống':'doi-song',
	'Xe cộ':'xe-co',
	'Nhà đất':'nha-dat'}
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/news.png'
		item.set_callback(list_baomoi, dulieu[k])
		yield item
@Route.register
def list_baomoi(plugin, ten=None):
	yield []
	if ten is None:
		pass
	else:
		try:
			r = getlink(ubm,ubm, 300)
			if r is not None and 'buildId":"' in r.text:
				idbm = re.search(r'buildId":"(.*?)"', r.text)[1]
				if (ten == 'home') or (ten == 'new'):
					url = f'{ubm}/_next/data/{idbm}/{ten}.json'
					kq = getlink(url, ubm, -1).json()
					getjs = kq['pageProps']['resp']['data']['content']['items']
				else:
					url = f'{ubm}/_next/data/{idbm}/category/{ten}.json'
					kq = getlink(url, ubm, -1).json()
					getjs = kq['pageProps']['resp']['data']['content']['sections'][1]['items']
				idp = [k['id'] for k in getjs if 'title' in k and 'id' in k]
				length = len(idp)
				if length>0:
					with ThreadPoolExecutor(length) as ex:
						results = ex.map(process_url, [idbm]*length, idp)
					for k in results:
						if k is not None:
							item = Listitem()
							item.label = k[0]
							item.info['mediatype'] = 'episode'
							item.info['plot'] = f'{k[1]}\nNguồn: {ubm}'
							item.art['thumb'] = item.art['poster'] = k[2]
							item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), k[3], k[0])
							yield item
				else:
					yield quangcao()
		except:
			yield quangcao()