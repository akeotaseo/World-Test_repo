from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao, stream, referer
@Route.register
def index_mocha(plugin, idk=None, next_page=None):
	yield []
	if any((idk is None,next_page is None)):
		pass
	else:
		try:
			resp = getlink(f'http://apivideo.mocha.com.vn:8081/onMediaBackendBiz/mochavideo/listVideoByCate?categoryid={idk}&limit=50&offset={next_page}0&lastIdStr=&token=', 'http://video.mocha.com.vn/',-1)
			if (resp is not None) and ('data' in resp.text):
				kq = resp.json()
				kl = kq['data']['listVideo']
				for k in kl:
					item = Listitem()
					item.label = k['name']
					item.info['mediatype'] = 'episode'
					if 'playlist' in k['original_path']:
						linkget = k['original_path']
					elif k['list_resolution']:
						linkget = k["list_resolution"][-1]['video_path']
					item.info['plot'] = f"{k['description']}\nNguồn: http://video.mocha.com.vn"
					item.art['thumb'] = item.art['poster'] = k['image_path']
					item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), f'{stream(linkget)}{referer("http://video.mocha.com.vn/")}', k['name'])
					yield item
				item1 = Listitem()
				item1.label = 'Trang tiếp'
				item1.info['mediatype'] = 'tvshow'
				item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
				item1.set_callback(index_mocha, idk, next_page + 5)
				yield item1
			else:
				yield quangcao()
		except:
			yield quangcao()