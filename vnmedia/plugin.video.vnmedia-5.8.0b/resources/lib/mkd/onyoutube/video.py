from codequick import Route, Listitem
from resources.lib.kedon import getlinkweb, quangcao, replace_all
import re
thaythe = {'\\"':'','\\u0026':'&'}
@Route.register
def youtube_tatcavideo(plugin, url=None):
	yield []
	if url is None:
		pass
	else:
		try:
			resp = getlinkweb(url, url, 3600)
			if (resp is not None):
				sre1 = re.compile(r'{"text":"(.*?)"}')
				sre2 = re.compile(r'"videoId":"(.*?)"')
				kq = replace_all(thaythe, resp.text)
				listplay = re.findall(r'richItemRenderer(.*?)navigationEndpoint', kq)
				for k in listplay:
					item = Listitem()
					idvd = sre2.search(k)[1]
					item.label = sre1.search(k)[1]
					item.info['mediatype'] = 'episode'
					item.art['thumb'] = item.art['poster'] = f'https://i.ytimg.com/vi/{idvd}/sddefault.jpg'
					item.set_path(f'plugin://plugin.video.youtube/play/?video_id={idvd}')
					yield item
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def youtube_thinhhanh(plugin):
	yield []
	try:
		url = 'https://www.youtube.com/feed/trending?gl=VN&hl=vi'
		resp = getlinkweb(url, url, 7200)
		if (resp is not None):
			sre1 = re.compile(r'text":"(.*?)"}')
			sre2 = re.compile(r'videoId":"(.*?)"')
			kq = replace_all(thaythe, resp.text)
			listplay = re.findall(r'videoRenderer(.*?)accessibility', kq)
			for k in listplay:
				item = Listitem()
				idvd = sre2.search(k)[1]
				item.label = sre1.search(k)[1]
				item.info['mediatype'] = 'episode'
				item.art['thumb'] = item.art['poster'] = f'https://i.ytimg.com/vi/{idvd}/sddefault.jpg'
				item.set_path(f'plugin://plugin.video.youtube/play/?video_id={idvd}')
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def youtube_amnhacthinhhanh(plugin):
	yield []
	try:
		url = 'https://www.youtube.com/feed/trending?gl=VN&hl=vi&bp=4gINGgt5dG1hX2NoYXJ0cw%3D%3D'
		resp = getlinkweb(url, url, 7200)
		if (resp is not None):
			sre1 = re.compile(r'text":"(.*?)"}')
			sre2 = re.compile(r'videoId":"(.*?)"')
			kq = replace_all(thaythe, resp.text)
			listplay = re.findall(r'videoRenderer(.*?)accessibility', kq)
			for k in listplay:
				item = Listitem()
				idvd = sre2.search(k)[1]
				item.label = sre1.search(k)[1]
				item.info['mediatype'] = 'episode'
				item.art['thumb'] = item.art['poster'] = f'https://i.ytimg.com/vi/{idvd}/sddefault.jpg'
				item.set_path(f'plugin://plugin.video.youtube/play/?video_id={idvd}')
				yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def youtube_kenh(plugin, url=None):
	yield []
	if url is None:
		pass
	else:
		try:
			item2 = Listitem()
			item2.label = 'Danh sách phát'
			item2.art['thumb'] = item2.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/yt_1200.png'
			item2.set_path(youtube_dslist, f'{url}/playlists')
			item1 = Listitem()
			item1.label = 'Tất cả Video'
			item1.info['mediatype'] = 'tvshow'
			item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/yt_1200.png'
			item1.set_path(youtube_tatcavideo, f'{url}/videos')
			yield item2
			yield item1
			resp = getlinkweb(url, url, 3600)
			if (resp is not None):
				sre1 = re.compile(r'text":"(.*?)"')
				sre2 = re.compile(r'"videoId":"(.*?)"')
				sre3 = re.compile(r'simpleText":"(.*?)"}')
				kq = replace_all(thaythe, resp.text)
				if 'channelVideoPlayerRenderer' in kq:
					listplay0 = re.findall(r'channelVideoPlayerRenderer(.*?)navigationEndpoint', kq)
					for k0 in listplay0:
						item0 = Listitem()
						idvd0 = sre2.search(k0)[1]
						item0.label = sre1.search(k0)[1]
						item0.info['mediatype'] = 'episode'
						item0.art['thumb'] = item0.art['poster'] = f'https://i.ytimg.com/vi/{idvd0}/sddefault.jpg'
						item0.set_path(f'plugin://plugin.video.youtube/play/?video_id={idvd0}')
						yield item0
				listplay = re.findall(r'gridVideoRenderer(.*?)navigationEndpoint', kq)
				for k in listplay:
					item = Listitem()
					idvd = sre2.search(k)[1]
					item.label = sre3.search(k)[1]
					item.info['mediatype'] = 'episode'
					item.art['thumb'] = item.art['poster'] = f'https://i.ytimg.com/vi/{idvd}/sddefault.jpg'
					item.set_path(f'plugin://plugin.video.youtube/play/?video_id={idvd}')
					yield item
			else:
				yield quangcao()
		except:
			yield quangcao()