from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from create_bot import date

# ----Inline buttons (EN)----
btn_temperature = InlineKeyboardButton(text='🌡️ Temperature', callback_data='🌡️ Temperature')
btn_moon_phase = InlineKeyboardButton(text='🌗 Moon phase', callback_data='🌗 Moon phase')
btn_visibility = InlineKeyboardButton(text='👁️👁️ Visibility', callback_data='👁️👁️ Visibility')
btn_wind_speed = InlineKeyboardButton(text='💨 Wind speed', callback_data='💨 Wind speed')
btn_hourly_forecast = InlineKeyboardButton(text='🕗 Hourly forecasts', callback_data='🕗 Hourly forecasts')
btn_daily_forecast = InlineKeyboardButton(text='📅 Daily forecasts', callback_data='📅 Daily forecasts')
btn_humidity = InlineKeyboardButton(text='💧 Humidity', callback_data='💧 Humidity')
btn_sun_rise_set = InlineKeyboardButton(text='🌇 Sunrise, sunset', callback_data='🌇 Sunrise, sunset')
btn_changing_city = InlineKeyboardButton(text='🏙️ Another city', callback_data='🏙️ Another city')

action_catalog = InlineKeyboardMarkup(row_width=2)
action_catalog.add(btn_temperature, btn_humidity, btn_visibility, btn_wind_speed)
action_catalog.add(btn_sun_rise_set, btn_moon_phase, btn_hourly_forecast, btn_daily_forecast)
action_catalog.add(btn_changing_city)

# ----Hourly_forecasts menu----
btn_main = InlineKeyboardButton(text='⬅️ Main menu', callback_data='⬅️ Main menu')
btn_first_day = InlineKeyboardButton(text=date.today(), callback_data=date.today())
btn_second_day = InlineKeyboardButton(text=date.tomorrow(), callback_data=date.tomorrow())
btn_third_day = InlineKeyboardButton(text=date.day_after_tomorrow(), callback_data=date.day_after_tomorrow())

hourly_forecasts_catalog = InlineKeyboardMarkup(row_width=3)
hourly_forecasts_catalog.add(btn_first_day, btn_second_day, btn_third_day).add(btn_main)

# ----Inline buttons (UA)----
btn_temperature_ua = InlineKeyboardButton(text='🌡️ Температура', callback_data='🌡️ Температура')
btn_moon_phase_ua = InlineKeyboardButton(text='🌗 Фаза місяця', callback_data='🌗 Фаза місяця')
btn_visibility_ua = InlineKeyboardButton(text='👁️👁️ Видимість', callback_data='👁️👁️ Видимість')
btn_wind_speed_ua = InlineKeyboardButton(text='💨 Швидкість вітру', callback_data='💨 Швидкість вітру')
btn_hourly_forecast_ua = InlineKeyboardButton(text='🕗 Погод. прогноз', callback_data='🕗 Погод. прогноз')
btn_daily_forecast_ua = InlineKeyboardButton(text='📅 Щоден. прогноз', callback_data='📅 Щоден. прогноз')
btn_humidity_ua = InlineKeyboardButton(text='💧 Вологість', callback_data='💧 Вологість')
btn_sun_rise_set_ua = InlineKeyboardButton(text='🌇 Схід, Захід', callback_data='🌇 Схід, Захід')
btn_changing_city_ua = InlineKeyboardButton(text='🏙️ Інше місто', callback_data='🏙️ Інше місто')

action_catalog_ua = InlineKeyboardMarkup(row_width=2)
action_catalog_ua.add(btn_temperature_ua, btn_humidity_ua, btn_visibility_ua, btn_wind_speed_ua)
action_catalog_ua.add(btn_sun_rise_set_ua, btn_moon_phase_ua, btn_hourly_forecast_ua, btn_daily_forecast_ua)
action_catalog_ua.add(btn_changing_city_ua)

# ----Hourly_forecasts menu (UA)----
btn_main_ua = InlineKeyboardButton(text='⬅️ Головне меню', callback_data='⬅️ Головне меню')
hourly_forecasts_catalog_ua = InlineKeyboardMarkup(row_width=3)
hourly_forecasts_catalog_ua.add(btn_first_day, btn_second_day, btn_third_day).add(btn_main_ua)

# ----Reply buttons----
btn_en = KeyboardButton('🇬🇧 English')
btn_ua = KeyboardButton('🇺🇦 Українська')

lang_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
lang_buttons.add(btn_en, btn_ua)
