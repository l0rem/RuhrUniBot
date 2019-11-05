from telegram.ext import ConversationHandler, MessageHandler, Filters
from telegram import ParseMode
from helpers import get_cid
from keyboards.common_keyboards import back_keyboard, main_menu_buttons
from .common_handlers import back_to_menu_handler

N = range(1)


def not_implemented_callback(update, context):
    cid = get_cid(update)
    mids = list()

    text = '<code>Not implemented yet!</code>\nStay tuned and come back later.'
    mids.append(context.bot.send_message(chat_id=cid,
                                         text=text,
                                         reply_markup=back_keyboard,
                                         parse_mode=ParseMode.HTML).message_id)

    context.chat_data['message_ids'] = mids

    return N


not_implemented_handler = MessageHandler(filters=Filters.regex(main_menu_buttons[2]),
                                         callback=not_implemented_callback)


notifications_conversation = ConversationHandler(
    entry_points=[not_implemented_handler],
    states={

        N: []
    },
    fallbacks=[back_to_menu_handler]
)