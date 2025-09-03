from codequick import Route, Listitem
@Route.register
def index_acestream(plugin):
	dulieu = {
	'Khampha':'http://note.hqth.me/raw/ace-45692',
	'NguyenSocTom':'https://raw.githubusercontent.com/soctom113/acestream/main/AceTV.md'
	}
	streams = [
		('Livetv.sx', 'https://raw.githubusercontent.com/kenvnm/kvn/main/acestream.png', '/resources/lib/mkd/onthethao/livetvxs:index_livetvxs'),
		('Streamthunder.org', 'https://raw.githubusercontent.com/kenvnm/kvn/main/acestream.png', '/resources/lib/mkd/onthethao/streamthunder:index_streamthunder'),
		('Highlights365.com', 'https://raw.githubusercontent.com/kenvnm/kvn/main/logo_header.png', '/resources/lib/mkd/onthethao/hl365:index_highlights365')
	]
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/acestream.png'
		item.set_callback(Route.ref('/resources/lib/mkd/ontruyenhinh/listiptv:list_iptv'), dulieu[k])
		yield item
	for name_key, banner_key, route_key in streams:
		i = Listitem()
		i.label = name_key
		i.info['mediatype'] = 'tvshow'
		i.art['thumb'] = i.art['poster'] = banner_key
		i.set_callback(Route.ref(route_key))
		yield i