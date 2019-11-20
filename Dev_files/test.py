from requests_html import HTMLSession
session = HTMLSession()

# Генерируем ссылку
base_url = 'https://www.uniprot.org/uniprot/?query=*&offset='
number = 25

# Получаем все результаты
kek = str()
for x in range(12):
	url = base_url + str(number*x)
	r = session.get(url)
	for y in r.html.find('.entryID'):
		kek += f"{y.text} "

print(kek)