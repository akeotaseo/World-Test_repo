from codequick import Route, Listitem
from resources.lib.kedon import getlink, ace, quangcao
from datetime import datetime, timedelta, date
from codequick.utils import color
from bs4 import BeautifulSoup
ultv = 'https://livetv765.me'
@Route.register
def index_livetvxs(plugin):
	yield []
	try:
		url = f'{ultv}/export/webmasters.php?lang=en'
		resp = getlink(url, url, 400)
		if (resp is not None) and ('acestream' in resp.text):
			soup = BeautifulSoup(resp.text, 'html.parser')
			soups = soup.select('tr td')
			for episode in soups:
				z = episode.select('td.time')
				for w in z:
					timex = w.get_text(strip=True)
					y = f'{date.today()}T0{timex}' if len(timex)==4 else f'{date.today()}T{timex}'
					z = (datetime.fromisoformat(y) + timedelta(hours=6)).strftime('%H:%M')
				a = episode.select('td a.title')
				for b in a:
					tentran = b.get_text(strip=True)
				anh = episode.select('td img')
				for im in anh:
					img = f'https:{im["src"]}'
				x = episode.select('div a')
				for dem, number in enumerate(x, start=1):
					tapdem = color(f'Link {dem}', 'yellow')
					lp = number['href']
					if 'acestream' in lp:
						item = Listitem()
						item.art['thumb'] = item.art['poster'] = img
						tenm = f'{tapdem} {z} {tentran}'
						item.label = tenm
						item.info['plot'] = f'{tenm}\nNguồn: {ultv}'
						item.info['mediatype'] = 'episode'
						item.path = ace(lp, tenm)
						item.set_callback(item.path)
						yield item
		else:
			yield quangcao()
	except:
		yield quangcao()