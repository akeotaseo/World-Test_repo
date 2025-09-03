from codequick import Route, Listitem
@Route.register
def index_tintuc(plugin):
	streams = [
		('Báo Nói - Đọc Báo Giúp Bạn', 'https://raw.githubusercontent.com/kenvnm/kvn/main/news.png', '/resources/lib/mkd/ontintuc/baomoi:index_baomoi'),
		('Tin thể thao', 'https://raw.githubusercontent.com/kenvnm/kvn/main/sportnews.png', '/resources/lib/mkd/onthethao/tinthethao:index_tinthethao'),
	]
	T = {
		'UCabsTV34JwALXKGMqHpvUiA': 'VTV24',
		'UCL9-pEHNBs3N4r2bMoXdLJA': 'VTC Now',
		'UCUmRGR3a-g13O6pG927KQmg': 'TV24h',
		'UCRjzfa1E0gA50lvDQipbDMg': '60 giây',
		'UCinkijG72G87sn-mtaFJTbA': 'Thời tiết-Môi trường',
		'UCZ7cd8K5jo7fHUksCgMfpeg': 'Văn hoá-Du lịch',
		'UC7723FqVehXq2zeRb3tP0hQ': 'Kinh tế-Tài chính',
		'UCIg56SgvoZF8Qg0Jx_gh6Pg': 'An ninh',
		'UCmBT5CqUxf3-K5_IU9tVtBg': 'Thông tấn xã',
		'UCPJfjHrW3-zIeSaZTgmckmg': 'Nhân dân',
		'UCZnhEIF8a5Uv4GMPwT6KafQ': 'Nông nghiệp-nông thôn',
		'UCHPzpxcYhxkb0fMJKeSe66g': 'Thế giới đó đây',
		'UCZcCmWhvK0gfThyWRmRerDQ': 'VTC tin mới',
		'UC7_mgS3z22z0WhR7COJ8E2w': 'Hà Nội tin tức',
		'UCZYKmEA2iQOSbyKc6xj5Vfw': 'HTV tin tức',
		'UC1K9R0YwYrp7auy6fPbnnIQ': 'THVL tổng hợp',
		'UC0OX9WL_PxOlX0HQbu45JfA': 'Luật giao thông',
		'UCtfsYfpS3KoRTEbCMc6l85w': 'Tuấn tiền tỉ',
		'UCaJ6YgNkAlRsl8nWZS2sjtg': 'Dương địa lý'
	}
	for name_key, banner_key, route_key in streams:
		i = Listitem()
		i.label = name_key
		i.info['mediatype'] = 'tvshow'
		i.art['thumb'] = i.art['poster'] = banner_key
		i.set_callback(Route.ref(route_key))
		yield i
	for k in T:
		yield Listitem.youtube(k, label=T[k])