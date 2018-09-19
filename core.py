# -*- coding: utf-8 -*-


from telegram.ext import Updater
from secrets import *
from handlers import *
import logging
from telethon import TelegramClient, sync, events
import asyncio
import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

api_id = 00000
api_hash = 'HASH'

client = TelegramClient('warden', api_id, api_hash)

upd = Updater(bottoken)
dp = upd.dispatcher
jobs = upd.job_queue


@client.on(events.NewMessage(outgoing=True))
async def handler(event):
    message = event.message
    if message.message == '':
        return
    prefix = message.message.split(' ')[0]
    f_text = message.message[len(prefix):]
    if prefix[0] == '/' and prefix[1:].isdigit():
        spaces = 0
        for let in f_text:
            if let == ' ':
                spaces += 1
        times = (len(f_text) + spaces) * int(message.message.split(' ')[0][1:])

        await message.edit(f_text)
    else:
        return
    for i in range(times):
        if f_text[0] == ' ':
            f_text = f_text[2:] + f_text[:2]
        else:
            f_text = f_text[1:] + f_text[0]
        await message.edit(f_text)
        await asyncio.sleep(0.3)
    await message.edit(message.message[len(prefix):])


if __name__ == '__main__':
    jobs.run_daily(menser, time=datetime.time(8, 30, 0))
    jobs.run_daily(tomorrower, time=datetime.time(18, 0, 0))
    dp.add_error_handler(error)
    dp.add_handler(start_h)
    dp.add_handler(help_h)
    dp.add_handler(mensa_h)
    dp.add_handler(tomorrow_h)
    dp.add_handler(times_h)
    dp.add_handler(voronezh_h)
    dp.add_handler(explain_h)
    dp.add_handler(map_h)
    dp.add_handler(fristenw_h)
    dp.add_handler(fristens_h)
    dp.add_handler(test_h)
    upd.start_polling()
    client.start()
    client.run_until_disconnected()

