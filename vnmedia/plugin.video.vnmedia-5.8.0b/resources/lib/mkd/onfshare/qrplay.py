from codequick import Script, Route, Listitem, Resolver
from resources.lib.kedon import getlink, getrow, yttk, quangcao, get_last_play, clear_last_played, remove_last_played
from resources.lib.mkd.onfshare.timfshare import get_tkfs1, get_tkfs2, get_tkfs3, get_tkfs4
from concurrent.futures import ThreadPoolExecutor
from xbmcgui import DialogProgress
from urllib.parse import quote_plus, unquote
from json import loads
from random import randint
from codequick.utils import color, bold
import xbmc, re
mv = bold(color('mi3s.top', 'yellow'))
@Route.register
def qrplay(plugin):
	T = {f'Nhấn để lấy mã liên kết với trang {mv}': mplay,
	'Last MPlay Direct': index_played}
	for k in T:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://mi3s.top/thumb/MPlay.jpg'
		item.set_callback(T[k])
		yield item
@Route.register
def mplay(plugin):
	yield []
	try:
		my_number = randint(10000, 99999)
		url = 'https://docs.google.com/spreadsheets/d/11kmgd4cK8Kj7bJ8e8rGfYmgNxUvb1nQWN9S0y-4M3JQ/gviz/tq?gid=1028412373&headers=1'
		dialog = DialogProgress()
		dialog.create(bold(color(my_number, "yellow")), 'Đang lấy dữ liệu...')
		countdown = 1000
		timeout_expired = False
		while countdown > 0:
			if dialog.iscanceled():
				dialog.close()
				yield quangcao()
				break
			resp = getlink(url , url, -1)
			if f'"{my_number}"' in resp.text:
				dialog.close()
				noi = re.search(r'\{.*\}', resp.text)[0]
				m = loads(noi)
				rows = m['table']['rows']
				for row in rows:
					try:
						dulieu = getrow(row['c'][1]).split('|')
						tentrandau = unquote(dulieu[0]).replace('+', ' ')
						kenh = unquote(dulieu[1])
						ten = getrow(row['c'][2])
						if ten == my_number:
							if kenh.startswith('http'):
								if 'fshare.vn/file' in kenh or 'fshare.vn/folder' in kenh:
									item = Listitem()
									item.label = tentrandau
									item.info['mediatype'] = 'episode'
									item.art['thumb'] = item.art['poster'] = 'https://mi3s.top/thumb/MPlay.jpg'
									item.set_callback(Resolver.ref('/resources/lib/kedon:play_fs'), kenh, tentrandau)
									yield item
								else:
									item = Listitem()
									item.label = tentrandau
									item.info['mediatype'] = 'episode'
									item.art['thumb'] = item.art['poster'] = 'https://mi3s.top/thumb/MPlay.jpg'
									item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), kenh, tentrandau)
									yield item
							else:
								search_query = quote_plus(kenh)
								with ThreadPoolExecutor(4) as ex:
									f1 = ex.submit(get_tkfs1, search_query)
									f2 = ex.submit(get_tkfs2, search_query)
									f3 = ex.submit(get_tkfs3, search_query)
									f4 = ex.submit(get_tkfs4)
									result_f1 = f1.result()
									result_f2 = f2.result()
									result_f3 = f3.result()
									result_f4 = f4.result()
								dialog.update(50)
								try:
									if result_f3 is not None and result_f4 is not None:
										if result_f3.content != result_f4.content:
											kqtvhd = result_f3.json()
											for t in kqtvhd:
												tenmm = t['title'].replace('&&','-')
												item = Listitem()
												item.label = tenmm
												item.info['plot'] = t['title']
												item.info['mediatype'] = 'tvshow'
												item.info['trailer'] = yttk(tenmm)
												item.art['thumb'] = item.art['poster'] = t['image']
												item.set_callback(Route.ref('/resources/lib/mkd/onfshare/thuvienhd:thuvienhd_link'), t['id'])
												yield item
								except:
									if result_f3 is not None and result_f4 is not None:
										if result_f3.content != result_f4.content:
											text = result_f3.text
											data = re.sub(r'<(.*?)\n','',text)
											jsm = loads(data)
											for t in jsm:
												tenmm = t['title'].replace('&&','-')
												item = Listitem()
												item.label = tenmm
												item.info['plot'] = t['title']
												item.info['mediatype'] = 'tvshow'
												item.info['trailer'] = yttk(tenmm)
												item.art['thumb'] = item.art['poster'] = t['image']
												item.set_callback(Route.ref('/resources/lib/mkd/onfshare/thuvienhd:thuvienhd_link'), t['id'])
												yield item
								try:
									x = result_f1.json()['items']
									for m in x:
										path = m['path']
										if '/file/' in path:
											item = Listitem()
											item.label = m['label']
											link = path.split('&url=')[1]
											item.info['mediatype'] = 'episode'
											item.info['trailer'] = yttk(m['label'])
											item.art['thumb'] = item.art['poster'] = 'https://mi3s.top/thumb/fshare.png'
											item.info['plot'] = m['info']['plot'] if 'info' in m else m['label']
											if Script.setting.get_string('taifshare') == 'true':
												item.context.script(Script.ref('/resources/lib/download:downloadfs'), 'Tải về', link)
											item.context.script(Script.ref('/resources/lib/mkd/onfshare/ifshare:tfavo'), 'Thêm vào Fshare Favorite', link)
											item.set_callback(Resolver.ref('/resources/lib/kedon:play_fs'), link, m['label'])
											yield item
										elif '/folder/' in path:
											item = Listitem()
											item.label = m['label']
											link = path.split("&url=")[1]
											item.info['mediatype'] = 'tvshow'
											item.info['trailer'] = yttk(m['label'])
											imgfs = 'https://mi3s.top/thumb/fshare.png'
											item.art['thumb'] = item.art['poster'] = imgfs
											item.info['plot'] = m['info']['plot'] if 'info' in m else m['label']
											item.context.script(Script.ref('/resources/lib/mkd/onfshare/ifshare:tfavo'), 'Thêm vào Fshare Favorite', link)
											item.set_callback(Route.ref('/resources/lib/mkd/onfshare/ifshare:index_fs'), link, 0, imgfs)
											yield item
								except:
									try:
										kq = result_f2.json()
										m = (k for k in kq['data'] if 'data' in kq)
										for k in m:
											item = Listitem()
											item.label = k['name']
											item.info['trailer'] = yttk(k['name'])
											imgfs = 'https://mi3s.top/thumb/fshare.png'
											item.art['thumb'] = item.art['poster'] = imgfs
											item.context.script(Script.ref('/resources/lib/mkd/onfshare/ifshare:tfavo'), 'Thêm vào Fshare Favorite', k['url'])
											if 'folder' in k['url']:
												item.info['mediatype'] = 'tvshow'
												item.set_callback(Route.ref('/resources/lib/mkd/onfshare/ifshare:index_fs'), k['url'], 0, imgfs)
											else:
												item.info['mediatype'] = 'episode'
												item.info['size'] = k['size']
												if Script.setting.get_string('taifshare') == 'true':
													item.context.script(Script.ref('/resources/lib/download:downloadfs'), 'Tải về', k['url'])
												item.set_callback(Resolver.ref('/resources/lib/kedon:play_fs'), k['url'], k['name'])
											yield item
									except:
										pass
								dialog.update(100)
					except:
						pass
				break
			else:
				countdown -= 1
				dialog.update(int(((1000-countdown)/1000)*100), f'Mã liên kết: {mv} - Đếm ngược: {bold(color(countdown, "orange"))}[CR]Vào trang {mv} để lấy nội dung phát')
				xbmc.sleep(1000)
				if countdown == 0:
					timeout_expired = True
		if timeout_expired:
			yield quangcao()
		dialog.close()
	except:
		yield quangcao()
@Route.register
def index_played(plugin):
	yield []
	b = get_last_play()
	if b:
		for m in b:
			item = Listitem()
			item.label = m
			item.info['mediatype'] = 'episode'
			item.art['thumb'] = item.art['poster'] = 'https://mi3s.top/thumb/MPlay.jpg'
			item.context.script(Script.ref('/resources/lib/kedon:remove_last_played'), 'Xoá khỏi lịch sử MPlay Direct', m)
			item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), b[m], m)
			yield item
		Playdel = {'label': 'Xoá lịch sử xem',
		'art': {'thumb': 'https://mi3s.top/thumb/MPlay.jpg',
		'poster': 'https://mi3s.top/thumb/MPlay.jpg'},
		'callback': clear_last_played}
		yield Listitem.from_dict(**Playdel)