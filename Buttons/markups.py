from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# btnStart
# btnStart = KeyboardButton('/start')
# mainStart = ReplyKeyboardMarkup(resize_keyboard=True).add(btnStart)

# btnMain = KeyboardButton('Main menu')

# ----Main_menu----
btnTemperature = KeyboardButton('/Temperature 🌡️')
btnMoonPhase = KeyboardButton('/Moon_phase 🌗')
btnHourlyForecast = KeyboardButton('/Hourly_forecasts 🕗')
btnDailyForecast = KeyboardButton('/Daily_forecasts 📅')
# btnOther = KeyboardButton('Other')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(btnTemperature, btnHourlyForecast).add(btnMoonPhase, btnDailyForecast)

# ----Other menu----
# btnInfo = KeyboardButton('Information')
# otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo, btnMain)
