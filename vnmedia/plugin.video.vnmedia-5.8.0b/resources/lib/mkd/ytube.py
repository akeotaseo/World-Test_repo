from codequick import Route, Listitem
@Route.register
def index_youtube(plugin):
	streams = [
		('TOP VIDEO THỊNH HÀNH', 'https://raw.githubusercontent.com/kenvnm/kvn/main/hot.png', '/resources/lib/mkd/onyoutube/video:youtube_thinhhanh'),
		('TOP ÂM NHẠC THỊNH HÀNH', 'https://raw.githubusercontent.com/kenvnm/kvn/main/nhacyt.png', '/resources/lib/mkd/onyoutube/video:youtube_amnhacthinhhanh')
	]
	yield Listitem.search(Route.ref('/resources/lib/mkd/onyoutube/tim:search_youtube'))
	for name_key, banner_key, route_key in streams:
		i = Listitem()
		i.label = name_key
		i.info['mediatype'] = 'tvshow'
		i.art['thumb'] = i.art['poster'] = banner_key
		i.set_callback(Route.ref(route_key))
		yield i