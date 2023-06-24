from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import python_weather

from date import Date

from setings import TOKEN

bot = Bot(token=TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
client = python_weather.Client(unit=python_weather.METRIC)

date = Date()
