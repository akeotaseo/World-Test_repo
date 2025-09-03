from codequick import Route, Listitem
from resources.lib.kedon import getlink, quangcao, yttk
from urllib.parse import quote_plus
from datetime import date
import re
tmdbAPI='https://api.themoviedb.org/3'
apimdb='b030404650f279792a8d3287232358e3'
apiKey = f'{apimdb}&language=vi-VN'
append = 'alternative_titles,credits,external_ids,keywords,videos,recommendations'
@Route.register
def index_fsmdb(plugin):
	yield Listitem.search(ds_fsmdb)
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
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/on.png'
		item.set_callback(ds_fsmdb, dulieu[k], 1)
		yield item
@Route.register
def ds_fsmdb(plugin, search_query=None, next_page=None):
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
					try:
						try:
							phathanh = k['release_date']
						except:
							phathanh = k['first_air_date']
					except:
						phathanh = date.today()
				item = Listitem()
				item.label = ten
				item.info['plot'] = f"{k['overview']}\nNguồn: https://themoviedb.org"
				item.info['mediatype'] = 'tvshow'
				item.info['premiered'] = phathanh
				item.info['rating'] = float(k['vote_average'])
				item.info['dbid'] = k['id']
				item.info['trailer'] = yttk(ten)
				item.art['thumb'] = item.art['poster'] = f"https://image.tmdb.org/t/p/w500{k['poster_path']}"
				item.set_callback(Route.ref('/resources/lib/mkd/onfshare/timfshare:searchfs'), ten)
				yield item
			if next_page < rj['total_pages']:
				item1 = Listitem()
				item1.label = f'Trang {str(int(next_page) + 1)}'
				item1.info['mediatype'] = 'tvshow'
				item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
				item1.set_callback(ds_fsmdb, match, next_page + 1)
				yield item1
		else:
			yield quangcao()
	except:
		yield quangcao()