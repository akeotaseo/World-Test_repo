from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlinkweb, replace_all, quangcao
from urllib.parse import quote_plus
from xbmcgui import Dialog
import re
thaythe = {'\\"':'','\\u0026':'&'}
@Route.register
def search_youtube(plugin, search_query=None):
	yield []
	if search_query is None:
		pass
	else:
		try:
			search_query = quote_plus(search_query)
			url = f'https://www.youtube.com/results?gl=VN&hl=vi&search_query={search_query}'
			resp = getlinkweb(url, url, 7200)
			if (resp is not None):
				sre1 = re.compile(r'text":"(.*?)"}')
				sre2 = re.compile(r'videoId":"(.*?)"')
				sre3 = re.compile(r'"simpleText":"(.*?)"}')
				sre4 = re.compile(r'webCommandMetadata":{"url":"(.*?)"')
				sre5 = re.compile(r'"url":"(.*?)"')
				kq = replace_all(thaythe, resp.text)
				if 'videoRenderer' in kq:
					listplay = re.findall(r'videoRenderer(.*?)accessibility', kq)
					for k in listplay:
						item = Listitem()
						tenvd = sre1.search(k)[1]
						idvd = sre2.search(k)[1]
						anhvd = f'https://i.ytimg.com/vi/{idvd}/sddefault.jpg'
						item.label = tenvd
						item.info['mediatype'] = 'episode'
						item.art['thumb'] = item.art['poster'] = anhvd
						item.set_path(f'plugin://plugin.video.youtube/play/?video_id={idvd}')
						yield item
				elif 'playlistRenderer' in kq:
					listplay1 = re.findall(r'playlistRenderer(.*?)webPageType', kq)
					for k1 in listplay1:
						item1 = Listitem()
						tenvd1 = sre3.search(k1)[1]
						idvd1 = sre4.search(k1)[1]
						anhvd1 = f'https://i.ytimg.com/vi/{idvd1}/sddefault.jpg'
						item1.label = tenvd
						item1.info['mediatype'] = 'tvshow'
						item1.art['thumb'] = item1.art['poster'] = anhvd1
						item1.set_path(Route.ref('/resources/lib/mkd/onyoutube/video:youtube_tatcavideo'), f'{url}{idvd1}')
						yield item1
				elif 'channelRenderer' in kq:
					listplay2 = re.findall(r'channelRenderer(.*?)webPageType', kq)
					for k2 in listplay2:
						item2 = Listitem()
						tenvd2 = sre3.search(k2)[1]
						idvd2 = sre5.search(k2)[1]
						anhvd2 = f'https://i.ytimg.com/vi/{idvd2}/sddefault.jpg'
						item2.label = tenvd2
						item2.info['mediatype'] = 'tvshow'
						item2.art['thumb'] = item2.art['poster'] = f'https:{anhvd2}'
						item2.set_path(Route.ref('/resources/lib/mkd/onyoutube/video:youtube_kenh'), f'{url}{idvd2}')
						yield item2
			else:
				yield quangcao()
		except:
			yield quangcao()
@Resolver.register
def trailer_youtube(plugin, search_query):
	try:
		b = quote_plus(search_query)
		url = f'https://www.youtube.com/results?gl=VN&hl=vi&search_query=Trailer+{b}'
		resp = getlinkweb(url, url, 7200)
		if (resp is not None) and ('videoRenderer' in resp.text):
			sre1 = re.compile(r'text":"(.*?)"}')
			sre2 = re.compile(r'videoId":"(.*?)"')
			kq = replace_all(thaythe, resp.text)
			listplay = re.findall(r'videoRenderer(.*?)accessibility', kq)
			links = ((sre1.search(k)[1], f'plugin://plugin.video.youtube/play/?video_id={sre2.search(k)[1]}') for k in listplay)
			titles, urls = zip(*links)
			ret = Dialog().select(search_query, titles)
			if ret < 0:
				return False
			else:
				return urls[ret]
	except:
		pass