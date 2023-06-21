from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from create_bot import date

# btnStart
# btnStart = KeyboardButton('/start')
# mainStart = ReplyKeyboardMarkup(resize_keyboard=True).add(btnStart)

btnMain = KeyboardButton('⬅️ Main menu')

# ----Main_menu----
btnTemperature = KeyboardButton('🌡️ Temperature')
btnMoonPhase = KeyboardButton('🌗 Moon_phase')
btnHourlyForecast = KeyboardButton('🕗 Hourly_forecasts')
btnDailyForecast = KeyboardButton('📅 Daily_forecasts')
btnClosing = KeyboardButton('🏙️ Another city')

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnTemperature, btnHourlyForecast).add(btnMoonPhase, btnDailyForecast).add(btnClosing)

# ----Hourly_forecasts menu----
btn_first_day = KeyboardButton(f'📅 {date.today()}')
btn_second_day = KeyboardButton(f'📅 {date.tomorrow()}')
btn_third_day = KeyboardButton(f'📅 {date.day_after_tomorrow()}')

hourlyForecastsMenu = ReplyKeyboardMarkup(resize_keyboard=True)
hourlyForecastsMenu.add(btn_first_day, btn_second_day, btn_third_day).add(btnMain)
