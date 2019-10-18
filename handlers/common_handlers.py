from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
from helpers import get_cid, create_user, clean_chat
from dbmodels import User
from phrases.common_phrases import start_phrase
from keyboards.common_keyboards import main_menu_keyboard, back_button


def start_callback(update, context):
    cid = get_cid(update)

    user = User.select().where(User.uid == cid)
    if not user.exists():
        create_user(uid=cid,
                    username=update.effective_message.from_user.username)

    context.bot.send_message(
        chat_id=cid,
        text=start_phrase,
        reply_markup=main_menu_keyboard,
        parse_mode=ParseMode.HTML
    )

    return ConversationHandler.END


start_handler = CommandHandler(
    command='start',
    callback=start_callback
)


def back_to_menu_callback(update, context):
    clean_chat(update, context)

    start_callback(update, context)

    return ConversationHandler.END


back_to_menu_handler = MessageHandler(filters=Filters.regex(back_button),
                                      callback=back_to_menu_callback)