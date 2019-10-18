from telegram.ext import run_async, ConversationHandler, MessageHandler, Filters
from telegram import ParseMode
from helpers import get_cid
from keyboards.common_keyboards import back_keyboard, main_menu_buttons
from .common_handlers import back_to_menu_handler
from phrases.mensa_phrases import mensa_menu_phrase

WATCHING_MENU = range(1)


@run_async
def mensa_callback(update, context):
    cid = get_cid(update)
    mids = list()

    mids.append(context.bot.send_message(chat_id=cid,
                                         text=mensa_menu_phrase,
                                         reply_markup=back_keyboard,
                                         parse_mode=ParseMode.HTML).message_id)

    context.chat_data['message_ids'] = mids

    return WATCHING_MENU


mensa_handler = MessageHandler(filters=Filters.regex(main_menu_buttons[0]),
                               callback=mensa_callback)

mensa_conversation = ConversationHandler(
    entry_points=[mensa_handler],
    states={

        WATCHING_MENU: []
    },
    fallbacks=[back_to_menu_handler]
)
