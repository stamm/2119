import requests, re, math, json
from bs4 import BeautifulSoup

data_common = [
  ('house', ''),
  ('rooms', ''),
  ('square[]', '29.3'),
  ('square[]', '90.4'),
  ('price[]', '5.7'),
  ('price[]', '20'),
  ('floor[]', '2'),
  ('floor[]', '23'),
]

data_count = data_common + [('getCount', 'true')]

url = 'https://2119.ru/search/parametrical/'
responce = requests.post(url, data=data_count, headers={'X-Requested-With': 'XMLHttpRequest'})
count = int(responce.content)
# print("count = %d" % count)

flats = []

for i in range(1, math.ceil(count/10) + 1):
    # print("page = %d" % i)
    data = data_common + [
        ('page', i),
        ('pageType', 'table'),
        ('sort', 'price'),
        ('sortBy', 'asc'),
    ]
    responce = requests.post(url, data=data)

    soup = BeautifulSoup(responce.content, 'html.parser')
    items = soup.find_all(class_='table-row')

    for item in items:
        flats.append({
            'number': int(item.find(class_='-number').find(class_='table-value').get_text().strip()),
            'price': int(re.compile("([0-9 ]+)").match(item.find(class_='-price').find(class_='table-value').span.get_text().strip()).group(1).replace(" ", "")),
            'square': float(item.find(class_='-square').find(class_='table-value').get_text().strip()),
            'floor': int(item.find(class_='-floor').find(class_='table-value').get_text().strip()),
            'house': int(item.find(class_='-house').find(class_='table-value').get_text().strip()),
            'rooms': int(item.find(class_='-rooms').find(class_='table-value').get_text().strip()),
        })

print(json.dumps(flats))
