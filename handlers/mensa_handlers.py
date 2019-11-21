from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from helpers import get_cid, clean_chat
from keyboards.common_keyboards import main_menu_buttons, back_button
from keyboards.mensa_keyboards import qwest_button, mensa_button
from .common_handlers import back_to_menu_handler
from phrases.mensa_phrases import mensa_menu_phrase, wait_phrase, qwest_menu_phrase
from keyboards.mensa_keyboards import days_buttons, today_buttons
from mensa_parser import parse_food
import datetime
from calendar import monthrange

WATCHING_MENU = range(1)


def gen_menu_text(food):
    message_text = ''

    for part in food:
        message_text += '<b>{}:</b>\n'.format(part)
        dishes = food.get(part)
        for dish in dishes:
            title = dish[0]
            tags = dish[1]
            price = dish[2]
            message_text += '<code>{}</code>\n<i>{} - {}</i>\n'.format(title, tags, price)
        message_text += '\n'

    return message_text


def mensa_callback(update, context):
    cid = get_cid(update)
    mids = list()
    try:
        target = context.chat_data['target']
    except KeyError:
        target = 'mensa'

    if target == 'mensa':
        options_keyboard = ReplyKeyboardMarkup([[qwest_button],
                                                [back_button]],
                                               resize_keyboard=True)
        menu_phrase = mensa_menu_phrase
    elif target == 'qwest':
        options_keyboard = ReplyKeyboardMarkup([[mensa_button],
                                                [back_button]],
                                               resize_keyboard=True)
        menu_phrase = qwest_menu_phrase
    else:
        return 404

    mids.append(context.bot.send_message(chat_id=cid,
                                         text=menu_phrase,
                                         reply_markup=options_keyboard,
                                         parse_mode=ParseMode.HTML).message_id)

    mids.append(context.bot.send_message(chat_id=cid,
                                         text=wait_phrase,
                                         parse_mode=ParseMode.HTML).message_id)

    food = parse_food(target=target)
    message_text = gen_menu_text(food)

    previous_button = InlineKeyboardButton(text=days_buttons[0],
                                           callback_data='prev')
    next_button = InlineKeyboardButton(text=days_buttons[1],
                                       callback_data='next')
    days_kb = InlineKeyboardMarkup([[previous_button, next_button]])

    context.bot.delete_message(chat_id=cid,
                               message_id=mids[-1])
    mids.pop(-1)

    mids.append(context.bot.send_message(chat_id=cid,
                                         text=message_text,
                                         reply_markup=days_kb,
                                         parse_mode=ParseMode.HTML).message_id)

    context.chat_data['message_ids'] = mids

    return WATCHING_MENU


def days_callback(update, context):
    data = update.callback_query.data
    cid = update.callback_query.from_user.id
    mids = context.chat_data['message_ids']

    try:
        target = context.chat_data['target']
    except KeyError:
        target = 'mensa'

    allowed_dates = parse_food(return_dates=True, target=target)
    today = datetime.datetime.today().date()
    if today in allowed_dates:
        previous_day = str(allowed_dates[allowed_dates.index(today) - 1])
        next_day = str(allowed_dates[allowed_dates.index(today) + 1])
    else:
        print('nothing...')
        days = monthrange(int(str(today).split('-')[0]), int(str(today).split('-')[1]))
        days = str(days).replace(' ', '').replace(')', '').replace('(', '').split(',')[1]
        today = str(today).split('-')
        day = int(today[-1])
        for i in range(1, 4):
            prev_day = day - i
            print(prev_day)
            date = datetime.date()
        return

    previous_button = InlineKeyboardButton(text=today_buttons[0],
                                           callback_data='today')
    next_button = InlineKeyboardButton(text=today_buttons[1],
                                       callback_data='today')

    if data == 'next':
        food = parse_food(date=next_day, target=target)
        days_kb = InlineKeyboardMarkup([[previous_button]])
    elif data == 'prev':
        food = parse_food(date=previous_day, target=target)
        days_kb = InlineKeyboardMarkup([[next_button]])
    else:
        food = parse_food(target=target)
        previous_button = InlineKeyboardButton(text=days_buttons[0],
                                               callback_data='prev')
        next_button = InlineKeyboardButton(text=days_buttons[1],
                                           callback_data='next')
        days_kb = InlineKeyboardMarkup([[previous_button, next_button]])

    message_text = gen_menu_text(food)

    mid = mids[-1]
    context.bot.edit_message_text(chat_id=cid,
                                  message_id=mid,
                                  text=message_text,
                                  reply_markup=days_kb,
                                  parse_mode=ParseMode.HTML)

    return WATCHING_MENU


def switch_callback(update, context):
    if update.effective_message.text == mensa_button:
        context.chat_data['target'] = 'mensa'
    elif update.effective_message.text == qwest_button:
        context.chat_data['target'] = 'qwest'

    clean_chat(update, context)
    context.chat_data['message_ids'] = list()
    mensa_callback(update, context)

    return WATCHING_MENU


days_handler = CallbackQueryHandler(pattern='^({}|{}|{})'.format('prev', 'next', 'today'),
                                    callback=days_callback)

mensa_handler = MessageHandler(filters=Filters.regex(main_menu_buttons[0]),
                               callback=mensa_callback)

switch_handler = MessageHandler(filters=Filters.regex('^({}|{})'.format(mensa_button,
                                                                        qwest_button)),
                                callback=switch_callback)

mensa_conversation = ConversationHandler(
    entry_points=[mensa_handler],
    states={

        WATCHING_MENU: [days_handler,
                        switch_handler],
    },
    fallbacks=[back_to_menu_handler]
)
