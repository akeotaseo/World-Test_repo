from codequick import Route, Listitem
@Route.register
def index_tinthethao(plugin):
	T = {
	'UCndcERoL9eG-XNljgUk1Gag': 'VFF',
	'UCqOmFFbm6NBv_1u9hnIZJmA': 'VPF',
	'UCrI4iNMPZ2vT_G-TqRO6yrw': 'VTV thể thao',
	'UCmn1v6lrIDZghUfbxXaorUw': 'Tạp chí bóng đá',
	'UCF0VFBZu-5SRJXMV_FMysEA': 'Bongdaplus',
	'UC4LvrpNXujjbGOS4RDvr41g': 'FPT bóng đá',
	'UCAKECJFTsS-QnggdDZD3y4Q': 'F Sports',
	'UCisgkf7-vE5k5sVhfSiUEow': 'Next Sports',
	'UC9xeuekJd88ku9LDcmGdUOA': 'K+ Sports',
	'UCIWo7q6irZUBaoPOrlf5IVw': 'On Sports',
	'UCOEucCL9r4YfNZ9Es6G-g9Q': 'On Sports Plus',
	'UCljFFNaQoJWeP91Bz4m_3bw': 'FPT bóng đá Việt',
	'UCEwAazC_ewgN5PPnR9vxFKA': 'Quán thể thao',
	'UC4FXEYiVVUdibNnqAnzdscw': 'Việt Nam Sport',
	'UCX_6zvzkYvRM1bDIpz802FA': 'BLV Quang Huy',
	'UCQqSJr6WYH0Bq7mrlFhzWDw': 'BLV Anh Quân',
	'UCbPF5L84DIv7zGg9mCqfGtw': 'BLV Tạ Biên Cương',
	'UCCgCw-IJYpse4qnOCvvcitA': 'Tuyền văn hoá',
	'UCtowbSVJlDLjgs-5qsznSTA': 'Cảm bóng đá',
	'UCyIOLARJsMYFbQ-7-P-4DIA': 'Nhà báo Minh Hải',
	'UCFEdjI6bdng-T1CWlqwSC1g': 'Anh Quân tin mới',
	'UCCBwmJaVIB220c5sWdE28XQ': 'Anh Quân bóng đá Việt'
	}
	for k in T:
		yield Listitem.youtube(k, label=T[k])