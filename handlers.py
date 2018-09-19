# -*- coding: utf-8 -*-
import logging
from telegram.ext import run_async
from telegram.ext import CommandHandler, MessageHandler
from telegram import ParseMode
import datetime
from secrets import*
import requests
from dbmodels import *
import json
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


@run_async
def error(bot, update, err):
    logger.warning('Update "%s" caused error "%s"', update, err)


@run_async
def mensa_handler(bot, update):
    Menu.create_table()
    cid = update.effective_message.chat.id
    msg = '<i>Food in Mensa for today:\n\n</i>'
    today = str(datetime.datetime.today()).split(' ')[0]

    menu = Menu.select().where(Menu.date == today)
    if menu.exists():
        menu = Menu.get(Menu.date == today)
        for title in titles:
            msg += '<b>{}</b>\n'.format(title)
            food = list()
            if titles.index(title) == 0:
                food = json.loads(menu.tipp)
            elif titles.index(title) == 1:
                food = json.loads(menu.komponentenessen)
            elif titles.index(title) == 2:
                food = json.loads(menu.beilagen)
            elif titles.index(title) == 3:
                food = json.loads(menu.aktionen)
            elif titles.index(title) == 4:
                food = json.loads(menu.suppe)

            for sp in food:
                price = sp.split('|||')[1].split('/')[0]
                msg += '{} - <code>{}</code>\n'.format(sp.split('|||')[0], price)
            msg += '\n  '
    else:
        menu = Menu.create(date=today)
        food = get_mensa()
        for elem in food:
            msg += '<b>{}</b>\n'.format(elem)

            for sp in food.get(elem):
                price = sp.split('|||')[1].split('/')[0]
                if elem in titles:
                    if elem == titles[0]:
                        f = json.loads(menu.tipp)
                        f.append(sp)
                        menu.tipp = json.dumps(f)
                    elif elem == titles[1]:
                        f = json.loads(menu.komponentenessen)
                        f.append(sp)
                        menu.komponentenessen = json.dumps(f)
                    elif elem == titles[2]:
                        f = json.loads(menu.beilagen)
                        f.append(sp)
                        menu.beilagen = json.dumps(f)
                    elif elem == titles[3]:
                        f = json.loads(menu.aktionen)
                        f.append(sp)
                        menu.aktionen = json.dumps(f)
                    elif elem == titles[4]:
                        f = json.loads(menu.suppe)
                        f.append(sp)
                        menu.suppe = json.dumps(f)
                    else:
                        f = json.loads(menu.extra)
                        f.append(sp)
                        menu.extra = json.dumps(f)
                menu.save()
                msg += '{} - <code>{}</code>\n'.format(sp.split('|||')[0], price)

            msg += '\n'
        menu.save()
    bot.send_message(cid,
                     msg,
                     parse_mode=ParseMode.HTML)


mensa_h = CommandHandler('mensa', mensa_handler)


def get_mensa(link=url):
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


def get_times():
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    time = soup.find('div', id='zeiten')
    divs = time.find_all('div')
    bs = list()
    ts = list()
    for div in divs:
        if div['id'] == 'head':
            bs.append(div.next.next)
        elif div['id'] == 'content':
            ts.append(div.next)
    end = dict()
    for elem in bs:
        end.update({elem: ts[bs.index(elem)]})
    return end


@run_async
def times_handler(bot, update):
    cid = update.effective_message.chat.id
    #msg = 'Öffnungszeiten for today:\n\n'
    #times = get_times()
    #for time in times:
    #    msg += '<b>{}</b>\n'.format(time)
    #    msg += '<i>{}</i>'.format(times.get(time))
    #    msg += '\n\n'
    bot.send_message(cid,
                     times,
                     parse_mode=ParseMode.HTML)


times_h = CommandHandler('times', times_handler)


@run_async
def voronezh_handler(bot, update):
    cid = update.effective_message.chat.id
    bot.send_photo(cid,
                   fid,
                   caption='<b>VORONEZH\' NE DOGONISH!</b>',
                   parse_mode=ParseMode.HTML)


voronezh_h = CommandHandler('voronezh', voronezh_handler)


def get_explains():
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    explains = soup.find('div', id='stoffe')
    divs = explains.find_all('div')
    explains = dict()
    for div in divs:
        txt = div.next
        shrt = txt.split(':')[0]
        txt = txt.split(':')[1]
        explains.update({shrt: txt})
    return explains


@run_async
def explain_handler(bot, update):
    cid = update.effective_message.chat.id
    #msg = 'Here are Inhaltsstoffe:\n\n'
    #exp = get_explains()
    #f  or e in exp:
    #    msg += '<b>{}:</b> {}\n'.format(e, exp.get(e))

    bot.send_message(cid,
                     explanation,
                     parse_mode=ParseMode.HTML)


explain_h = CommandHandler('explain', explain_handler)


explain_h = CommandHandler('explain', explain_handler)


@run_async
def menser(bot, job):
    bot.send_message(qcid,
                     '<code>Good morning, chat!</code>',
                     parse_mode=ParseMode.HTML)
    food = get_mensa()
    msg = '<i>Food in Mensa for today:\n\n</i>'
    for elem in food:
        msg += '<b>{}</b    >\n'.format(elem)
        for sp in food.get(elem):
            price = sp.split('|||')[1].split('/')[0]
            msg += '{} - <code>{}</code>\n'.format(sp.split('|||')[0], price)
        msg += '\n'

    bot.send_message(qcid,
                     msg,
                     parse_mode=ParseMode.HTML)


@run_async
def tomorrower(bot, job):
    weekday = datetime.datetime.today().weekday()
    if weekday >= 5:
        bot.send_message(qcid,
                         '<code>Hey there!</code>\nTheres no food for tomorrow :(',
                         parse_mode=ParseMode.HTML)
        return
    else:
        weekday += 2
    link = 'https://el.rub.de/mobile/mensa/index.php?tag={}'.format(weekday)
    bot.send_message(qcid,
                     '<code>Good evening, chat!</code>',
                     parse_mode=ParseMode.HTML)
    food = get_mensa(link)
    msg = '<i>Food in Mensa for tomorrow:\n\n</i>'
    for elem in food:
        msg += '<b>{}</b    >\n'.format(elem)
        for sp in food.get(elem):
            price = sp.split('|||')[1].split('/')[0]
            msg += '{} - <code>{}</code>\n'.format(sp.split('|||')[0], price)
        msg += '\n'

    bot.send_message(qcid,
                     msg,
                     parse_mode=ParseMode.HTML)


@run_async
def test_handler(bot, update):
    cid = update.effective_message.chat.id
    print(update)


test_h = MessageHandler(callback=test_handler, filters=())


@run_async
def start_handler(bot, update):
    cid = update.effective_message.chat.id
    bot.send_message(cid,
                     '<b>Hey!\n</b>This is bot for Ruhr University of Bochum. '
                     'Its alternative to RUB Mobile und rub.de .\n'
                     'To get list of supported commands use /help .',
                     parse_mode=ParseMode.HTML)


start_h = CommandHandler('start', start_handler)


@run_async
def help_handler(bot, update):
    cid = update.effective_message.chat.id
    bot.send_message(
        cid,
        '<b>List of supported commands:</b>\n'
        '/mensa - Get menu in RUBMensa for today\n'
        '/tomorrow - Get menu in RUBMensa for tomorrow\n'
        '/explain - Get explanations for Mensa menu\n'
        '/times - Get opening hours of Mensa\n'
        '/map - Get map of RUB\n'
        '/fristen_w - Get fristen for Wintersemester\n'
        '/fristen_s - Get fristen for Sommersemester\n',
        parse_mode=ParseMode.HTML
    )


help_h = CommandHandler('help', help_handler)


@run_async
def map_handler(bot, update):
    cid = update.effective_message.chat.id
    bot.send_photo(cid,
                   rub_map,
                   caption='By @RuhrUniBot')


map_h = CommandHandler('map', map_handler)


def get_fristen():
    url = 'https://www.ruhr-uni-bochum.de/studierendensekretariat/studium/fristen.html.de'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    print(soup.find('table'))


@run_async
def fristenw_handler(bot, update):
    cid = update.effective_message.chat.id
    msg = '<b>Fristen for Wintersemester</b>'
    bot.send_document(cid,
                      fristen_w,
                      filename='Fristen Wintersemester 18/19',
                      caption=msg,
                      parse_mode=ParseMode.HTML)


fristenw_h = CommandHandler('fristen_w', fristenw_handler)


@run_async
def fristens_handler(bot, update):
    cid = update.effective_message.chat.id
    msg = '<b>Fristen for Sommersemester</b>'
    bot.send_document(cid,
                      fristen_s,
                      filename='Fristen Sommersemester 18',
                      caption=msg,
                      parse_mode=ParseMode.HTML)


fristens_h = CommandHandler('fristen_s', fristens_handler)


@run_async
def tomorrow_handler(bot, update):
    cid = update.effective_message.chat.id
    weekday = datetime.datetime.today().weekday()
    if weekday >= 5:
        bot.send_message(cid,
                         '<code>Hey there!</code>\nTheres no food for tomorrow :(',
                         parse_mode=ParseMode.HTML)
        return
    else:
        weekday += 2
    link = 'https://el.rub.de/mobile/mensa/index.php?tag={}'.format(weekday)
    food = get_mensa(link)
    msg = '<i>Food in Mensa for tomorrow:\n\n</i>'
    for elem in food:
        msg += '<b>{}</b>\n'.format(elem)
        for sp in food.get(elem):
            price = sp.split('|||')[1].split('/')[0]
            msg += '{} - <code>{}</code>\n'.format(sp.split('|||')[0], price)
        msg += '\n'

    bot.send_message(cid,
                     msg,
                     parse_mode=ParseMode.HTML)


tomorrow_h = CommandHandler('tomorrow', tomorrow_handler)

    



