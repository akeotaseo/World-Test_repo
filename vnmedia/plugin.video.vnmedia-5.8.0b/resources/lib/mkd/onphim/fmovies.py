from codequick import Route, Listitem, Resolver
from resources.lib.kedon import listqc, yttk, qc, news, getlink, quangcao, referer, stream, replace_all, gioithieu
from bs4 import BeautifulSoup
from urllib.parse import unquote, quote_plus, urlparse
from concurrent.futures import ThreadPoolExecutor
from resolveurl import resolve
from resolveurl.lib.jsunpack import unpack
from base64 import b64encode, b64decode
from codequick.utils import italic
import re
fmo = 'https://fmovies24.to'
def maketrans():
	bflixKey = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
	return bytes.maketrans(bflixKey, bflixKey)
def encode2(x):
	return b64encode(x).translate(maketrans())
def decode2(x):
	try:
		y = x.translate(maketrans())
	except:
		y = str(x).translate(maketrans())
	return b64decode(y)
def endEN(t, n):
	return t + n
def VHtgA(t, n):
	return t % n
def dec2(t, n) :
	o = []
	s = list(range(256))
	u = 0
	h = ''
	for e in range(256):
		u = endEN(u + s[e],ord(t[e % len(t)])) % 256
		o = s[e]
		s[e] = s[u]
		s[u] = o
	e = 0
	u = 0
	length = len(n)
	for c in range(length):
		e = (e + 1) % 256
		o = s[e]
		u = (u + s[e]) % 256
		s[e] = s[u]
		s[u] = o
		char_value = ord(n[c]) if isinstance(n[c], str) else n[c]
		h += chr(char_value ^ s[(s[e] + s[u]) % 256])
	return h
def encode_id(idp):
	ukey = 'https://raw.githubusercontent.com/Ciarands/vidsrc-keys/main/keys.json'
	k = getlink(ukey, ukey, 300).json()
	c1 = dec2(k[0], idp).encode('Latin_1')
	c2 = dec2(k[1], c1).encode('Latin_1')
	return b64encode(c2).decode('utf-8').replace('/','_')
def but(t):
	o = ''
	for s, char in enumerate(t):
		u = ord(char)
		if u != 0:
			if s % 8 == 2:
				u -= 2
			elif s % 8 == 4 or s % 8 == 7:
				u += 2
			elif s % 8 == 0:
				u += 4
			elif s % 8 == 5 or s % 8 == 6:
				u -= 4
			elif s % 8 == 1:
				u += 3
			elif s % 8 == 3:
				u += 5
		o += chr(u)
	return o.encode('Latin_1').decode('utf-8')
def getVerid(idp):
	thaythe = {'/':'_','+':'-'}
	a = dec2('Ij4aiaQXgluXQRs6', idp).encode('Latin_1')  
	b = replace_all(thaythe, encode2(a).decode('utf-8')).encode('Latin_1')
	c = replace_all(thaythe, encode2(b).decode('utf-8'))
	d = (''.join(reversed(c))).encode('Latin_1') 
	e = replace_all(thaythe, encode2(d).decode('utf-8'))
	return but(e)
def dekoduj(r,o):
	t = []
	n = 0
	a = ''
	e = list(range(256))
	for f in range(256):
		n = (n + e[f] + ord(r[f % len(r)])) % 256
		t = e[f]
		e[f] = e[n]
		e[n] = t
	f = 0
	n = 0
	length = len(o)
	for h in range(length):
		f += 1
		n = (n + e[f % 256]) % 256
		if f not in e:
			f = 0
			e[0], e[n] = e[n], e[0]
		e[f], e[n] = e[n], e[f]
		char_value = ord(o[h]) if isinstance(o[h], str) else o[h]
		a += chr(char_value ^ e[(e[f] + e[n]) % 256])
	return a
def DecodeLink(mainurl):
	mainurl = replace_all({'_':'/','-':'+'}, mainurl)
	ac = decode2(mainurl)
	link = dekoduj('8z5Ag5wgagfsOuhz', ac)
	return unquote(link)
@Route.register
def index_fm(plugin):
	yield Listitem.search(page)
	dulieu = {
	'Phim mới': f'{fmo}/updated',
	'Thịnh hành': f'{fmo}/trending',
	'Đề xuất': f'{fmo}/filter?keyword=&sort=recently_added',
	'Ưa thích': f'{fmo}/filter?keyword=&sort=most_favourited',
	'Phim phổ biến': f'{fmo}/filter?keyword=&sort=most_watched',
	'Phim lẻ': f'{fmo}/movie',
	'Phim lẻ mới': f'{fmo}/filter?keyword=&type[]=movie&sort=release_date',
	'Phim lẻ phổ biến': f'{fmo}/filter?keyword=&type[]=movie&sort=most_watched',
	'Phim lẻ đề xuất': f'{fmo}/filter?keyword=&type[]=movie&sort=recently_added',
	'Phim lẻ ưa thích': f'{fmo}/filter?keyword=&type[]=movie&sort=most_favourited',
	'Phim bộ': f'{fmo}/tv',
	'Phim bộ mới': f'{fmo}/filter?keyword=&type[]=tv&sort=release_date',
	'Phim bộ phổ biến': f'{fmo}/filter?keyword=&type[]=tv&sort=most_watched',
	'Phim bộ đề xuất': f'{fmo}/filter?keyword=&type[]=tv&sort=recently_added',
	'Phim bộ ưa thích': f'{fmo}/filter?keyword=&type[]=tv&sort=most_favourited',
	'TOP IMDB': f'{fmo}/top-imdb'
	}
	for k in dulieu:
		item = Listitem()
		item.label = k
		item.info['mediatype'] = 'tvshow'
		item.art['thumb'] = item.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/fmovi.png'
		item.set_callback(page, dulieu[k], 1)
		yield item
@Route.register
def page(plugin, search_query=None, next_page=None):
	yield []
	try:
		if '://' not in search_query:
			next_page = 1
			sr = quote_plus(search_query)
			url = f'{fmo}/filter?keyword={sr}'
		else:
			url = search_query
		lasturl = f'{url}&page={next_page}' if '?' in url else f'{url}?page={next_page}'
		r = getlink(lasturl, url, 1000)
		if (r is not None):
			soup = BeautifulSoup(r.text, 'html.parser')
			s = soup.select('.movies .item')
			if len(s)>0:
				for k in s:
					item = Listitem()
					tenm = k.select_one('.meta a').get_text(strip=True)
					img = k.select_one('.poster img')['data-src']
					tip = k.select_one('.poster a')['data-tip']
					idp = f'{fmo}/ajax/film/tooltip/{tip}' if not tip.startswith('http') else tip
					item.label = tenm
					item.info['plot'] = f'{tenm}\nNguồn: {fmo}'
					item.info['mediatype'] = 'tvshow'
					item.art['thumb'] = item.art['poster'] = img
					item.set_callback(episode, idp, img, tenm)
					yield item
				if f'page={next_page + 1}' in r.text:
					item1 = Listitem()
					item1.label = f'Trang {next_page + 1}'
					item1.info['mediatype'] = 'tvshow'
					item1.art['thumb'] = item1.art['poster'] = 'https://raw.githubusercontent.com/kenvnm/kvn/main/next.png'
					item1.set_callback(page, url, next_page + 1)
					yield item1
			else:
				yield quangcao()
		else:
			yield quangcao()
	except:
		yield quangcao()
@Route.register
def episode(plugin, url=None, anh=None, title=None):
	yield []
	if any((url is None, anh is None, title is None)):
		pass
	else:
		try:
			r = getlink(url, url, 1000)
			soupx = BeautifulSoup(r.text, 'html.parser')
			idx = soupx.select_one('div.head div.dropdown.user-bookmark')['data-id']
			year_span = soupx.select('div.meta > span')[0].get_text(strip=True)
			mark = soupx.select('div.meta > span')[1].get_text(strip=True)
			response = getlink(f'{fmo}/ajax/episode/list/{idx}?vrf={quote_plus(getVerid(idx))}', url,-1)
			if (response is not None) and ('data-id' in response.text):
				result = response.json()['result']
				soup = BeautifulSoup(result, 'html.parser')
				soups = soup.select('div.body ul')
				title = title.strip()
				if len(soups)>1:
					v = ((k['data-season'].strip(),link.get_text(strip=True),link['data-id']) for k in soups for link in k.select('li a'))
					for k in v:
						item = Listitem()
						tenm = f'{title} - Season {k[0]} {k[1]}'
						item.label = tenm
						item.info['plot'] = f'{tenm}\nNguồn: {fmo}'
						item.info['mediatype'] = 'tvshow'
						item.info['year'] = year_span
						item.info['rating'] = float(mark)
						item.info['trailer'] = yttk(tenm)
						item.art['thumb'] = item.art['poster'] = anh
						item.set_callback(server, k[2], tenm, anh, url, mark, year_span)
						yield item
				else:
					yield gioithieu(title, title, anh)
					idp = soup.select_one('div.body ul li a')['data-id']
					r = getlink(f'{fmo}/ajax/server/list/{idp}?vrf={quote_plus(getVerid(idp))}', url,-1)
					resultx = r.json()['result']
					soupx = BeautifulSoup(resultx, 'html.parser')
					for k in soupx.select('ul li'):
						item = Listitem()
						tenm = f'{k.get_text(strip=True)} - {italic(title)}'
						item.label = tenm
						item.info['plot'] = f'{tenm}\nNguồn: {fmo}'
						item.info['mediatype'] = 'episode'
						item.info['year'] = year_span
						item.info['rating'] = float(mark)
						item.info['trailer'] = yttk(title)
						item.art['thumb'] = item.art['poster'] = anh
						item.set_callback(playfm, k['data-link-id'], title, url, idp)
						yield item
			else:
				yield quangcao()
		except:
			yield quangcao()
@Route.register
def server(plugin, idp=None, title=None, anh=None, url=None, mark=None, year_span=None):
	yield []
	if any((idp is None, anh is None, title is None, url is None, mark is None, year_span is None)):
		pass
	else:
		try:
			r = getlink(f'{fmo}/ajax/server/list/{idp}?vrf={quote_plus(getVerid(idp))}', url,-1)
			if (r is not None):
				yield gioithieu(title, title, anh)
				result = r.json()['result']
				soup = BeautifulSoup(result, 'html.parser')
				for k in soup.select('ul li'):
					item = Listitem()
					tenm = f'{k.get_text(strip=True)} - {italic(title.strip())}'
					item.label = tenm
					item.info['plot'] = f'{tenm}\nNguồn: {fmo}'
					item.info['mediatype'] = 'episode'
					item.info['year'] = year_span
					item.info['rating'] = float(mark)
					item.info['trailer'] = yttk(title)
					item.art['thumb'] = item.art['poster'] = anh
					item.set_callback(playfm, k['data-link-id'], title, url, idp)
					yield item
			else:
				yield quangcao()
		except:
			yield quangcao()
def subfm(idm, url):
	r2 = getlink(f'{fmo}/ajax/episode/subtitles/{idm}', url,-1)
	if (r2 is not None):
		try:
			js = r2.json()
			subl = ''.join(k['file'] for k in js if 'vietnam' in k['label'].lower())
		except:
			subl = news
	else:
		subl = news
	return subl
def decodeVidstream(a):
	domain = urlparse(a).netloc
	tu = f'https://{domain}/futoken'
	futoken = getlink(tu, tu,-1).text
	k=re.findall("k='([^']+)'",futoken,re.DOTALL)[0]
	if '.bz/' in a:
		query = a.split('e/')[1].split('?')
	else:
		query = a.split('/e/')[1].split('?')
	v = encode_id(query[0])
	af = [k] + [str(ord(k[i % len(k)]) + ord(char)) for i, char in enumerate(v)]
	urlk = f'https://{domain}/mediainfo/{",".join(af)}?{query[1]}'
	try:
		ff=getlink(urlk,a,-1).json()
		fil=ff['result']['sources'][0]['file']
		link=f'{stream(fil)}{referer(a)}'
	except:
		link = qc
	return link
def resol_kerox(url, ref):
	html = getlink(url, ref, -1).text
	packed = re.findall(r'(eval\(function\(p,a,c,k,e,(?:r|d).*)',html)[0]
	unpacked = unpack(packed)
	str_url = re.findall('file:"([^"]+)"',unpacked)
	stream_url = f'{stream(str_url[0])}{referer(url)}' if str_url else qc
	return stream_url
def linkfm(idm, href):
	r = getlink(f'{fmo}/ajax/server/{idm}?vrf={quote_plus(getVerid(idm))}', href, -1)
	if (r is not None):
		try:
			link = DecodeLink(r.json()['result']['url'])
			try:
				stream_url = decodeVidstream(link)
			except:
				if 'kerapoxy.' in link:
					stream_url = resol_kerox(link, href)
				else:
					stream_url = resolve(link)
		except:
			stream_url = qc
	else:
		stream_url = qc
	return stream_url
@Resolver.register
def playfm(plugin, idm, title, url, idp):
	try:
		with ThreadPoolExecutor(2) as ex:
			f1 = ex.submit(linkfm, idm, url)
			f2 = ex.submit(subfm, idp, url)
		return listqc(title, f2.result(), f1.result())
	except:
		return listqc(title, news, qc)