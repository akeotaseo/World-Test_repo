from codequick import Route, Listitem, Script
@Route.register
def listiptv_root(plugin):
	streams = [
		('Xem lại truyền hình', 'https://raw.githubusercontent.com/kenvnm/kvn/main/xemlaitv.png', '/resources/lib/mkd/ontruyenhinh/replayvtv:index_vtv'),
		('VTVGO', 'https://raw.githubusercontent.com/kenvnm/kvn/main/vtvgo.png', '/resources/lib/mkd/ontruyenhinh/vtvgo:index_vtvgo'),
		('DADDYLIVE', 'https://raw.githubusercontent.com/kenvnm/kvn/main/daddy-live-hd-channels-list.png', '/resources/lib/mkd/onthethao/daddylive:all_daddy'),
		('VAVOO', 'https://raw.githubusercontent.com/kenvnm/kvn/main/vavoo.png', '/resources/lib/mkd/ontruyenhinh/vavoo:index_vavoo')
	]
	T = {'Truyền hình FPT1': 'https://raw.githubusercontent.com/ntd249/ntdiptv/main/fptudp',
	'Truyền hình FPT2': 'https://raw.githubusercontent.com/thanh51/repository.thanh51/master/ONETV.m3u',
	'Truyền hình VNPT': 'https://raw.githubusercontent.com/ntd249/ntdiptv/main/mytvrtp',
	'Truyền hình Viettel': 'https://raw.githubusercontent.com/ntd249/ntdiptv/main/viettelrtp',
	'CV Media': 'https://cvtv.xyz',
	'DakLakTV': 'https://raw.githubusercontent.com/luongtamlong/Dak-Lak-IPTV/main/daklakiptv.m3u',
	'VietNgaTV': 'https://raw.githubusercontent.com/phuhdtv/vietngatv/master/vietngatv.m3u',
	'KhanggTV': 'http://hqth.me/tviptv',
	'VMTTV': 'https://tth.vn/vmttv',
	'TaiIPTV': 'https://hqth.me/tai_iptv',
	'CaLemTV': 'https://raw.githubusercontent.com/KevinNitroG/Entertainment/m3u/playlists/calemtv.m3u',
	'HaNoiIPTV': 'https://raw.githubusercontent.com/HaNoiIPTV/HaNoiIPTV.m3u/master/Danh%20s%C3%A1ch%20k%C3%AAnh/G%C3%B3i%20ch%C3%ADnh%20th%E1%BB%A9c/H%C3%A0%20N%E1%BB%99i%20IPTV.m3u',
	'SunshineTV': 'https://raw.githubusercontent.com/Hannstcott/SunshineTr/main/sunshinetv.m3u',
	'AXT 4K Sport': 'https://raw.githubusercontent.com/MrToBun007/AXT/main/4K-UHD.m3u',
	'AlexDang 4K Sport': 'https://raw.githubusercontent.com/kgasaz/4kuhd/master/sports-channels-4k.m3u',
	'4K UHD TV': 'https://raw.githubusercontent.com/kgasaz/4kuhd/master/sports-channels-4k.m3u',
	'Phim miễn phí': 'http://iptv.pro.vn/phimiptv',
	'ChinaTV': 'http://hqth.me/china-tv',
	'IPTV-ORG All': 'https://iptv-org.github.io/iptv/index.m3u',
	'IPTV-ORG Category': 'https://iptv-org.github.io/iptv/index.category.m3u',
	'IPTV-ORG Language': 'https://iptv-org.github.io/iptv/index.language.m3u',
	'IPTV-ORG Country': 'https://iptv-org.github.io/iptv/index.country.m3u',
	'IPTV-ORG Region': 'https://iptv-org.github.io/iptv/index.region.m3u'}
	if 'http' in Script.setting.get_string('myiptv'):
		iv = Listitem()
		iv.label = 'My List IPTV'
		iv.info['mediatype'] = 'tvshow'
		iv.art['thumb'] = iv.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/iptv.png'
		iv.set_callback(Route.ref('/resources/lib/mkd/ontruyenhinh/listiptv:list_iptv'), Script.setting.get_string('myiptv'))
		yield iv
	for name_key, banner_key, route_key in streams:
		i = Listitem()
		i.label = name_key
		i.info['mediatype'] = 'tvshow'
		i.art['thumb'] = i.art['poster'] = banner_key
		i.set_callback(Route.ref(route_key))
		yield i
	for k in T:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/iptv.png'
		item.set_callback(Route.ref('/resources/lib/mkd/ontruyenhinh/listiptv:list_iptv'), T[k])
		yield item