from telegram.ext import Updater
from handlers.common_handlers import start_handler, back_to_menu_handler
from handlers.map_handlers import map_conversation
from handlers.schedule_handlers import schedule_conversation
from handlers.notifications_handlers import notifications_conversation
from handlers.help_handlers import help_conversation
from handlers.mensa_handlers import mensa_conversation
import logging
from dbmodels import check_tables
from decouple import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.getLevelName(config('LOG_LEVEL', default='INFO')))

bot_token = config('BOT_TOKEN', default='token')

upd = Updater(bot_token,
              use_context=True)
dp = upd.dispatcher
jobs = upd.job_queue


if __name__ == '__main__':
    check_tables()

    dp.add_handler(start_handler)
    dp.add_handler(map_conversation)
    dp.add_handler(schedule_conversation)
    dp.add_handler(notifications_conversation)
    dp.add_handler(help_conversation)
    dp.add_handler(mensa_conversation)
    dp.add_handler(back_to_menu_handler)

    upd.start_polling()
