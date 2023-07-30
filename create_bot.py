from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from deep_translator import GoogleTranslator

import python_weather

from setings import TOKEN

bot = Bot(token=TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
client = python_weather.Client(unit=python_weather.METRIC)

translator = GoogleTranslator(source='auto', target='uk')
