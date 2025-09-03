from codequick import Route, Listitem, Script, Resolver
from resources.lib.kedon import search_history_get, search_history_clear, fu, get_info_fs, yttk, __addonnoti__, quangcao, search_history_save
from urllib.parse import quote_plus
from codequick.utils import keyboard
import re
def get_user_input():
	shorturl = Script.setting.get_string('shorten_host')
	search_term = keyboard(shorturl.upper(),'',False)
	return search_term
@Route.register
def index_number(plugin):
	yield PlayNumberCode()
	yield Listitem.from_dict(**{'label': 'MÃ CODE gần đây',
	'art': {'thumb': 'https://raw.githubusercontent.com/kenvnm/kvn/main/watched.png',
	'poster': 'https://raw.githubusercontent.com/kenvnm/kvn/main/watched.png'},
	'callback': index_codeganday})
@Route.register
def index_codeganday(plugin):
	yield []
	b = search_history_get()
	if b:
		for m in b:
			item = Listitem()
			item.label = m.split('/')[-1]
			item.info['mediatype'] = 'tvshow'
			item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/numbercode.png'
			item.context.script(Script.ref('/resources/lib/kedon:remove_search_history'), 'Xoá khỏi lịch sử CODE', m)
			item.set_callback(dulieucode, m)
			yield item
		yield Listitem.from_dict(**{'label': 'Xoá lịch sử CODE',
		'art': {'thumb': 'https://raw.githubusercontent.com/kenvnm/kvn/main/watched.png',
		'poster': 'https://raw.githubusercontent.com/kenvnm/kvn/main/watched.png'},
		'callback': search_history_clear})
@Route.register
def dulieucode(plugin, m=None):
	yield []
	if m is None:
		pass
	else:
		try:
			x = fu(m)
			if 'fshare.vn/folder' in x:
				item = Listitem()
				ten = get_info_fs(x)[0]
				item.label = ten
				item.info['mediatype'] = 'tvshow'
				item.info['plot'] = f'{ten}\nNguồn: https://fshare.vn'
				item.info['trailer'] = yttk(ten)
				imgfs = 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
				item.art['thumb'] = item.art['poster'] = imgfs
				item.context.script(Script.ref('/resources/lib/mkd/onfshare/ifshare:tfavo'), 'Thêm vào Fshare Favorite', x)
				item.set_callback(Route.ref('/resources/lib/mkd/onfshare/ifshare:index_fs'), x, 0, imgfs)
				yield item
			elif 'fshare.vn/file' in x:
				item = Listitem()
				ten = get_info_fs(x)[0]
				item.label = ten
				item.info['size'] = get_info_fs(x)[1]
				item.info['plot'] = f'{ten}\nNguồn: https://fshare.vn'
				item.info['mediatype'] = 'episode'
				item.info['trailer'] = yttk(ten)
				item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
				if Script.setting.get_string('taifshare') == 'true':
					item.context.script(Script.ref('/resources/lib/download:downloadfs'), 'Tải về', x)
				item.context.script(Script.ref('/resources/lib/mkd/onfshare/ifshare:tfavo'), 'Thêm vào Fshare Favorite', x)
				item.set_callback(Resolver.ref('/resources/lib/kedon:play_fs'), x, ten)
				yield item
			else:
				Script.notify(__addonnoti__, 'CODE không đúng')
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def searchnumber(plugin, search_query=None):
	yield []
	if search_query is None:
		pass
	else:
		try:
			shorturl = Script.setting.get_string('shorten_host')
			search_query = get_user_input()
			if search_query == '':
				Script.notify(f'{__addonnoti__} - {shorturl.upper()}', 'Bạn chưa nhập CODE')
				yield quangcao()
			else:
				search_query = quote_plus(search_query)
				z = f'http://{shorturl}/{search_query}'
				search_history_save(z)
				x = fu(z)
				if 'fshare.vn/folder' in x:
					item = Listitem()
					ten = get_info_fs(x)[0]
					item.label = ten
					item.info['mediatype'] = 'tvshow'
					item.info['trailer'] = yttk(ten)
					item.info['plot'] = f'{ten}\nNguồn: https://fshare.vn'
					imgfs = 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
					item.art['thumb'] = item.art['poster'] = imgfs
					item.context.script(Script.ref('/resources/lib/mkd/onfshare/ifshare:tfavo'), 'Thêm vào Fshare Favorite', x)
					item.set_callback(Route.ref('/resources/lib/mkd/onfshare/ifshare:index_fs'), x, 0, imgfs)
					yield item
				elif 'fshare.vn/file' in x:
					item = Listitem()
					ten = get_info_fs(x)[0]
					item.label = ten
					item.info['size'] = get_info_fs(x)[1]
					item.info['mediatype'] = 'episode'
					item.info['trailer'] = yttk(ten)
					item.info['plot'] = f'{ten}\nNguồn: https://fshare.vn'
					item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
					if Script.setting.get_string('taifshare') == 'true':
						item.context.script(Script.ref('/resources/lib/download:downloadfs'), 'Tải về', x)
					item.context.script(Script.ref('/resources/lib/mkd/onfshare/ifshare:tfavo'), 'Thêm vào Fshare Favorite', x)
					item.set_callback(Resolver.ref('/resources/lib/kedon:play_fs'), x, ten)
					yield item
				else:
					Script.notify(__addonnoti__, 'CODE không đúng')
					yield quangcao()
		except:
			yield quangcao()
def PlayNumberCode():
	shorturl = Script.setting.get_string('shorten_host')
	item = Listitem()
	item.label = 'MÃ CODE'
	item.info['mediatype'] = 'tvshow'
	item.info['plot'] = f'Mã CODE được chia sẻ bởi nhóm fb Hội mê phim - máy chủ {shorturl.upper()}'
	item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/numbercode.png'
	item.set_callback(searchnumber, searchnumber)
	return item