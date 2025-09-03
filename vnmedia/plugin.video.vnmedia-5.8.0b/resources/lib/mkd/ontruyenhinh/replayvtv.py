from codequick import Route, Listitem
from datetime import date, timedelta
@Route.register
def index_vtv(plugin):
	n1 = date.today()
	for i in range(30):
		n = n1-timedelta(i)
		h = n.strftime('%d/%m/%Y')
		item = Listitem()
		item.label = h
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/lua-cho-tivi-cho-gia-dinh-1.jpg'
		item.set_callback(Route.ref('/resources/lib/mkd/ontruyenhinh/vtvgo:list_vtv'), n, h)
		yield item