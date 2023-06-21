from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from setings import TOKEN
import python_weather
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from date import Date


bot = Bot(token=TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
client = python_weather.Client(unit=python_weather.IMPERIAL)

date = Date()
