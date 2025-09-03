from codequick import Route, Listitem, Script
from xbmcvfs import listdir, translatePath
from codequick.utils import ensure_unicode
from os.path import join, getsize
from os import remove
from xbmc import executebuiltin
@Route.register
def index_datai(plugin):
    yield []
    folder_path = ensure_unicode(Script.setting.get_string('dl_folder')) if Script.setting.get_string('dl_folder') else join(translatePath('special://home/media/'))
    d = (l for k in listdir(folder_path) for l in k)
    h = (k for k in d if d)
    for k in h:
        item = Listitem()
        item.label = k
        p = f'{folder_path}{k}'
        item.path =p
        item.info['mediatype'] = 'episode'
        item.info['size'] = getsize(p)
        item.info['plot'] = f'{k}\nNguồn: https://fshare.vn'
        item.context.script(delfile, 'Xoá tệp', p)
        yield item
@Script.register
def delfile(plugin, file_path):
    remove(file_path)
    executebuiltin('Container.Refresh()')