from codequick import Route, Listitem
from resources.lib.kedon import getlink, quangcao, ace
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup
u365 = 'http://highlights365.com'
@Route.register
def index_highlights365(plugin):
	yield []
	try:
		url = f'{u365}/broadcasts'
		resp = getlink(url, url, 1000)
		if (resp is not None):
			soup = BeautifulSoup(resp.text, 'html.parser')
			for episode in soup.select('div.broadcast-item'):
				linktrans = episode.select('div.team-info a')
				for linktran in linktrans:
					link = linktran['href']
					ten = linktran.get_text(strip=True)
				times = episode.select('div.time')
				for time in times:
					item = Listitem()
					timex = time.get_text(strip=True)
					y = f'{date.today()}T0{timex}' if len(timex)==4 else f'{date.today()}T{timex}'
					tenm = f'{(datetime.fromisoformat(y) + timedelta(hours=7)).strftime("%H:%M")} {ten}'
					item.label = tenm
					item.info['plot'] = f'{tenm}\nNguồn: {u365}'
					item.info['mediatype'] = 'tvshow'
					item.art['thumb'] = item.art['poster'] = f"https:{episode.select_one('div.c-flag img')['data-src']}"
					item.set_callback(laylink_highlights365, f'{u365}{link}', tenm)
					yield item
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def laylink_highlights365(plugin, url=None, ten=None):
	yield []
	if any((url is None,ten is None)):
		pass
	else:
		try:
			resp = getlink(url, url, 1000)
			if (resp is not None) and ('acestream://' in resp.text):
				soup = BeautifulSoup(resp.text, 'html.parser')
				soups = soup.select('div.link-list.acestream a')
				for dem, number in enumerate(soups, start=1):
					lp = number['href']
					if 'acestream' in lp:
						item = Listitem()
						item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/acestream.png'
						tenm = f'Link {dem}-{ten}'
						item.label = tenm
						item.info['plot'] = f'{tenm}\nNguồn: {u365}'
						item.info['mediatype'] = 'episode'
						item.set_callback(ace(lp, tenm))
						yield item
			else:
				yield quangcao()
		except:
			yield quangcao()