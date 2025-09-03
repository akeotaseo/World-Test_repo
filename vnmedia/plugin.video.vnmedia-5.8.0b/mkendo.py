from codequick import Route, Listitem, run
@Route.register
def root(plugin, content_type='video'):
    streams = [
        ('Sports Sites', 'https://raw.githubusercontent.com/kenvnm/kvn/main/thethao.png', '/resources/lib/mkd/thethao:index_thethao')
        # ('Mplay', 'https://mi3s.top/thumb/fshare/qrcodeplay.png', '/resources/lib/mkd/onfshare/qrplay:qrplay'),
        # ('Free Film', 'https://mi3s.top/thumb/phimmienphi.png', '/resources/lib/mkd/phim:index_phim'),
        # ('Fshare', 'https://mi3s.top/thumb/fshare.png', '/resources/lib/mkd/fshare:index_fshare'),
        # ('Youtube', 'https://mi3s.top/thumb/youtube.png', '/resources/lib/mkd/ytube:index_youtube'),
        # ('Truyền hình', 'https://mi3s.top/thumb/truyenhinh.png', '/resources/lib/mkd/truyenhinh:listiptv_root'),
        # ('Thể thao', 'https://mi3s.top/thumb/thethao.png', '/resources/lib/mkd/thethao:index_thethao'),
        # ('Tin tức', 'https://mi3s.top/thumb/tintuc.png', '/resources/lib/mkd/tintuc:index_tintuc'),
        # ('Âm nhạc', 'https://mi3s.top/thumb/amnhac.png', '/resources/lib/mkd/nhac:index_amnhac'),
        # ('Thiếu nhi', 'https://mi3s.top/thumb/thieunhi.png', '/resources/lib/mkd/thieunhi:index_thieunhi'),
        # ('Giải trí', 'https://mi3s.top/thumb/giaitri.png', '/resources/lib/mkd/giaitri:index_giaitri'),
        # ('Góc chia sẻ', 'https://mi3s.top/thumb/fshare/gocchiase.png', '/resources/lib/mkd/onfshare/gcs:index_gcs'),
        # ('Tiện ích', 'https://mi3s.top/thumb/tienich.png', '/resources/lib/mkd/tienich:index_tienich')
    ]
    for name_key, banner_key, url_key in streams:
        item = Listitem()
        item.label = name_key
        item.info['mediatype'] = 'tvshow'
        item.art['thumb'] = item.art['poster'] = banner_key
        item.set_callback(Route.ref(url_key))
        yield item
if __name__ == '__main__':
    run()