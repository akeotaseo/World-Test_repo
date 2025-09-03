from codequick import Route, Listitem
@Route.register
def index_giaitri(plugin):
	dulieu = {
	'Video Ngắn':1000,
	'Hài':7,
	'Ngắm':1042,
	'Vui độc lạ':1011,
	'Vlogs':1051,
	'TV Show':1039
	}
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/Emoji-mat-cuoi-he-rang.jpg'
		item.set_callback(Route.ref('/resources/lib/mkd/ontintuc/mocha:index_mocha'), dulieu[k], 0)
		yield item