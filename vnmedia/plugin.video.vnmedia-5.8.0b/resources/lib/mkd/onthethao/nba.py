from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao
from bs4 import BeautifulSoup
from codequick.utils import color
import re
unba = 'https://xem.tructiepnba.com'
def timenba(chuoi):
	try:
		m = re.search(r"(\d{1,2}/\d{1,2}).*?–.*?(\d{1,2}h\d{2})", chuoi)
		return f'{m[2]} {m[1]}'
	except:
		return chuoi
@Route.register
def index_nba(plugin):
	yield []
	try:
		resp = getlink(unba, unba, 400)
		if (resp is not None):
			soup = BeautifulSoup(resp.text, 'html.parser')
			soups = soup.select('div.wp-block-group__inner-container')
			for block in soups:
				try:
					title = block.h2.get_text(strip=True)
					time = timenba(block.p.get_text(strip=True))
					buttons = block.select('a.wp-block-button__link')
					for button in buttons:
						item = Listitem()
						tenm = f'{time} {title} {color(button.text.strip(), "yellow")}'
						item.label = tenm
						item.info['plot'] = f'{tenm}\nNguồn: {unba}'
						item.info['mediatype'] = 'tvshow'
						item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/nba.png'
						item.set_callback(list_nba, button['href'], tenm)
						yield item
				except:
					pass
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def list_nba(plugin, url=None, title=None):
	yield []
	if any((url is None,title is None)):
		pass
	else:
		try:
			resp = getlink(url, url, 400)
			if (resp is not None):
				item1 = Listitem()
				tenm = f'SV1 - {title}'
				item1.label = tenm
				item1.info['plot'] = f'{tenm}\nNguồn: {unba}'
				item1.info['mediatype'] = 'episode'
				item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/nba.png'
				item1.set_callback(Resolver.ref('/resources/lib/kedon:ifr_khomuc'), url, tenm)
				yield item1
				soup = BeautifulSoup(resp.text, 'html.parser')
				soups = soup.select('pagelinkselement#post-pagination a')
				for episode in soups:
					item = Listitem()
					tenk = f'{episode.get_text(strip=True)} - {title}'
					item.label = tenk
					item.info['plot'] = f'{tenk}\nNguồn: {unba}'
					item.info['mediatype'] = 'episode'
					item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/nba.png'
					item.set_callback(Resolver.ref('/resources/lib/kedon:ifr_khomuc'), episode['href'], tenk)
					yield item
			else:
				yield quangcao()
		except:
			yield quangcao()