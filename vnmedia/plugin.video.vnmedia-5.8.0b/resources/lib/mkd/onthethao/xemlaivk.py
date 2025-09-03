from codequick import Route, Listitem
@Route.register
def index_xemlaivk(plugin):
	streams = [
		('Replay Sport - TIENGRUOI', 'https://raw.githubusercontent.com/kenvnm/kvn/main/fullmatch.png', 'xemlai'),
		('Tóm tắt trận đấu - TIENGRUOI', 'https://raw.githubusercontent.com/kenvnm/kvn/main/highlights.png', 'highlight')
	]
	for name_key, banner_key, url_key in streams:
		item = Listitem()
		item.label = name_key
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = banner_key
		item.set_callback(Route.ref('/resources/lib/mkd/onthethao/phut90:xemlai_90p'), url_key, 1)
		yield item
	yield xemlai90ptc()
def xemlai90ptc():
	item = Listitem()
	item.label = 'Replay Sport - THAPCAM'
	item.info['mediatype'] = 'tvshow'
	item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/fullmatch.png'
	item.set_callback(Route.ref('/resources/lib/mkd/onthethao/thapcam:xemlai_tc'), 1)
	return item