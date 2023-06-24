from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import date

btn_main = InlineKeyboardButton(text='⬅️ Main menu', callback_data='⬅️ Main menu')

# ----Inline buttons----
btn_temperature = InlineKeyboardButton(text='🌡️ Temperature', callback_data='🌡️ Temperature')
btn_moon_phase = InlineKeyboardButton(text='🌗 Moon phase', callback_data='🌗 Moon phase')
btn_visibility = InlineKeyboardButton(text='👁️👁️ Visibility', callback_data='👁️👁️ Visibility')
btn_wind_speed = InlineKeyboardButton(text='💨 Wind speed', callback_data='💨 Wind speed')
btn_hourly_forecast = InlineKeyboardButton(text='🕗 Hourly forecasts', callback_data='🕗 Hourly forecasts')
btn_daily_forecast = InlineKeyboardButton(text='📅 Daily forecasts', callback_data='📅 Daily forecasts')
btn_ultraviolet = InlineKeyboardButton(text='☀️ Ultraviolet', callback_data='☀️ Ultraviolet')
btn_sun_rise_set = InlineKeyboardButton(text='🌇 Sunrise, sunset', callback_data='🌇 Sunrise, sunset')
btn_changing_city = InlineKeyboardButton(text='🏙️ Another city', callback_data='🏙️ Another city')

action_catalog = InlineKeyboardMarkup(row_width=2)
action_catalog.add(btn_temperature, btn_moon_phase, btn_visibility, btn_wind_speed)
action_catalog.add(btn_sun_rise_set, btn_ultraviolet, btn_hourly_forecast, btn_daily_forecast)
action_catalog.add(btn_changing_city)

# ----Hourly_forecasts menu----
btn_first_day = InlineKeyboardButton(text=date.today(), callback_data=date.today())
btn_second_day = InlineKeyboardButton(text=date.tomorrow(), callback_data=date.tomorrow())
btn_third_day = InlineKeyboardButton(text=date.day_after_tomorrow(), callback_data=date.day_after_tomorrow())

hourly_forecasts_catalog = InlineKeyboardMarkup(row_width=3)
hourly_forecasts_catalog.add(btn_first_day, btn_second_day, btn_third_day).add(btn_main)

# ----Reply buttons----
# btnChanging = KeyboardButton('🏙️ Another city')
#
# mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
# mainMenu.add(btnChanging)
