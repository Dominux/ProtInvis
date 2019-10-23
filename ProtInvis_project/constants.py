dyes_list = {
		'Кумасси бриллиантовый синий': ['K', 'R', 'H'],
	    'Окрашивание серебром': ['N', 'Q', 'C'],
	    'Амидовый черный': ['K', 'R', 'H'],
	    'Бромфеноловый синий': ['K', 'R', 'H'],
	    'Пирогаллоловый красный': ['K'],
	    'Sypro Ruby': ['K', 'R', 'H'],
	    'Stain-free': ['W'],
	    'Zn-имидазольное негативное окрашивание': ['H', 'C', 'Q', 'N'],
	    }

dyes_for_form = [(_, _) for _ in dyes_list.keys()]

a_replace = {
		'B': 'N',
		'Z': 'Q',
		'J': 'L',
		'X': '',
		}

aa_list = list('ACDEFGHIKLMNOPQRSTUVWY')
