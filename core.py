# -*- coding: utf-8 -*-

from telegram.ext import Updater
from handlers import *
import logging
from secrets import bottoken

logging.basicConfig(                                                    # some logging things
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)


upd = Updater(bottoken)                                                 # creating an Updater  and dispatcher instances

dp = upd.dispatcher
jobs = upd.job_queue


if __name__ == '__main__':
    Menu.create_table()                                                 # creating tables if existing not found
    Subdata.create_table()
    Notify.create_table()

    jobs.run_daily(notifier,                                            # setting jobs for notifications about food
                   datetime.time(7, 0, 0),                              # (2 hrs ahead, cuz of time preferences on my)
                   (0, 1, 2, 3, 4))                                     # AMS server
    jobs.run_daily(notifier,
                   datetime.time(7, 30, 0),
                   (0, 1, 2, 3, 4))
    jobs.run_daily(notifier,
                   datetime.time(8, 0, 0),
                   (0, 1, 2, 3, 4))
    jobs.run_daily(notifier,
                   datetime.time(8, 30, 0),
                   (0, 1, 2, 3, 4))
    jobs.run_daily(notifier,
                   datetime.time(9, 0, 0),
                   (0, 1, 2, 3, 4))
    jobs.run_daily(notifier,
                   datetime.time(9, 30, 0),
                   (0, 1, 2, 3, 4))
    jobs.run_daily(notifier,
                   datetime.time(10, 0, 0),
                   (0, 1, 2, 3, 4))

    dp.add_error_handler(error)                                         # adding some handlers to Dispatcher
    dp.add_handler(start_h)
    dp.add_handler(help_h)
    dp.add_handler(mensa_h)
    dp.add_handler(tomorrow_h)
    dp.add_handler(times_h)
    dp.add_handler(explain_h)
    dp.add_handler(map_h)
    dp.add_handler(fristenw_h)
    dp.add_handler(fristens_h)
    dp.add_handler(source_h)
    dp.add_handler(notify_h)
    dp.add_handler(time_h)
    dp.add_handler(unsub_h)

    upd.start_polling()                                                 # starting to ask Telegram server for updates



