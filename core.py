from telegram.ext import Updater
from handlers.common_handlers import start_handler
from handlers.mensa_handlers import mensa_conversation
import logging
from dbmodels import check_tables
from decouple import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.getLevelName(config('LOG_LEVEL', default='DEBUG')))

bot_token = config('BOT_TOKEN', default='token')

upd = Updater(bot_token,
              use_context=True)
dp = upd.dispatcher
jobs = upd.job_queue


if __name__ == '__main__':
    check_tables()

    dp.add_handler(start_handler)
    dp.add_handler(mensa_conversation)

    upd.start_polling()
