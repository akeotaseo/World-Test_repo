from codequick import Route, Listitem, Resolver
from resources.lib.kedon import getlink, quangcao, yttk, listqc, news, qc, fu
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from datetime import date
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from resolveurl import resolve
from codequick.utils import italic
import re
tmdbAPI='https://api.themoviedb.org/3'
apimdb='b030404650f279792a8d3287232358e3'
apiKey = f'{apimdb}&language=vi-VN'
append = 'alternative_titles,credits,external_ids,keywords,videos,recommendations'
ALPHABET = {
'47ab07f9': 'A', '47ab07fa': 'B', '47ab07fb': 'C', '47ab07fc': 'D', '47ab07fd': 'E',
'47ab07fe': 'F', '47ab07ff': 'G', '47ab0800': 'H', '47ab0801': 'I', '47ab0802': 'J',
'47ab0803': 'K', '47ab0804': 'L', '47ab0805': 'M', '47ab0806': 'N', '47ab0807': 'O',
'47ab0808': 'P', '47ab0809': 'Q', '47ab080a': 'R', '47ab080b': 'S', '47ab080c': 'T',
'47ab080d': 'U', '47ab080e': 'V', '47ab080f': 'W', '47ab0810': 'X', '47ab0811': 'Y',
'47ab0812': 'Z',
'47ab0819': 'a', '47ab081a': 'b', '47ab081b': 'c', '47ab081c': 'd', '47ab081d': 'e',
'47ab081e': 'f', '47ab081f': 'g', '47ab0820': 'h', '47ab0821': 'i', '47ab0822': 'j',
'47ab0823': 'k', '47ab0824': 'l', '47ab0825': 'm', '47ab0826': 'n', '47ab0827': 'o',
'47ab0828': 'p', '47ab0829': 'q', '47ab082a': 'r', '47ab082b': 's', '47ab082c': 't',
'47ab082d': 'u', '47ab082e': 'v', '47ab082f': 'w', '47ab0830': 'x', '47ab0831': 'y',
'47ab0832': 'z',
'47ab07e8': '0', '47ab07e9': '1', '47ab07ea': '2', '47ab07eb': '3', '47ab07ec': '4',
'47ab07ed': '5', '47ab07ee': '6', '47ab07ef': '7', '47ab07f0': '8', '47ab07f1': '9',
'47ab07f2': ':', '47ab07e7': '/', '47ab07e6': '.', '47ab0817': '_', '47ab07e5': '-'
}
def decode(uri):
	for key, value in ALPHABET.items():
		uri = uri.replace(key, value)
	return uri.replace('---', '-$DASH$-').replace('-', '').replace('$DASH$', '-')
def subvidto(idk):
	if '&' in str(idk):
		match = re.search(r'(\d+)&season=(\d+)&episode=(\d+)', idk)
		u2 = f'https://vidsrc.to/embed/tv/{match[1]}/{match[2]}/{match[3]}'
	else:
		u2 = f'https://vidsrc.to/embed/movie/{idk}'
	r2 = getlink(u2,u2,-1)
	if (r2 is not None) and ('data-id' in r2.text):
		dataid = re.search('data-id="(.*?)"', r2.text)[1]
		u = f'https://vidsrc.to/ajax/embed/episode/{dataid}/subtitles'
		r = getlink(u,u,-1)
		if (r is not None) and ('Vietnam' in r.text):
			vtt = ''.join((k['file'] for k in r.json() if 'Vietnam' in k['label']))
		else:
			vtt = news
	else:
		vtt = news
	return vtt
@Route.register
def index_mdb(plugin):
	yield Listitem.search(ds_mdb)
	dulieu = {
	'Trending': f'{tmdbAPI}/trending/all/day?api_key={apiKey}&region=US',
	'Popular Movies': f'{tmdbAPI}/movie/popular?api_key={apiKey}&region=US',
	'Popular TV Shows': f'{tmdbAPI}/tv/popular?api_key={apiKey}&region=US&with_original_language=en',
	'Airing Today TV Shows': f'{tmdbAPI}/tv/airing_today?api_key={apiKey}&region=US&with_original_language=en',
	'Netflix': f'{tmdbAPI}/discover/tv?api_key={apiKey}&with_networks=213',
	'Amazon': f'{tmdbAPI}/discover/tv?api_key={apiKey}&with_networks=1024',
	'Disney+': f'{tmdbAPI}/discover/tv?api_key={apiKey}&with_networks=2739',
	'Hulu': f'{tmdbAPI}/discover/tv?api_key={apiKey}&with_networks=453',
	'Apple TV+': f'{tmdbAPI}/discover/tv?api_key={apiKey}&with_networks=2552',
	'HBO': f'{tmdbAPI}/discover/tv?api_key={apiKey}&with_networks=49',
	'Paramount+': f'{tmdbAPI}/discover/tv?api_key={apiKey}&with_networks=4330',
	'Top Rated Movies': f'{tmdbAPI}/movie/top_rated?api_key={apiKey}&region=US',
	'Top Rated TV Shows': f'{tmdbAPI}/tv/top_rated?api_key={apiKey}&region=US',
	'Upcoming Movies': f'{tmdbAPI}/movie/upcoming?api_key={apiKey}&region=US',
	'Korean Shows': f'{tmdbAPI}/discover/tv?api_key={apiKey}&with_original_language=ko',
	'Airing Today Anime': f'{tmdbAPI}/tv/airing_today?api_key={apiKey}&with_keywords=210024|222243&sort_by=primary_release_date.desc',
	'Ongoing Anime': f'{tmdbAPI}/tv/on_the_air?api_key={apiKey}&with_keywords=210024|222243&sort_by=primary_release_date.desc',
	'Anime': f'{tmdbAPI}/discover/tv?api_key={apiKey}&with_keywords=210024|222243',
	'Anime Movies': f'{tmdbAPI}/discover/movie?api_key={apiKey}&with_keywords=210024|222243'
	}
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/onstream.png'
		item.set_callback(ds_mdb, dulieu[k], 1)
		yield item
@Route.register
def ds_mdb(plugin, search_query=None, next_page=None):
	yield []
	try:
		if '://' not in search_query:
			next_page = 1
			sr = quote_plus(search_query)
			match = f'{tmdbAPI}/search/multi?api_key={apiKey}&query={sr}'
		else:
			match = search_query
		u = f'{match}&page={next_page}'
		r = getlink(u,u,1000)
		if (r is not None) and ('results' in r.text):
			rj = r.json()
			for k in rj['results']:
				if 'known_for' in k:
					s = k['known_for'][0]
					try:
						ten = s['name']
					except:
						ten = s['title']
					idp = s['id']
					mota = s['overview']
					diem = s['vote_average']
					anhposter = s['poster_path']
					try:
						typep = s['media_type']
					except:
						typep = 'movie' if '/movie' in match else 'tv'
					try:
						try:
							phathanh = s['release_date']
						except:
							phathanh = s['first_air_date']
					except:
						phathanh = date.today()
				else:
					try:
						ten = k['name']
					except:
						ten = k['title']
					idp = k['id']
					mota = k['overview']
					diem = k['vote_average']
					anhposter = k['poster_path']
					try:
						typep = k['media_type']
					except:
						typep = 'movie' if '/movie' in match else 'tv'
					try:
						try:
							phathanh = k['release_date']
						except:
							phathanh = k['first_air_date']
					except:
						phathanh = date.today()
				item = Listitem()
				item.label = ten
				item.info['plot'] = f'{mota}\nNguồn: https://themoviedb.org'
				item.info['mediatype'] = 'tvshow'
				item.info['premiered'] = phathanh
				item.info['rating'] = float(diem)
				item.info['dbid'] = idp
				item.info['trailer'] = yttk(ten)
				item.art['thumb'] = item.art['poster'] = f"https://image.tmdb.org/t/p/w500{anhposter}"
				item.set_callback(detail_mdb, idp, typep)
				yield item
			tong = rj['total_pages']
			if next_page < tong:
				item1 = Listitem()
				item1.label = f'Trang {str(int(next_page) + 1)}'
				item1.info['mediatype'] = 'tvshow'
				item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
				item1.set_callback(ds_mdb, match, next_page + 1)
				yield item1
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def detail_mdb(plugin, idp=None, typep=None):
	yield []
	if any((idp is None,typep is None)):
		pass
	else:
		try:
			if typep == 'tv':
				res_url = f'{tmdbAPI}/tv/{idp}?api_key={apiKey}&append_to_response={append}'
				res_response = getlink(res_url,res_url,1000)
				if res_response is not None:
					res_data = res_response.json()
					try:
						title = res_data['title']
					except:
						title = res_data['name']
					try:
						trailer_results = res_data['videos']['results'][0]['key']
						ut = f'plugin://plugin.video.youtube/play/?video_id={trailer_results}'
						for season in res_data['seasons']:
							season_number = season['season_number']
							item = Listitem()
							item.label = f"{title} - {season['name']}"
							item.info['plot'] = f'{season["overview"]}\nNguồn: https://themoviedb.org'
							item.info['mediatype'] = 'tvshow'
							item.info['premiered'] = season['air_date']
							item.info['rating'] = float(season['vote_average'])
							item.info['dbid'] = idp
							item.info['trailer'] = ut
							item.art['thumb'] = item.art['poster'] = f"https://image.tmdb.org/t/p/w500{season['poster_path']}"
							item.set_callback(tv_mdb, idp, season_number, title)
							yield item
					except:
						for season in res_data['seasons']:
							season_number = season['season_number']
							item = Listitem()
							item.label = f"{title} - {season['name']}"
							item.info['plot'] = f'{season["overview"]}\nNguồn: https://themoviedb.org'
							item.info['mediatype'] = 'tvshow'
							item.info['premiered'] = season['air_date']
							item.info['rating'] = float(season['vote_average'])
							item.info['dbid'] = idp
							item.info['trailer'] = yttk(title)
							item.art['thumb'] = item.art['poster'] = f"https://image.tmdb.org/t/p/w500{season['poster_path']}"
							item.set_callback(tv_mdb, idp, season_number, title)
							yield item
				else:
					yield quangcao()
			else:
				res_url = f'{tmdbAPI}/movie/{idp}?api_key={apiKey}&append_to_response={append}'
				res_response = getlink(res_url,res_url,1000)
				if res_response is not None:
					res_data = res_response.json()
					try:
						title = res_data['title']
					except:
						title = res_data['name']
					poster = res_data['poster_path']
					mota = res_data['overview']
					img = f"https://image.tmdb.org/t/p/w500{res_data['poster_path']}"
					try:
						try:
							release_date = res_data['release_date']
						except:
							release_date = res_data['first_air_date']
					except:
						release_date = date.today()
					try:
						trailer_results = res_data['videos']['results'][0]['key']
						ut = f'plugin://plugin.video.youtube/play/?video_id={trailer_results}'
						item2 = Listitem()
						item2.label = f'TRAILER: {italic(title)}'
						item2.info['mediatype'] = 'episode'
						item2.art['thumb'] = item2.art['poster'] = f'https://i.ytimg.com/vi/{trailer_results}/sddefault.jpg'
						item2.set_path(ut)
						yield item2
						item = Listitem()
						item.label = title
						item.info['trailer'] = ut
						item.info['rating'] = float(res_data['vote_average'])
						item.info['mediatype'] = 'tvshow'
						item.info['premiered'] = release_date
						item.info['plot'] = f'{mota}\nNguồn: https://themoviedb.org'
						item.art['thumb'] = item.art['poster'] = img
						item.set_callback(list_flix, title, idp)
						yield item
					except:
						item = Listitem()
						item.label = title
						item.info['trailer'] = yttk(title)
						item.info['rating'] = float(res_data['vote_average'])
						item.info['mediatype'] = 'tvshow'
						item.info['premiered'] = release_date
						item.info['plot'] = f'{mota}\nNguồn: https://themoviedb.org'
						item.art['thumb'] = item.art['poster'] = img
						item.set_callback(list_flix, title, idp)
						yield item
				else:
					yield quangcao()
		except:
			yield quangcao()
@Route.register
def tv_mdb(plugin, idp=None, season_number=None, title=None):
	yield []
	if any((idp is None,season_number is None,title is None)):
		pass
	else:
		try:
			res_url = f'{tmdbAPI}/tv/{idp}/season/{season_number}?api_key={apiKey}'
			res_response = getlink(res_url,res_url,1000)
			if res_response is not None:
				season_data = res_response.json()
				season_episodes = season_data['episodes']
				bg_poster = f"https://image.tmdb.org/t/p/w500{season_data['poster_path']}"
				vote_average = season_data['vote_average']
				try:
					trailer_results = season_data['videos']['results'][0]['key']
					ut = f'plugin://plugin.video.youtube/play/?video_id={trailer_results}'
					for episode in season_episodes:
						eps_title = episode['name']
						episode_number = episode['episode_number']
						season_number = episode['season_number']
						ss = f'{season_number:02}'
						es = f'{episode_number:02}'
						e = f'{title} S{ss}E{es}'
						uep = f'{idp}&season={season_number}&episode={episode_number}'
						item = Listitem()
						item.label = e
						item.info['mediatype'] = 'tvshow'
						item.info['rating'] = float(vote_average)
						item.info['premiered'] = episode['air_date']
						item.info['plot'] = f'{season["overview"]}\nNguồn: https://themoviedb.org'
						item.info['trailer'] = ut
						item.art['thumb'] = item.art['poster'] = bg_poster
						item.set_callback(list_season, idp, ss, es, e, uep)
						yield item
				except:
					for episode in season_episodes:
						episode_number = episode['episode_number']
						season_number = episode['season_number']
						item = Listitem()
						ss = f'{season_number:02}'
						es = f'{episode_number:02}'
						e = f'{title} S{ss}E{es}'
						uep = f'{idp}&season={season_number}&episode={episode_number}'
						item.label = e
						item.info['mediatype'] = 'tvshow'
						item.info['rating'] = float(vote_average)
						item.info['premiered'] = episode['air_date']
						item.info['plot'] = f'{season["overview"]}\nNguồn: https://themoviedb.org'
						item.info['trailer'] = yttk(e)
						item.art['thumb'] = item.art['poster'] = bg_poster
						item.set_callback(list_season, idp, ss, es, e, uep)
						yield item
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def list_flix(plugin, tenm=None, idp=None):
	yield []
	if any((tenm is None,idp is None)):
		pass
	else:
		try:
			u = f'{tmdbAPI}/movie/{idp}?language=en-US&api_key={apimdb}'
			ru = getlink(u,u,-1)
			if (ru is not None):
				rj = ru.json()
				bg_poster = f"https://image.tmdb.org/t/p/w500{rj['poster_path']}"
				try:
					name = rj['name']
				except:
					name = rj['title']
				i = Listitem()
				i.label = f'play123 - {italic(tenm)}'
				i.info['mediatype'] = 'episode'
				i.art['thumb'] = i.art['poster'] = bg_poster
				i.set_callback(Resolver.ref('/resources/lib/kedon:play123embed'), f'https://play.123embed.net/ajax/movie/get_sources/{idp}/grab', name)
				yield i
				url = f'https://doomovies.net/movies/{name.replace(" ","-")}'
				r = getlink(url, url, 1000)
				if (r is not None) and ('tbody' in r.text):
					soup = BeautifulSoup(r.text, 'html.parser')
					soups = soup.select('tbody a[target="_blank"]')
					for k in soups:
						href = k['href']
						c = k.get_text(strip=True).split('.')[0]
						item = Listitem()
						item.label = f'{c} - {italic(tenm)}'
						item.info['mediatype'] = 'episode'
						item.art['thumb'] = item.art['poster'] = bg_poster
						item.set_callback(list_mv, href, name, idp)
						yield item
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def list_season(plugin, idp=None, season_number=None, episode_number=None, tenm=None, idk=None):
	yield []
	if any((idp is None,season_number is None,episode_number is None,tenm is None,idk is None)):
		pass
	else:
		try:
			u = f'{tmdbAPI}/tv/{idp}?language=en-US&api_key={apimdb}'
			ru = getlink(u,u,-1)
			if (ru is not None):
				rj = ru.json()
				bg_poster = f"https://image.tmdb.org/t/p/w500{rj['poster_path']}"
				try:
					name = rj['name']
				except:
					name = rj['title']
				url_sepi = f's{season_number}e{episode_number}'
				title = f'{name} {url_sepi}'
				title2 = name.replace(' ','-')
				i = Listitem()
				i.label = f'play123 - {italic(tenm)}'
				i.info['mediatype'] = 'episode'
				i.art['thumb'] = i.art['poster'] = bg_poster
				i.set_callback(Resolver.ref('/resources/lib/kedon:play123embed'), f'https://play.123embed.net/tv/{idp}-S{int(season_number)}/{int(episode_number)}', title)
				yield i
				url = f'https://bstsrs.one/show/{title2}-{url_sepi}/season/{season_number}/episode/{episode_number}'
				r = getlink(url, url, 1000)
				if (r is not None) and ('dbneg' in r.text):
					pattern = r"window\.open\(dbneg\('(.*?)'\)"
					dbneg_values = re.findall(pattern, r.text)
					for k in dbneg_values:
						href = decode(k)
						c = urlparse(href.strip()).netloc.split('.')[0]
						item = Listitem()
						item.label = f'{c} - {italic(tenm)}'
						item.info['mediatype'] = 'episode'
						item.art['thumb'] = item.art['poster'] = bg_poster
						item.set_callback(play_mv, href, title, idk)
						yield item
			else:
				yield quangcao()
		except:
			yield quangcao()
@Resolver.register
def list_mv(plugin, href, title, idk):
	try:
		u = fu(href)
		with ThreadPoolExecutor(2) as ex:
			f1 = ex.submit(resolve, u)
			f2 = ex.submit(subvidto, idk)
		return listqc(title, f2.result(), f1.result())
	except:
		return listqc(title, news, qc)
@Resolver.register
def play_mv(plugin, href, title, idk):
	try:
		with ThreadPoolExecutor(2) as ex:
			f1 = ex.submit(resolve, href)
			f2 = ex.submit(subvidto, idk)
		return listqc(title, f2.result(), f1.result())
	except:
		return listqc(title, news, qc)