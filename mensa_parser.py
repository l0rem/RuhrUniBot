import requests
from bs4 import BeautifulSoup
import datetime

url = 'https://www.akafoe.de/gastronomie/speiseplaene-der-mensen/ruhr-universitaet-bochum'


def parse_mensa(date='today'):
    data = requests.get(url).text

    soup = BeautifulSoup(data,
                         features='html.parser')

    data = soup.find_all('div', class_='container')[-3]

    datespan = data.find('h3').next.split(' ')[1].split('.')
    start_date = datetime.date(int(datespan[-1]), int(datespan[1]), int(datespan[0]))
    print(start_date.weekday())
    allowed_dates = list()

    for i in range(10):
        print(i)


    sections = data.find_all('div', class_='col-md-6')

    if date is 'today':
        today = int(str(datetime.datetime.today()).split(' ')[0].split('-')[-1])
    else:
        today = date

    if today >= datespan[0]:
        dist = (today - datespan[0]) * 2
    else:
        dist = (datespan[1] - today) * 2

    dishes = (str(sections[dist]) + str(sections[dist + 1])).split('<hr/>')
    data = dict()
    for sort in dishes:
        dish = BeautifulSoup(sort,
                             features='html.parser')
        type_ = dish.find('h3').next
        data.update({type_: []})
        foods = dish.find_all('div', class_='item')
        for food in foods:
            title = food.find('h4').next
            tags = food.find('small').next
            price = food.find('div', class_='price').next
            old_data = data.get(type_)
            old_data.append([title, tags, price])
            data.update({type_: old_data})
    return data


print(parse_mensa())


