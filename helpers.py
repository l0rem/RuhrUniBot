import requests
from telegram import Update
from bs4 import BeautifulSoup


def get_mensa(link='https://el.rub.de/mobile/mensa/'):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    essen = soup.find('div', id='alles')
    divs = essen.find_all('div')
    types = list()
    food = list()

    for div in divs:
        if div['id'] == 'head':
            types.append(div.next.next)
            food.append(list())
        elif div['id'] == 'content':
            price = div.find('br').next
            food[-1].append(div.next + '|||' + price)
    end = dict()
    for t in types:
        l = list()
        for f in food[types.index(t)]:
            l.append(f)
        end.update({t: l})
    return end


def get_cid(update: Update):

    return update.effective_message.chat.id


def get_uid(update: Update):

    return update.effective_message.from_user.id

print(get_mensa())