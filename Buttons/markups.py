from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import date

# btnStart
# btnStart = KeyboardButton('/start')
# mainStart = ReplyKeyboardMarkup(resize_keyboard=True).add(btnStart)

btnMain = InlineKeyboardButton(text='⬅️ Main menu', callback_data='⬅️ Main menu')

# ----Inline buttons----
btnTemperature = InlineKeyboardButton(text='🌡️ Temperature', callback_data='🌡️ Temperature')
btnMoonPhase = InlineKeyboardButton(text='🌗 Moon phase', callback_data='🌗 Moon phase')
btnHourlyForecast = InlineKeyboardButton(text='🕗 Hourly forecasts', callback_data='🕗 Hourly forecasts')
btnDailyForecast = InlineKeyboardButton(text='📅 Daily forecasts', callback_data='📅 Daily forecasts')

action_catalog = InlineKeyboardMarkup(row_width=2)
action_catalog.add(btnTemperature, btnMoonPhase, btnHourlyForecast, btnDailyForecast)

# ----Main_menu----
# btnChanging = KeyboardButton('🏙️ Another city')
#
# mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
# mainMenu.add(btnChanging)

# ----Hourly_forecasts menu----
btn_first_day = InlineKeyboardButton(text=date.today(), callback_data=date.today())
btn_second_day = InlineKeyboardButton(text=date.tomorrow(), callback_data=date.tomorrow())
btn_third_day = InlineKeyboardButton(text=date.day_after_tomorrow(), callback_data=date.day_after_tomorrow())

hourlyForecastsCatalog = InlineKeyboardMarkup(row_width=3)
hourlyForecastsCatalog.add(btn_first_day, btn_second_day, btn_third_day).add(btnMain)
