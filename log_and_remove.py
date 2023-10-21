#!/usr/bin/env python3
# 2023-08-20 by apie
# Log and remove messages sent to the bot. Useful for tracking habits. The bot saves the message + time in a db.
import time
import logging
from io import StringIO
from aiogram import Bot, Dispatcher, executor, types
from tinydb import TinyDB
from settings import API_TOKEN
from list_e import list_entries

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("""Hi
    I will log and remove your message.
    """)

@dp.message_handler(commands=['last'])
async def show_last_entries(message: types.Message):
    username = message['from']['username']
    with StringIO() as f:
        list_entries(username, 10, f)
        entries = f.getvalue() or 'niets'
    rep = await message.reply(entries)
    time.sleep(10)
    await rep.delete()
    await message.delete()

@dp.message_handler()
async def log(message: types.Message):
    username = message['from']['username']
    print(f"[{message.date}] {username}: {message.text}")
    db = TinyDB('db.json')
    table = db.table(username)
    table.insert({'date': message.date.timestamp(), 'text': message.text})
    await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

