from telegram.ext import Updater
from handlers import *
import logging
from decouple import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.getLevelName(config('LOG_LEVEL', default='DEBUG')))

bot_token = config('BOT_TOKEN', default='token')

upd = Updater(bot_token,
              use_context=True)
dp = upd.dispatcher
jobs = upd.job_queue


if __name__ == '__main__':
    Menu.create_table()

    dp.add_handler(mensa_handler)

    upd.start_polling()
