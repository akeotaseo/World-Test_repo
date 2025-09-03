from codequick import Route, Script, Listitem
from codequick.utils import color
@Route.register
def index_fshare(plugin):
	streams = [
		(color('MỚI NHẤT', 'yellow'), 'https://raw.githubusercontent.com/kenvnm/kvn/main/moicapnhat.png', 'https://thuvienhd.xyz/recent/page/'),
		('4K - H265', 'https://raw.githubusercontent.com/kenvnm/kvn/main/4k.png', 'https://thuvienhd.xyz/genre/4k/page/'),
		('Bluray nguyên gốc', 'https://raw.githubusercontent.com/kenvnm/kvn/main/bluray.png', 'https://thuvienhd.xyz/genre/bluray-nguyen-goc/page/'),
		('Thuyết minh', 'https://raw.githubusercontent.com/kenvnm/kvn/main/thuyetminh.png', 'https://thuvienhd.xyz/genre/thuyet-minh-tieng-viet/page/'),
		('Lồng tiếng', 'https://raw.githubusercontent.com/kenvnm/kvn/main/longtieng.png', 'https://thuvienhd.xyz/genre/long-tieng-tieng-viet/page/'),
		('Hoạt hình', 'https://raw.githubusercontent.com/kenvnm/kvn/main/anime.png', 'https://thuvienhd.xyz/genre/animation/page/'),
		('Phim lẻ', 'https://raw.githubusercontent.com/kenvnm/kvn/main/phimle.png', 'https://thuvienhd.xyz/genre/phim-le/page/'),
		('Phim bộ', 'https://raw.githubusercontent.com/kenvnm/kvn/main/phimbo.png', 'https://thuvienhd.xyz/genre/series/page/')
	]
	s2 = [
		('NHẬP CODEPLAY', 'https://raw.githubusercontent.com/kenvnm/kvn/main/playcode.png', '/resources/lib/mkd/onfshare/codenumber:index_number'),
		('Fshare Favourite', 'https://raw.githubusercontent.com/kenvnm/kvn/main/yeuthich.png', '/resources/lib/mkd/onfshare/ifshare:fs_favorite'),
		('VNM Tuyển Chọn', 'https://raw.githubusercontent.com/kenvnm/kvn/main/dexuat.png', '/resources/lib/mkd/onfshare/timfshare:index_pdx'),
	]
	s3 = [
		('HdVietNam', 'https://raw.githubusercontent.com/kenvnm/kvn/main/thuvienhd.png', '/resources/lib/mkd/onfshare/hdvn:index_hdvn'),
		('Thư viện HD', 'https://raw.githubusercontent.com/kenvnm/kvn/main/tvhd.png', '/resources/lib/mkd/onfshare/thuvienhd:index_thuvienhd'),
		('Thư viện Cine', 'https://raw.githubusercontent.com/kenvnm/kvn/main/thuviencine.png', '/resources/lib/mkd/onfshare/thuviencine:index_thuviencine'),
		('TOP FSHARE', 'https://raw.githubusercontent.com/kenvnm/kvn/main/topfshare.png', '/resources/lib/mkd/onfshare/ifshare:fs_topfollow')
	]
	yield Listitem.search(Route.ref('/resources/lib/mkd/onfshare/timfshare:searchfs'))
	if Script.setting.get_string('historyfs') is not '0':
		yield Listitem.from_dict(**{'label': 'LỊCH SỬ XEM',
		'art': {'thumb': 'https://raw.githubusercontent.com/kenvnm/kvn/main/lichsu.png',
		'poster': 'https://raw.githubusercontent.com/kenvnm/kvn/main/lichsu.png'},
		'callback': Route.ref('/resources/lib/mkd/onfshare/ifshare:index_daxem')})
	if Script.setting.get_string('taifshare') == 'true':
		yield Listitem.from_dict(**{'label': 'Tệp đã tải',
		'art':{'thumb':'https://raw.githubusercontent.com/kenvnm/kvn/main/datai.png',
		'poster':'https://raw.githubusercontent.com/kenvnm/kvn/main/datai.png'},
		'callback': Route.ref('/resources/lib/mkd/onfshare/datai:index_datai')})
	for namekey, bannerkey, routekey in s2:
		i2 = Listitem()
		i2.label = namekey
		i2.info['mediatype'] = 'tvshow'
		i2.art['thumb'] = i2.art['poster'] = bannerkey
		i2.set_callback(Route.ref(routekey))
		yield i2
	yield trending()
	for name_key, banner_key, url_key in streams:
		item = Listitem()
		item.label = name_key
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = banner_key
		item.set_callback(Route.ref('/resources/lib/mkd/onfshare/thuvienhd:thuvienhd_page'), url_key, 1)
		yield item
	for name, banner, route in s3:
		i3 = Listitem()
		i3.label = name
		i3.info['mediatype'] = 'tvshow'
		i3.art['thumb'] = i3.art['poster'] = banner
		i3.set_callback(Route.ref(route))
		yield i3
	yield loginfs()
	yield checkinfofs()
	yield speedtestfs()
def trending():
	item = Listitem()
	item.label = color('TRENDING', 'yellow')
	item.info['mediatype'] = 'tvshow'
	item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/hot.png'
	item.set_callback(Route.ref('/resources/lib/mkd/onfshare/thuviencine:thuviencine_page'), 'https://thuviencine.com/top/', 1)
	return item
def speedtestfs():
	i4 = Listitem()
	i4.label = 'Đo tốc độ Fshare'
	i4.art['thumb'] = i4.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/Speedtest.png'
	i4.set_callback(Script.ref('/resources/lib/download:speedtestfs'))
	return i4
def checkinfofs():
	i5 = Listitem()
	i5.label = 'Thông tin tài khoản'
	i5.art['thumb'] = i5.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
	i5.set_callback(Script.ref('/resources/lib/mkd/onfshare/ifshare:fs_info'))
	return i5
def loginfs():
	i6 = Listitem()
	i6.label = 'Cài đặt tài khoản'
	i6.art['thumb'] = i6.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/settings-3311592_960_720.png'
	i6.set_callback(Script.ref('/resources/lib/mkd/tienich:settingaddon'))
	return i6