from codequick import Route, Script, Listitem
@Route.register
def index_phim(plugin):
	yield Listitem.search(Route.ref('/resources/lib/mkd/onfshare/timfshare:search_freefilm'))
	streams = [
		('ApiiOnline', 'https://raw.githubusercontent.com/kenvnm/kvn/main/apiionline.png', '/resources/lib/mkd/onphim/apiionline:index_apiionline'),
		('OPhim', 'https://raw.githubusercontent.com/kenvnm/kvn/main/ophim.png', '/resources/lib/mkd/onphim/ophim:index_ophim'),
		('NguonC', 'https://raw.githubusercontent.com/kenvnm/kvn/main/nguonc.png', '/resources/lib/mkd/onphim/nguonc:index_nguonc'),
		('KKphim', 'https://raw.githubusercontent.com/kenvnm/kvn/main/kkphim.png', '/resources/lib/mkd/onphim/kkphim:index_kkphim'),
		('PhimMoi', 'https://raw.githubusercontent.com/kenvnm/kvn/main/phimmoi.png', '/resources/lib/mkd/onphim/phimmoi:index_phimmoi'),
		('Bluphim', 'https://raw.githubusercontent.com/kenvnm/kvn/main/bluphim.png', '/resources/lib/mkd/onphim/bluphim:index_bluphim'),
		('AnimeHay', 'https://raw.githubusercontent.com/kenvnm/kvn/main/anime47.png', '/resources/lib/mkd/onphim/anime47:index_anime47'),
		('Fmovies', 'https://raw.githubusercontent.com/kenvnm/kvn/main/fmovi.png', '/resources/lib/mkd/onphim/fmovies:index_fm'),
		('FilmPlus', 'https://raw.githubusercontent.com/kenvnm/kvn/main/onstream.png', '/resources/lib/mkd/onphim/mdb:index_mdb')
	]
	T = {'Phimtonghop': 'http://iptv.pro.vn/phimiptv',
	'ThuvienHDle': 'https://hqth.me/phimlevip2',
	'ThuvienHDbo': 'https://hqth.me/phimbovip2',
	'ThuvienCinele': 'https://hqth.me/phimlevip',
	'ThuvienCinebo': 'https://hqth.me/phimbovip',
	'Ophimle': 'https://hqth.me/ophimle',
	'Ophimbo': 'https://hqth.me/ophimbo',
	'Phimmoile': 'https://hqth.me/phimle',
	'Phimmoibo': 'https://hqth.me/phimbo',
	'Phim360': 'https://hqth.me/tv360'}
	for name_key, banner_key, route_key in streams:
		item = Listitem()
		item.label = name_key
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = banner_key
		item.set_callback(Route.ref(route_key))
		yield item
	for k in T:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/iptv.png'
		item.set_callback(Route.ref('/resources/lib/mkd/ontruyenhinh/listiptv:list_iptv'), T[k])
		yield item
	if Script.setting.get_string('kenh18') == 'true':
		yield Listitem.from_dict(**{'label': 'JAVHD',
		'art': {'thumb': 'https://raw.githubusercontent.com/kenvnm/kvn/main/raphd.jpg',
		'poster': 'https://raw.githubusercontent.com/kenvnm/kvn/main/raphd.jpg'},
		'info': {'mediatype':'tvshow'},
		'callback': Route.ref('/resources/lib/mkd/onphim/raphd:index_raphd')})
		yield Listitem.from_dict(**{'label': 'AVDB',
		'art': {'thumb': 'https://raw.githubusercontent.com/kodivietnam/kodivietnam.github.io/main/avdb.jpg',
		'poster': 'https://raw.githubusercontent.com/kodivietnam/kodivietnam.github.io/main/avdb.jpg'},
		'info': {'mediatype':'tvshow'},
		'callback': Route.ref('/resources/lib/mkd/onphim/avdb:index_avdb')})