import requests
from bs4 import BeautifulSoup
import datetime

url = 'https://www.akafoe.de/gastronomie/speiseplaene-der-mensen/ruhr-universitaet-bochum'


def parse_mensa(date=None, return_dates=False):
    data = requests.get(url).text

    soup = BeautifulSoup(data,
                         features='html.parser')

    data = soup.find_all('div', class_='container')[-3]

    datespan = data.find('h3').next.split(' ')[1].split('.')
    start_date = datetime.date(int(datespan[-1]), int(datespan[1]), int(datespan[0]))
    allowed_dates = list()
    allowed_dates.append(start_date)

    k = 0
    for i in range(1, 14):
        try:
            d = datetime.date(int(datespan[-1]), int(datespan[1]), int(datespan[0]) + i)
        except ValueError:
            if k == 0:
                d = datetime.date(int(datespan[-1]), int(datespan[1]) + 1, 1)
                k = i - 1
            else:
                d = datetime.date(int(datespan[-1]), int(datespan[1]) + 1, i - k)
        if d.weekday() <= 4:
            allowed_dates.append(d)

    if return_dates:
        return allowed_dates

    sections = data.find_all('div', class_='col-md-6')

    if date is None:
        day_needed = datetime.datetime.today().date()
    else:
        day_needed = datetime.date(int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2]))
    if day_needed not in allowed_dates:
        return False
    else:
        dist = allowed_dates.index(day_needed) * 2

    if return_dates:
        return allowed_dates

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





