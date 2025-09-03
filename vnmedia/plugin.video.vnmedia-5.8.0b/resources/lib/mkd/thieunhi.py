from codequick import Resolver, Route, Listitem
from resources.lib.kedon import getlink, quangcao, referer, stream
@Route.register
def index_thieunhi(plugin):
	try:
		resp = getlink(f'http://apivideo.mocha.com.vn:8081/onMediaBackendBiz/mochavideo/listVideoByCate?categoryid=1023&limit=50&offset=00&lastIdStr=&token=', 'http://video.mocha.com.vn/', 1000)
		if (resp is not None):
			kq = resp.json()
			kl = kq['data']['listVideo']
			for k in kl:
				item = Listitem()
				item.label = k['name']
				item.info['mediatype'] = 'episode'
				if 'playlist' in k['original_path']:
					linkget = k['original_path']
				else:
					linkget = k['list_resolution'][-1]['video_path']
				item.info['plot'] = k['description']
				item.art['thumb'] = item.art['poster'] = k['image_path']
				item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), f'{stream(linkget)}{referer("http://video.mocha.com.vn/")}', k['name'])
				yield item
			item1 = Listitem()
			item1.label = 'Trang tiếp'
			item1.info['mediatype'] = 'tvshow'
			item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
			item1.set_callback(index_nextthieunhi, 5)
			yield item1
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def index_nextthieunhi(plugin, next_page=None):
	yield []
	if next_page is None:
		pass
	else:
		try:
			resp = getlink(f'http://apivideo.mocha.com.vn:8081/onMediaBackendBiz/mochavideo/listVideoByCate?categoryid=1023&limit=50&offset={next_page}0&lastIdStr=&token=', 'http://video.mocha.com.vn/', 1000)
			if (resp is not None):
				kq = resp.json()
				kl = kq['data']['listVideo']
				for k in kl:
					item = Listitem()
					item.label = k['name']
					item.info['mediatype'] = 'episode'
					if 'playlist' in k['original_path']:
						linkget = k['original_path']
					else:
						linkget = k['list_resolution'][-1]['video_path']
					item.info['plot'] = k['description']
					item.art['thumb'] = item.art['poster'] = k['image_path']
					item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), f'{stream(linkget)}{referer("http://video.mocha.com.vn/")}', k['name'])
					yield item
				item1 = Listitem()
				item1.label = 'Trang tiếp'
				item1.info['mediatype'] = 'tvshow'
				item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
				item1.set_callback(index_nextthieunhi, next_page + 5)
				yield item1
			else:
				yield quangcao()
		except:
			yield quangcao()