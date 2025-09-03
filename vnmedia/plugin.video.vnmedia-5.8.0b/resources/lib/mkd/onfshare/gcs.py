from codequick import Route, Listitem, Script, Resolver
from resources.lib.kedon import getlink, fu, yttk, getrow, quangcao, __addonnoti__
from json import loads
from urllib.parse import unquote
from codequick.utils import color
import re
@Route.register
def index_gcs(plugin):
    yield []
    u = Script.setting.get_string('TextURL')
    if u:
        try:
            x = fu(u)
            if 'docs.google.com' in x:
                if 'gid' in x:
                    timid = re.findall(r'/d/(.*?)/.*?gid=(\d+)', x)
                    sid = timid[0][0]
                    gid = timid[0][1]
                else:
                    sid = re.findall(r'/d/(.*?)/', x)[0]
                    gid = '0'
                url = f'https://docs.google.com/spreadsheets/d/{sid}/gviz/tq?gid={gid}&headers=1'
                resp = getlink(url, url, 600)
                if (resp is not None):
                    try:
                        noi = re.search(r'\{.*\}', resp.text)[0]
                        m = loads(noi)
                        cols = m['table']['cols']
                        rows = m['table']['rows']
                        kenh = cols[1]['label']
                        if 'http' in kenh:
                            lcols = len(cols)
                            item = Listitem()
                            tenm = cols[0]['label']
                            item.label = tenm
                            item.info['trailer'] = yttk(tenm)
                            imgfs = cols[2]['label'] if lcols > 2 else 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
                            item.art['thumb'] = item.art['poster'] = imgfs
                            if lcols > 3:
                                item.info['plot'] = f"{cols[3]['label']}\nDữ liệu được máy tính thu thập từ Internet"
                            else:
                                item.info['plot'] = f'{tenm}\nNguồn: {u}'
                            item.art['fanart'] = cols[4]['label'] if lcols > 4 else imgfs
                            set_item_callbacks(item, kenh, tenm, imgfs)
                            yield item
                        for cow in cols:
                            p = cow['label']
                            if '|http' in p:
                                yield create_listitem_from_link(p, color('VN Media', 'yellow'))
                        for row in rows:
                            k = getrow(row['c'][0])
                            if '|http' in k:
                                yield create_listitem_from_link(k, color('VN Media', 'yellow'))
                            elif 'http' in getrow(row['c'][1]):
                                lrow = len(row['c'])
                                item = Listitem()
                                item.label = k
                                item.info['trailer'] = yttk(k)
                                kenh = getrow(row['c'][1])
                                imgfs = getrow(row['c'][2]) if lrow > 2 else 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
                                item.art['thumb'] = item.art['poster'] = imgfs
                                if lrow > 3:
                                    item.info['plot'] = f"{getrow(row['c'][3])}\nDữ liệu được máy tính thu thập từ Internet"
                                else:
                                    item.info['plot'] = f'{k}\nNguồn: {u}'
                                item.art['fanart'] = getrow(row['c'][4]) if lrow > 4 else imgfs
                                set_item_callbacks(item, kenh, k, imgfs)
                                yield item
                    except:
                        yield []
            else:
                respx = getlink(u, u, 600)
                ri = respx.iter_lines(decode_unicode=True)
                tach = (ll.rstrip() for ll in ri if ll.strip())
                for k in tach:
                    yield listitemvmf(k, color('VN Media', 'yellow'))
        except:
            yield quangcao()
    else:
        Script.notify(__addonnoti__, 'Vui lòng nhập Link trong cài đặt của VN Media')
        yield quangcao()
@Route.register
def listgg_gcs(plugin, urltext=None, title=None):
    yield []
    if any((urltext is None, title is None)):
        pass
    else:
        try:
            if 'gid' in urltext:
                timid = re.findall(r'/d/(.+?)/.+?gid=(\d+)', urltext)
                sid = timid[0][0]
                gid = timid[0][1]
            else:
                sid = re.findall(r'/d/(.*?)/', urltext)[0]
                gid = '0'
            url = f'https://docs.google.com/spreadsheets/d/{sid}/gviz/tq?gid={gid}&headers=1'
            resp = getlink(url, url, 600)
            if (resp is not None):
                try:
                    noi = re.search(r'\{.*\}', resp.text)[0]
                    m = loads(noi)
                    cols = m['table']['cols']
                    rows = m['table']['rows']
                    kenh = cols[1]['label']
                    if 'http' in kenh:
                        lcols = len(cols)
                        item = Listitem()
                        tenm = cols[0]['label']
                        item.label = tenm
                        item.info['trailer'] = yttk(tenm)
                        imgfs = cols[2]['label'] if lcols > 2 else 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
                        item.art['thumb'] = item.art['poster'] = imgfs
                        if lcols > 3:
                            item.info['plot'] = f"{cols[3]['label']}\nNguồn: {urltext}"
                        else:
                            item.info['plot'] = f'{tenm}\nNguồn: {urltext}'
                        item.art['fanart'] = cols[4]['label'] if lcols > 4 else imgfs
                        set_item_callbacks(item, kenh, tenm, imgfs)
                        yield item
                    for cow in cols:
                        p = cow['label']
                        if '|http' in p:
                            yield create_listitem_from_link(p, title)
                    for row in rows:
                        k = getrow(row['c'][0])
                        if '|http' in k:
                            yield create_listitem_from_link(k, title)
                        elif 'http' in getrow(row['c'][1]):
                            lrow = len(row['c'])
                            item = Listitem()
                            item.label = k
                            item.info['trailer'] = yttk(k)
                            kenh = getrow(row['c'][1])
                            imgfs = getrow(row['c'][2]) if lrow > 2 else 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
                            item.art['thumb'] = item.art['poster'] = imgfs
                            if lrow > 3:
                                item.info['plot'] = f"{getrow(row['c'][3])}\nDữ liệu được máy tính thu thập từ Internet"
                            else:
                                item.info['plot'] = f'{k}\nNguồn: {urltext}'
                            item.art['fanart'] = getrow(row['c'][4]) if lrow > 4 else imgfs
                            set_item_callbacks(item, kenh, k, imgfs)
                            yield item
                except:
                    yield quangcao()
            else:
                yield quangcao()
        except:
            yield quangcao()
@Route.register
def listvmf_gcs(plugin, url=None, title=None):
    yield []
    if any((url is None, title is None)):
        pass
    else:
        try:
            resp = getlink(url, url, 100)
            if (resp is not None) and (resp.content):
                ri = resp.iter_lines(decode_unicode=True)
                tach = (ll.rstrip() for ll in ri if ll.strip())
                for k in tach:
                    yield listitemvmf(k, color('VN Media', 'yellow'))
            else:
                yield quangcao()
        except:
            yield quangcao()
def set_item_callbacks(item, kenh, title, imgfs):
    script = Script.ref('/resources/lib/mkd/onfshare/ifshare:tfavo')
    taifshare = Script.setting.get_string('taifshare')
    if 'fshare.vn/folder' in kenh:
        item.info['mediatype'] = 'tvshow'
        item.context.script(script, 'Thêm vào Fshare Favorite', kenh)
        item.set_callback(Route.ref('/resources/lib/mkd/onfshare/ifshare:index_fs'), kenh, 0, imgfs)
    elif 'fshare.vn/file' in kenh:
        item.info['mediatype'] = 'episode'
        item.context.script(script, 'Thêm vào Fshare Favorite', kenh)
        if taifshare == 'true':
            item.context.script(Script.ref('/resources/lib/download:downloadfs'), 'Tải về', kenh)
        item.set_callback(Resolver.ref('/resources/lib/kedon:play_fs'), kenh, title)
    elif 'docs.google.com' in kenh:
        item.info['mediatype'] = 'tvshow'
        item.set_callback(listgg_gcs, kenh, title)
    elif 'VMF' in kenh:
        item.info['mediatype'] = 'tvshow'
        item.set_callback(listvmf_gcs, kenh.replace('VMF-', ''), title)
    else:
        item.info['mediatype'] = 'episode'
        item.set_callback(Resolver.ref('/resources/lib/kedon:play_vnm'), unquote(kenh), title)
def create_listitem_from_link(link, title):
    tachhat = link.split('|')
    ltach = len(tachhat)
    if tachhat[1] and ltach > 1:
        item = Listitem()
        kenh = tachhat[1]
        tenm = tachhat[0].translate(str.maketrans({'*': '', '@': ''}))
        item.label = tenm
        item.info['trailer'] = yttk(tenm)
        imgfs = tachhat[3] if ltach > 3 else 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
        item.art['thumb'] = item.art['poster'] = imgfs
        if ltach > 4:
            item.info['plot'] = f'{tachhat[4]}\nDữ liệu được máy tính thu thập từ Internet'
        else:
            item.info['plot'] = f'{tenm}\nDữ liệu được máy tính thu thập từ Internet'
        item.art['fanart'] = tachhat[5] if ltach > 5 else imgfs
        set_item_callbacks(item, kenh, tenm, imgfs)
        return item
def listitemvmf(link, title):
    tachhat = link.split('|')
    ltach = len(tachhat)
    if ltach > 1:
        item = Listitem()
        kenh = tachhat[1]
        tenm = tachhat[0].translate(str.maketrans({'*': '', '@': ''}))
        item.label = tenm
        item.info['trailer'] = yttk(tenm)
        imgfs = tachhat[3] if ltach > 3 else 'https://raw.githubusercontent.com/kenvnm/kvn/main/fshare.png'
        item.art['thumb'] = item.art['poster'] = imgfs
        if ltach > 4:
            item.info['plot'] = f'{tachhat[4]}\nDữ liệu được máy tính thu thập từ Internet'
        else:
            item.info['plot'] = f'{tenm}\nDữ liệu được máy tính thu thập từ Internet'
        set_item_callbacks(item, kenh, tenm, imgfs)
        return item