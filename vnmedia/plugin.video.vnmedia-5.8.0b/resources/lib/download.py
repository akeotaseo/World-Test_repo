from codequick import Script
from urllib.parse import urlparse, unquote
from resources.lib.kedon import getfs, __addonnoti__, useragentdf
from requests import get
from codequick.utils import ensure_unicode
from xbmcgui import DialogProgress, Dialog
from xbmcvfs import translatePath
from time import time
from os.path import join, basename, exists
from os import unlink
from codequick.utils import color
import sys
@Script.register
def downloadfs(plugin, x):
    url = getfs(x)
    dp = DialogProgress()
    pathx = ensure_unicode(Script.setting.get_string('dl_folder')) if Script.setting.get_string('dl_folder') else join(translatePath('special://home/media/'))
    filename = unquote(basename(urlparse(url).path))
    zippath = join(pathx + filename)
    if exists(zippath):
        unlink(zippath)
    dp.create(f'{__addonnoti__} đang tải...', f'Đang tải tệp {filename}')
    dp.update(0, f'Đang tải tệp {filename}')
    f = open(zippath, 'wb')
    zipresp = get(url, stream=True, timeout=30, headers={'user-agent': useragentdf})
    if not zipresp:
        Dialog().ok(__addonnoti__, 'Tập tin này bị hỏng')
        sys.exit()
    else:
        total = zipresp.headers.get('content-length')
    if total is not None:
        downloaded = 0
        total = int(total)
        start_time = time()
        mb = 1024*1024
        for chunk in zipresp.iter_content(chunk_size=max(int(total/512), mb)):
            downloaded += len(chunk)
            f.write(chunk)
            done = int(1e2 * downloaded/total)
            kbps_speed = downloaded/(time() - start_time)
            eta = (total - downloaded)/kbps_speed if kbps_speed > 0 and not done >= 100 else 0
            kbps_speed = kbps_speed/1024
            type_speed = 'KB'
            if kbps_speed >= 1024:
                kbps_speed = kbps_speed/1024
                type_speed = 'MB'
            currently_downloaded = f'Đã tải: {downloaded/mb:.02f}MB / {total/mb:.02f}MB'
            speed = f'Tốc độ tải: {kbps_speed:.02f} {type_speed}/s'
            div = divmod(eta, 60)
            speed += f' - Còn {int(div[0]):02}:{int(div[1]):02}'
            if dp.iscanceled():
                dp.close()
                sys.exit()
            dp.update(done, f'{filename}\n{currently_downloaded}\n{speed}')
    else:
        f.write(zipresp.content)
    dp.close()
@Script.register
def speedtestfs(plugin):
    dp = DialogProgress()
    dp.create(__addonnoti__, 'Đang đo tốc độ mạng')
    dp.update(0, 'Đang kết nối tới máy chủ')
    zipresp = get('https://www.fshare.vn/file/3EHWU9EZH8F6', stream=True, timeout=100, headers={'user-agent': useragentdf})
    if not zipresp:
        Dialog().ok(__addonnoti__, 'Lỗi kết nối')
        sys.exit()
    else:
        total = zipresp.headers.get('content-length')
    try:
        if total is not None:
            downloaded = 0
            total = int(total)
            start_time = time()
            mb = 1024*1024
            for chunk in zipresp.iter_content(chunk_size=max(int(total/512), mb)):
                downloaded += len(chunk)
                done = int(1e2 * downloaded/total)
                kbps_speed = downloaded/(time() - start_time)
                eta = (total - downloaded)/kbps_speed if kbps_speed > 0 and not done >= 100 else 0
                kbps_speed = kbps_speed/1024
                type_speed = 'KB'
                if kbps_speed >= 1024:
                    kbps_speed = kbps_speed/1024
                    type_speed = 'MB'
                td = f'{kbps_speed:.02f} {type_speed}/s'
                speed = f'Tốc độ tải: {color(td, "yellow")}'
                if dp.iscanceled():
                    dp.close()
                    sys.exit()
                dp.update(done, speed)
            file_size = total/mb
            download_time = time() - start_time
            speed_kbps = int(file_size/download_time)
            if speed_kbps <= 5:
                quality = 'SD 480p'
            elif speed_kbps <= 10:
                quality = 'HD 720p'
            elif speed_kbps <= 20:
                quality = 'FHD 1080p'
            elif speed_kbps <= 30:
                quality = '2K 1440p'
            elif speed_kbps <= 50:
                quality = '4K 2160p'
            else:
                quality = '8K 4320p'
            Dialog().ok(__addonnoti__, f'Băng thông hiện tại: {color(speed_kbps*8, "yellow")} Mbps\nChất lượng video đề xuất: {color(quality, "yellow")}')
            sys.exit()
        else:
            f.write(zipresp.content)
    except:
        sys.exit()
    dp.close()