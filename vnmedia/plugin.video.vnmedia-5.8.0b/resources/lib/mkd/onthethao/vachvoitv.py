from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao, fu, domain
from bs4 import BeautifulSoup
from codequick.utils import color
@Route.register
def index_vachvoi(plugin):
	yield []
	try:
		ref = domain(fu('https://bit.ly/vachvoi'))
		u = f'{ref}/blocks/matchtoday.aspx?page=1'
		resp = getlink(u, u, 1000)
		if (resp is not None):
			soup = BeautifulSoup(resp.text, 'html.parser')
			soups = soup.select('div.grid-match')
			for k in soups:
				title = k.select_one('a')['title']
				link = k.select_one('a')['href'] if k.select_one('a')['href'].startswith('http') else f"{ref}{k.select_one('a')['href']}"
				tg = k.select_one('div.grid-match__date').get_text(strip=True)
				blv = k.select_one('div.grid-match__commentator').get_text(strip=True)
				ten = f'{tg} {title} {color(blv, "yellow")}'
				item = Listitem()
				item.label = ten
				item.info['plot'] = f'{ten}\nNguồn: {ref}'
				item.info['mediatype'] = 'episode'
				item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kodivietnam/kodivietnam.github.io/main/vachvoi.png'
				item.set_callback(Resolver.ref('/resources/lib/kedon:ifr_khomuc'), link, ten)
				yield item
		else:
			yield quangcao()
	except:
		pass