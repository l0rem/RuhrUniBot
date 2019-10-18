import requests
from telegram import Update
from telegram.ext import callbackcontext
from dbmodels import User
import datetime
from bs4 import BeautifulSoup


def get_mensa(link='https://el.rub.de/mobile/mensa/'):
    r = requests.get(link, verify=False)
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


def create_user(uid, username):
    User.create(uid=uid,
                username=username,
                joined_on=str(datetime.datetime.now()).split('.')[0])


def clean_chat(update: Update, context: callbackcontext):

    if 'message_ids' in context.chat_data.keys():

        cid = get_cid(update)

        for mid in context.chat_data['message_ids']:
            try:
                context.bot.delete_message(chat_id=cid,
                                           message_id=mid)
            except Exception as e:
                print(e)

    context.chat_data['message_ids'] = list()
