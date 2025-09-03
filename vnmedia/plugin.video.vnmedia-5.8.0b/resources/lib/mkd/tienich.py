from codequick import Route, Script, Listitem, Resolver
from resources.lib.kedon import __addonnoti__, remove_file, getlink
from xbmc import executebuiltin
from bs4 import BeautifulSoup
from urlquick import cache_cleanup
def convert_size_to_bytes(size_str):
	size_str = size_str.upper().replace(" ", "")
	size, unit = float(size_str[:-2]), size_str[-2:]
	units = {"KB": 1024, "MB": 1024**2, "GB": 1024**3}
	return int(size * units[unit])
@Route.register
def index_tienich(plugin):
	streams = [
		('Cài đặt tiện ích', 'https://raw.githubusercontent.com/kenvnm/kvn/main/settings-3311592_960_720.png', settingaddon),
		('Đo tốc độ mạng', 'https://raw.githubusercontent.com/kenvnm/kvn/main/Speedtest.png', Script.ref('/resources/lib/download:speedtestcf')),
		('Đo bitrate', 'https://raw.githubusercontent.com/kodivietnam/kodivietnam.github.io/main/video-bitrate-2.png', index_bitrate),
		('Địa chỉ IP', 'https://raw.githubusercontent.com/kenvnm/kvn/main/what-is-an-ip-address-featured-image.jpg', check_myip),
		('Xoá bộ nhớ đệm', 'https://raw.githubusercontent.com/kenvnm/kvn/main/95571098-clear-cache-rubber-stamp-grunge-design-with-dust-scratches-effects-can-be-easily-removed-for-a-clean.jpg', deletecache)
	]
	for name_key, banner_key, route_key in streams:
		i = Listitem()
		i.label = name_key
		i.art['thumb'] = i.art['poster'] = banner_key
		i.set_callback(route_key)
		yield i
@Route.register
def index_bitrate(plugin):
	u = 'https://repo.jellyfin.org/jellyfish/'
	r = getlink(u, u, 1000)
	soup = BeautifulSoup(r.text, 'html.parser')
	rows = soup.select('table.main tbody tr')
	for row in rows:
		i = Listitem()
		file_tag = row.select_one('td.file a')
		tenm = file_tag.get_text(strip=True)
		file_url = file_tag['href'] if file_tag['href'].startswith('http') else f'{u}{file_tag["href"]}'
		file_size = row.select_one('td:last-child').get_text(strip=True)
		i.label = tenm
		i.info['size'] = convert_size_to_bytes(file_size)
		i.art['thumb'] = i.art['poster'] = 'https://raw.githubusercontent.com/kodivietnam/kodivietnam.github.io/main/video-bitrate-2.png'
		i.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), file_url, tenm)
		yield i
@Script.register
def check_myip(plugin):
	resp = getlink('https://redirector.googlevideo.com/report_mapping?di=no', 'https://www.google.com.vn/',-1)
	if resp is not None:
		Script.notify(__addonnoti__, resp.text)
	else:
		Script.notify(__addonnoti__, 'Không có dữ liệu')
@Script.register
def settingaddon(plugin):
	executebuiltin('Addon.OpenSettings(plugin.video.vnmedia)')
@Script.register
def deletecache(plugin):
	cache_cleanup(-1)
	remove_file('.urlquick.slite3')
	Script.notify(__addonnoti__, 'Đã xoá bộ nhớ đệm')