from codequick import Route, Listitem
@Route.register
def index_thethao(plugin):
	streams = [
		('REPLAY', 'https://raw.githubusercontent.com/kenvnm/kvn/main/xemlai.png', '/resources/lib/mkd/onthethao/xemlaivk:index_xemlaivk'),
		# ('Tin thể thao', 'https://raw.githubusercontent.com/kenvnm/kvn/main/tinthethao.png', '/resources/lib/mkd/onthethao/tinthethao:index_tinthethao'),
		('ACESTREAM', 'https://raw.githubusercontent.com/kenvnm/kvn/main/acestream.png', '/resources/lib/mkd/acest:index_acestream'),
		('DADDYLIVE', 'https://raw.githubusercontent.com/kenvnm/kvn/main/daddy-live-hd-channels-list.png', '/resources/lib/mkd/onthethao/daddylive:index_daddy'),
		# ('MECIURI [COLOR red]OFF?...[/COLOR]', 'https://raw.githubusercontent.com/kenvnm/kvn/main/sports-channels.png', '/resources/lib/mkd/onthethao/ustream:index_ustream'),
		('90P-VEBO', 'https://raw.githubusercontent.com/kenvnm/kvn/main/90p.png', '/resources/lib/mkd/onthethao/phut90:index_90p'),
		('THAPCAM', 'https://raw.githubusercontent.com/kenvnm/kvn/main/thapcamtv.png', '/resources/lib/mkd/onthethao/thapcam:index_thapcam'),
		('CAKEO', 'https://raw.githubusercontent.com/kenvnm/kvn/main/cakeotv.png', '/resources/lib/mkd/onthethao/cakeo:index_cakeo'),
		('MITOM', 'https://raw.githubusercontent.com/kenvnm/kvn/main/mitom.png', '/resources/lib/mkd/onthethao/phut91:index_91phut'),
		('CAKHIA', 'https://raw.githubusercontent.com/kenvnm/kvn/main/cakhia.png', '/resources/lib/mkd/onthethao/cakhia:index_cakhia'),
		('RAKHOI', 'https://raw.githubusercontent.com/kenvnm/kvn/main/rakhoi.png', '/resources/lib/mkd/onthethao/rakhoi:index_rakhoi'),
		('CAHEO', 'https://raw.githubusercontent.com/kenvnm/kvn/main/caheo.png', '/resources/lib/mkd/onthethao/caheo:index_caheo'),
		('SAOKE', 'https://raw.githubusercontent.com/kenvnm/kvn/main/saoke.png', '/resources/lib/mkd/onthethao/saoke:index_saoke'),
		('GAVANG ', 'https://raw.githubusercontent.com/kenvnm/kvn/main/gavang.png', '/resources/lib/mkd/onthethao/gavang:index_gavang'),
		('SOCOLIVE', 'https://raw.githubusercontent.com/kenvnm/kvn/main/soco.png', '/resources/lib/mkd/onthethao/socolive:index_socolive'),
		('TRUCTIEPNBA', 'https://raw.githubusercontent.com/kenvnm/kvn/main/nba.png', '/resources/lib/mkd/onthethao/nba:index_nba')
	]
	i = Listitem()
	i.label = 'SỰ KIỆN TRỰC TIẾP'
	i.info['mediatype'] = 'tvshow'
	i.art['thumb'] = i.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/sukien.png'
	i.set_callback(Route.ref('/resources/lib/mkd/onfshare/gcs:listvmf_gcs'), 'https://mi3s.top/vnmedia', 'SỰ KIỆN TRỰC TIẾP')
	# yield i
	for name_key, banner_key, url_key in streams:
		item = Listitem()
		item.label = name_key
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = banner_key
		item.set_callback(Route.ref(url_key))
		yield item