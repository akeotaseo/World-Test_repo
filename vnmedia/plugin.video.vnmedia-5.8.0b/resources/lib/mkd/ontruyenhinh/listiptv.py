from codequick import Route, Listitem, Resolver
from resources.lib.kedon import ace, streamiptv, useragentott, referer, quangcao, getlinkip
import re
@Route.register
def list_iptv(plugin, url=None):
	yield []
	if url is None:
		pass
	else:
		try:
			item = Listitem()
			item.label = 'TẤT CẢ CÁC KÊNH'
			item.info['mediatype'] = 'tvshow'
			item.info['plot'] = f'TẤT CẢ CÁC KÊNH\nNguồn: {url}'
			item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/truyenhinh.png'
			item.set_callback(little_iptv, url)
			yield item
			try:
				texturl = getlinkip(url, url).text
				group = re.findall(r'group-title="(.*?)"', texturl)
				ld = list(dict.fromkeys(group))
				um = []
				um = [k for tk in ld for k in (tk.split(';') if ';' in tk else [tk]) if k != '' and k not in um]
				for p in um:
					item = Listitem()
					item.label = p
					item.info['plot'] = f'{p}\nNguồn: {url}'
					item.info['mediatype'] = 'tvshow'
					item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/truyenhinh.png'
					item.set_callback(info_iptv, url, p)
					yield item
			except:
				pass
		except:
			yield quangcao()
@Route.register
def info_iptv(plugin, url=None, tk=None):
	yield []
	if any((url is None,tk is None)):
		pass
	else:
		try:
			texturl = getlinkip(url, url).text
			ketqua = re.sub(r'(#EXTM3U|#[^EX|^KODI])(.*)', '', texturl).split('#EXTINF')
			sre1 = re.compile(r'\n((http|https|udp|rtp|acestream):(.*?)\n)')
			sre2 = re.compile(r'[,](?!.*[,])(.*)')
			sre4 = re.compile(r'tvg-logo="(.*?)"')
			sre5 = re.compile(r'http-user-agent=(.*?)\n')
			sre6 = re.compile(r'http-referrer=(.*?)\n')
			sre7 = re.compile(r'license_key=(.*?)\n')
			for kq in ketqua:
				try:
					s1 = sre1.search(kq)
					s2 = sre2.search(kq)
					s4 = sre4.search(kq)
					s5 = sre5.search(kq)
					s6 = sre6.search(kq)
					s7 = sre7.search(kq)
					if s7:
						yield []
					else:
						if f'group-title="{tk}"' in kq and ';' not in kq and s1:
							item = Listitem()
							kenh = s1[1]
							item.label = s2[1]
							item.info['mediatype'] = 'episode'
							item.info['plot'] = f'{s2[1]}\nNguồn: {url}'
							if s4:
								item.art['thumb'] = item.art['poster'] = s4[1]
							else:
								item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/truyenhinh.png'
							if 'acestream' in kenh or ':6878' in kenh:
								item.set_callback(ace(kenh, s2[1]))
							else:
								user = s5[1] if s5 else useragentott
								linkplay = f'{streamiptv(kenh, user)}{referer(s6[1])}' if s6 else streamiptv(kenh, user)
								item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), linkplay, s2[1])
							yield item
						elif tk in kq and ';' in kq and s1:
							item = Listitem()
							kenh = s1[1]
							item.label = s2[1]
							item.info['mediatype'] = 'episode'
							item.info['plot'] = f'{s2[1]}\nNguồn: {url}'
							if s4:
								item.art['thumb'] = item.art['poster'] = s4[1]
							else:
								item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/truyenhinh.png'
							if 'acestream' in kenh or ':6878' in kenh:
								item.set_callback(ace(kenh, s2[1]))
							else:
								user = s5[1] if s5 else useragentott
								linkplay = f'{streamiptv(kenh, user)}{referer(s6[1])}' if s6 else streamiptv(kenh, user)
								item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), linkplay, s2[1])
							yield item
				except:
					yield quangcao()
		except:
			yield quangcao()
@Route.register
def little_iptv(plugin, url=None):
	yield []
	if url is None:
		pass
	else:
		try:
			texturl = getlinkip(url, url).text
			ketqua = re.sub(r'(#EXTM3U|#[^EX|^KODI])(.*)', '', texturl).split('#EXTINF')
			sre1 = re.compile(r'\n((http|https|udp|rtp|acestream):(.*?)\n)')
			sre2 = re.compile(r'[,](?!.*[,])(.*)')
			sre3 = re.compile(r'group-title="(.*?)"')
			sre4 = re.compile(r'tvg-logo="(.*?)"')
			sre5 = re.compile(r'http-user-agent=(.*?)\n')
			sre6 = re.compile(r'http-referrer=(.*?)\n')
			sre7 = re.compile(r'license_key=(.*?)\n')
			for kq in ketqua:
				try:
					s1 = sre1.search(kq)
					s2 = sre2.search(kq)
					s3 = sre3.search(kq)
					s4 = sre4.search(kq)
					s5 = sre5.search(kq)
					s6 = sre6.search(kq)
					s7 = sre7.search(kq)
					if s7:
						yield []
					else:
						if s1:
							item = Listitem()
							kenh = s1[1]
							tenkenh = s2[1]
							nhomkenh = s3[1] if s3 else 'TỔNG HỢP'
							item.info['plot'] = f'{nhomkenh} - {tenkenh}\nNguồn: {url}'
							tenm = f'{tenkenh} - {nhomkenh}'
							item.label = tenm
							item.info['mediatype'] = 'episode'
							if s4:
								item.art['thumb'] = item.art['poster'] = s4[1]
							else:
								item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/truyenhinh.png'
							if 'acestream' in kenh or ':6878' in kenh:
								item.set_callback(ace(kenh, tenm))
							else:
								user = s5[1] if s5 else useragentott
								linkplay = f'{streamiptv(kenh, user)}{referer(s6[1])}' if s6 else streamiptv(kenh, user)
								item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), linkplay, tenm)
							yield item
				except:
					yield []
		except:
			yield quangcao()