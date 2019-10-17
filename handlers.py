# -*- coding: utf-8 -*-

import logging
from telegram.ext import run_async, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup,\
    ReplyKeyboardRemove, ParseMode
import datetime
from dbmodels import *
from helpers import get_mensa
import json
from texts import titles, times, explanation, start_phrase, help_phrase

logger = logging.getLogger(__name__)


@run_async
def error(bot, update, err):
    logger.warning('Update "%s" caused error "%s"', update, err)


@run_async
def mensa_callback(update, context):
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
            msg += '\n'
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
    context.bot.send_message(
        cid,
        msg,
        parse_mode=ParseMode.HTML
    )


mensa_handler = CommandHandler(command='mensa',
                               callback=mensa_callback)





@run_async
def times_handler(bot, update):
    cid = update.effective_message.chat.id
    bot.send_message(
        cid,
        times,
        parse_mode=ParseMode.HTML
    )


times_h = CommandHandler('times', times_handler)


@run_async
def explain_handler(bot, update):
    cid = update.effective_message.chat.id
    bot.send_message(
        cid,
        explanation,
        parse_mode=ParseMode.HTML
    )


explain_h = CommandHandler('explain', explain_handler)


@run_async
def start_handler(bot, update):
    cid = update.effective_message.chat.id
    bot.send_message(
        cid,
        start_phrase,
        parse_mode=ParseMode.HTML
    )


start_h = CommandHandler('start', start_handler)


@run_async
def help_handler(bot, update):
    cid = update.effective_message.chat.id
    bot.send_message(
        cid,
        help_phrase,
        parse_mode=ParseMode.HTML
    )


help_h = CommandHandler('help', help_handler)


@run_async
def map_handler(bot, update):
    cid = update.effective_message.chat.id
    mp = Subdata.select().where(Subdata.name == 'map')

    if mp.exists():
        mp = Subdata.get(Subdata.name == 'map')
        fid = mp.fid
        bot.send_photo(
            cid,
            fid,
            caption='By @RuhrUniBot'
        )
    else:
        m = bot.send_photo(
            cid,
            'https://www.ruhr-uni-bochum.de/anreise/images/RUB-Lageplan_en-1200.jpg',
            caption='By @RuhrUniBot'
        )
        fid = m.photo[-1].file_id
        Subdata.create(
             name='map',
             fid=fid
        )


map_h = CommandHandler('map', map_handler)


@run_async
def fristenw_handler(bot, update):
    cid = update.effective_message.chat.id
    msg = '<b>Fristen for Wintersemester</b>'
    fristen_w = Subdata.select().where(Subdata.name == 'fristen_w')
    if fristen_w.exists():
        fristen_w = Subdata.get(Subdata.name == 'fristen_w')
        bot.send_document(
            cid,
            fristen_w.fid,
            caption=msg,
            parse_mode=ParseMode.HTML
        )
    else:
        m = bot.send_document(
            cid,
            'https://www.ruhr-uni-bochum.de/imperia/md/content/dezergba/studierendensekretariat/fristen_2017_2.pdf',
            caption=msg,
            parse_mode=ParseMode.HTML
        )
        fid = m.document.file_id
        Subdata.create(
            name='fristen_w',
            fid=fid
        )


fristenw_h = CommandHandler('fristen_w', fristenw_handler)


@run_async
def fristens_handler(bot, update):
    cid = update.effective_message.chat.id
    msg = '<b>Fristen for Sommersemester</b>'
    fristen_s = Subdata.select().where(Subdata.name == 'fristen_s')

    if fristen_s.exists():
        fristen_s = Subdata.get(Subdata.name == 'fristen_s')
        bot.send_document(
            cid,
            fristen_s.fid,
            caption=msg,
            parse_mode=ParseMode.HTML
        )
    else:
        m = bot.send_document(
            cid,
            'https://www.ruhr-uni-bochum.de/imperia/md/content/dezergba/studierendensekretariat/fristen20181.pdf',
            caption=msg,
            parse_mode=ParseMode.HTML
        )
        fid = m.document.file_id
        Subdata.create(
            name='fristen_s',
            fid=fid
        )


fristens_h = CommandHandler('fristen_s', fristens_handler)


@run_async
def tomorrow_handler(bot, update):
    cid = update.effective_message.chat.id
    weekday = datetime.datetime.today().weekday()
    if weekday >= 5:
        bot.send_message(
            cid,
            '<code>Hey there!</code>\nTheres no food for tomorrow :(',
            parse_mode=ParseMode.HTML
        )
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

    bot.send_message(
        cid,
        msg,
        parse_mode=ParseMode.HTML
    )


tomorrow_h = CommandHandler('tomorrow', tomorrow_handler)


@run_async
def source_handler(bot, update):
    cid = update.effective_message.chat.id
    button = InlineKeyboardButton('GitHub', url='https://github.com/l0rem/RuhrUniBot')
    markup = InlineKeyboardMarkup([[button]])
    bot.send_message(
        cid,
        '''This bot was written by @Lor3m in <code>Python3</code> with <code>python-telegram-bot</code>.
You can find source code on GitHub.''',
        parse_mode=ParseMode.HTML,
        reply_markup=markup
    )


source_h = CommandHandler('source', source_handler)


@run_async
def notify_handler(bot, update):
    cid = update.effective_message.chat.id
    if cid < 0:
        bot.send_message(
            cid,
            '<b>Sorry, but You cant use this command in groups atm.</b>\n'
            'Stay tuned.',
            parse_mode=ParseMode.HTML
        )
        return
    else:
        button0 = KeyboardButton('\U000020639:00')
        button1 = KeyboardButton('\U000020639:30')
        button2 = KeyboardButton('\U0000206310:00')
        button3 = KeyboardButton('\U0000206310:30')
        button4 = KeyboardButton('\U0000206311:00')
        button5 = KeyboardButton('\U0000206311:30')
        button6 = KeyboardButton('\U0000206312:00')

        kb = ReplyKeyboardMarkup([[button0, button1],
                                  [button2, button3],
                                  [button4, button5],
                                  [button6]],
                                 resize_keyboard=True,
                                 one_time_keyboard=True)
        bot.send_message(
            cid,
            '<b>When would You like to receive notifications about todays menu?</b>\n\n'
            'Note, that Tagessuppe and Tipp des Tagges appear at about 10:30 - 10:40 a.m.',
            parse_mode=ParseMode.HTML,
            reply_markup=kb
        )


notify_h = CommandHandler('notify', notify_handler)


@run_async
def time_handler(bot, update):
    cid = update.effective_message.chat.id
    inbase = Notify.select().where(Notify.cid == cid)
    if inbase.exists():
        inbase = Notify.get(Notify.cid == cid)
        Notify.delete_by_id(inbase.id)

    Notify.create(
        cid=cid,
        time=update.effective_message.text,
        res='-'
    )
    bot.send_message(
        cid,
        '<b>Okay!</b>\n\nIm going to notify You about menu in Mensa every day at {} a.m.\n'
        'You can use /unsubscribe to stop receiving notifications.'.format(update.effective_message.text),
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardRemove()
    )


time_h = MessageHandler(filters=Filters.regex('^({}|{}|{}|{}|{}|{}|{})'.format('\U000020639:00',
                                                                               '\U000020639:30',
                                                                               '\U0000206310:00',
                                                                               '\U0000206310:30',
                                                                               '\U0000206311:00',
                                                                               '\U0000206311:30',
                                                                               '\U0000206312:00')),
                        callback=time_handler)


@run_async
def unsub_handler(bot, update):
    cid = update.effective_message.chat.id
    inbase = Notify.select().where(Notify.cid == cid)
    if inbase.exists():
        inbase = Notify.get(Notify.cid == cid)
        Notify.delete_by_id(inbase.id)
        bot.send_message(
            cid,
            '<b>You will not be notified about menu in Mensa anymore.</b>\n\n'
            'Note, that You can always set new notification using /notify',
            parse_mode=ParseMode.HTML
        )
    else:
        bot.send_message(
            cid,
            '<b>Sorry, but it seems like You have no active notifications.</b>\n\n'
            'Did You set up one?',
            parse_mode=ParseMode.HTML
        )


unsub_h = CommandHandler('unsubscribe', unsub_handler)


@run_async
def notifier(bot, job):
    time = str(datetime.datetime.now()).split(' ')[1].split(':')
    hour = str(int(time[0]) + 2)
    minute = time[1]
    time = hour + ':' + minute
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

    for chat in Notify.select().where(Notify.time == time):
        bot.send_message(
            chat.cid,
            '<code>Good morning!</code>',
            parse_mode=ParseMode.HTML
        )
        bot.send_message(
            chat.cid,
            msg,
            parse_mode=ParseMode.HTML
        )


    



