from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from .others import data_forecast

from Buttons import markups

from create_bot import client, translator

from date import today, tomorrow, day_after_tomorrow

from image_converter import ImageConverter


class Form(StatesGroup):
    language = State()  # Will be represented in storage as 'Form:language'
    city = State()  # Will be represented in storage as 'Form:city'


async def command_start(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        pass
    else:
        await state.finish()

    await Form.language.set()
    # username = message.from_user.first_name
    resp_message = "Please choose the language of communication 🇬🇧.\nБудь ласка, оберіть мову спілкування 🇺🇦."
    await message.answer(resp_message, reply_markup=markups.lang_buttons)


async def command_help(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        language = data['language']
        if language == "🇬🇧 English":
            await message.answer("I can tell you about the weather in all cities, "
                                 "write commands\n/start or /weather to start interacting with the bot.")
        else:
            await message.answer("Я можу розповісти про погоду в усіх містах, "
                                 "напишіть команди\n/start або /weather щоб почати взаємодіяти з ботом.")


async def process_language(message: types.Message, state: FSMContext):
    language = message.text
    async with state.proxy() as data:
        data['language'] = language

    if language == "🇬🇧 English":
        await Form.next()
        await message.answer("Please enter the name of the city you need.")
    elif language == "🇺🇦 Українська":
        await Form.next()
        await message.answer("Будь ласка, введіть назву потрібного вам міста.")
    else:
        await message.answer("Please click on button to choose the language.\n"
                             "Будь ласка, натисніть на кнопку, щоб обрати мову спілкування.")


async def process_city(message: types.Message, state: FSMContext):
    city = message.text
    async with state.proxy() as data:
        data['city'] = city
        if data['language'] == "🇬🇧 English":
            resp_message = "Please choose information what you need about this city:"
            await message.answer(resp_message, reply_markup=markups.action_catalog)
        else:
            resp_message = "Будь ласка, оберіть що ви хочете дізнатись про це місто:"
            await message.answer(resp_message, reply_markup=markups.action_catalog_ua)


async def return_to_main_menu(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data['language'] == "🇬🇧 English":
            resp_message = "Please choose information what you need about this city:"
            await call.message.edit_text(text=resp_message, reply_markup=markups.action_catalog)
        else:
            resp_message = "Будь ласка, оберіть що ви хочете дізнатись про це місто:"
            await call.message.edit_text(text=resp_message, reply_markup=markups.action_catalog_ua)


async def process_closing(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data['language'] == "🇬🇧 English":
            resp_message = "Please enter the city you need."
        else:
            resp_message = "Будь ласка, введіть місто яке вам потрібно."
    await Form.city.set()
    await call.message.answer(resp_message)


async def process_temperature(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        weather = await client.get(data['city'])

        celsius = weather.current.temperature
        translation_kind = translator.translate(weather.current.kind.__str__())
        translation_area = translator.translate(f"{weather.nearest_area.name}; {weather.nearest_area.country}")

        if data['language'] == "🇬🇧 English":
            resp_msg = f"{weather.nearest_area.name}; {weather.nearest_area.country}\n\n"
            resp_msg += f"Current temperature: {celsius}°C\n"
            resp_msg += f"Feels like: {weather.current.feels_like}°C\n"
            resp_msg += f"State of the weather: {weather.current.kind}\n\n"
            if celsius <= 10:
                resp_msg += "Cool! Dress warmer!"
            else:
                resp_msg += "Warmth! Dress easier!"
        else:
            resp_msg = f"{translation_area}\n\n"
            resp_msg += f"Температура зараз: {celsius}°C\n"
            resp_msg += f"Відчувається, як: {weather.current.feels_like}°C\n"
            resp_msg += f"Стан погоди: {translation_kind}\n\n"
            if celsius <= 10:
                resp_msg += "Прохолодно! Одягайся тепліше!"
            else:
                resp_msg += "Тепло! Одягайся легше!"

        await call.message.answer(resp_msg)


async def process_wind_speed(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        weather = await client.get(data['city'])
        wind_speed = weather.current.wind_speed

        if data['language'] == "🇬🇧 English":
            resp_msg = f"Wind speed: {wind_speed} km/h"
        else:
            resp_msg = f"Швидкість вітру: {wind_speed} км/год"

        if wind_speed >= 39:
            photo = open('Images/strong_wind.jpg', 'rb')
            if data['language'] == "🇬🇧 English":
                resp_msg += ", Strong wind"
            else:
                resp_msg += ", Сильний вітер"
        else:
            photo = open('Images/wind.jpg', 'rb')
            if data['language'] == "🇬🇧 English":
                resp_msg += ", Light wind"
            else:
                resp_msg += ", Легкий вітер"

        await call.message.answer_photo(photo, caption=resp_msg)


async def process_visibility(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        weather = await client.get(data['city'])
        visibility = weather.current.visibility

        if data['language'] == "🇬🇧 English":
            resp_msg = f"Visibility: {visibility} km"
        else:
            resp_msg = f"Видимість: {visibility} км"

        if visibility <= 2:
            photo = open('Images/bad_visibility.jpg', 'rb')
            if data['language'] == "🇬🇧 English":
                resp_msg += ", Bad visibility"
            else:
                resp_msg += ", Погана видимість"
        else:
            photo = open('Images/good_visibility.jpg', 'rb')
            if data['language'] == "🇬🇧 English":
                resp_msg += ", Good visibility"
            else:
                resp_msg += ", Хороша видимість"

        await call.message.answer_photo(photo, caption=resp_msg)


async def process_humidity(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        weather = await client.get(data['city'])
        humidity = weather.current.humidity

        if data['language'] == "🇬🇧 English":
            resp_msg = f"Current percentage of humidity: {humidity}%"
        else:
            resp_msg = f"Поточний відсоток вологості: {humidity}%"

        if humidity > 70:
            photo = open('Images/high_humidity.jpg', 'rb')
        elif humidity < 40:
            photo = open('Images/low_humidity.jpg', 'rb')
        else:
            photo = open('Images/norm_humidity.jpg', 'rb')

        await call.message.answer_photo(photo, caption=resp_msg)


async def process_sun_rise_set(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        weather = await client.get(data['city'])

        if data['language'] == "🇬🇧 English":
            resp_msg = "Three day of sun information.\n\n"
            for forecast in weather.forecasts:
                resp_msg += f"Date: {forecast.date}\n"
                resp_msg += f"Sun rise: {forecast.astronomy.sun_rise}\n"
                resp_msg += f"Sun set: {forecast.astronomy.sun_set}\n\n"
        else:
            resp_msg = "Триденна інформація про сонце.\n\n"
            for forecast in weather.forecasts:
                resp_msg += f"Дата: {forecast.date}\n"
                resp_msg += f"Схід сонця: {forecast.astronomy.sun_rise}\n"
                resp_msg += f"Захід сонця: {forecast.astronomy.sun_set}\n\n"

        await call.message.answer(resp_msg)


async def process_moon_phase(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        weather = await client.get(data['city'])

        if data['language'] == "🇬🇧 English":
            resp_msg = "Three-day moon phase forecast.\n\n"
            for forecast in weather.forecasts:
                resp_msg += f"Date: {forecast.date}\n"
                resp_msg += f"Moon phase: {forecast.astronomy.moon_phase}\n"
                resp_msg += f"Moon illumination - {forecast.astronomy.moon_illumination}%\n\n"
        else:
            resp_msg = "Прогноз фази місяця на три дні.\n\n"
            for forecast in weather.forecasts:
                translation = translator.translate(forecast.astronomy.moon_phase.__str__())
                resp_msg += f"Дата: {forecast.date}\n"
                resp_msg += f"Фаза місяця: {translation}\n"
                resp_msg += f"Місячне освітлення - {forecast.astronomy.moon_illumination}%\n\n"

        await call.message.answer(resp_msg)


async def process_hourly_forecasts(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data['language'] == "🇬🇧 English":
            await call.message.edit_text(text="Please choose day of the hourly forecast:",
                                         reply_markup=markups.hourly_forecasts_catalog)
        else:
            await call.message.edit_text(text="Оберіть день погодинного прогнозу:",
                                         reply_markup=markups.hourly_forecasts_catalog_ua)


async def hourly_forecasts_today(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        city = data['city']
        language = data['language']
        weather = await client.get(city)
        forecast_data = data_forecast(weather, 0)

        image_converter = ImageConverter(language, forecast_data['time'], forecast_data['temperature'],
                                         forecast_data['description'], forecast_data['kind'])
        image_converter.forecast("today")

    photo = open('Forecasts/Today_forecast.png', 'rb')
    t_lowest = min(forecast_data['temperature'])
    t_highest = max(forecast_data['temperature'])

    if language == "🇬🇧 English":
        message = f"{city}, Temperature will be from {t_lowest} to {t_highest}°C"
    else:
        message = f"{city}, Температура буде від {t_lowest} до {t_highest}°C"

    await call.message.answer_photo(photo, caption=message)


async def hourly_forecasts_tomorrow(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        city = data['city']
        language = data['language']
        weather = await client.get(city)
        forecast_data = data_forecast(weather, 1)

        image_converter = ImageConverter(language, forecast_data['time'], forecast_data['temperature'],
                                         forecast_data['description'], forecast_data['kind'])
        image_converter.forecast("tomorrow")

    photo = open('Forecasts/Tomorrow_forecast.png', 'rb')
    t_lowest = min(forecast_data['temperature'])
    t_highest = max(forecast_data['temperature'])

    if language == "🇬🇧 English":
        message = f"{city}, Temperature will be from {t_lowest} to {t_highest}°C"
    else:
        message = f"{city}, Температура буде від {t_lowest} до {t_highest}°C"

    await call.message.answer_photo(photo, caption=message)


async def hourly_forecasts_day_after_tomorrow(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        city = data['city']
        language = data['language']
        weather = await client.get(city)
        forecast_data = data_forecast(weather, 2)

        image_converter = ImageConverter(language, forecast_data['time'], forecast_data['temperature'],
                                         forecast_data['description'], forecast_data['kind'])
        image_converter.forecast("day after tomorrow")

    photo = open('Forecasts/Day_After_Tomorrow_forecast.png', 'rb')
    t_lowest = min(forecast_data['temperature'])
    t_highest = max(forecast_data['temperature'])

    if language == "🇬🇧 English":
        message = f"{city}, Temperature will be from {t_lowest} to {t_highest}°C"
    else:
        message = f"{city}, Температура буде від {t_lowest} до {t_highest}°C"

    await call.message.answer_photo(photo, caption=message)


async def process_daily_forecasts(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        weather = await client.get(data['city'])
        language = data['language']
        if language == "🇬🇧 English":
            resp_msg = "Three-day temperature forecast.\n\n"
        else:
            resp_msg = "Прогноз температури на три дні.\n\n"

        for forecast in weather.forecasts:
            day = forecast.date
            t_lowest = forecast.lowest_temperature
            t_highest = forecast.highest_temperature

            if language == "🇬🇧 English":
                descriptions = ", ".join(set(h.description for h in forecast.hourly))
                resp_msg += f"Date: {day}\n"
                resp_msg += f"Temperature will be from {t_lowest} to {t_highest}°C\n"
                resp_msg += f"Description: {descriptions}\n\n"
            else:
                translation = ", ".join(set(translator.translate(h.description) for h in forecast.hourly))
                resp_msg += f"Дата: {day}\n"
                resp_msg += f"Температура буде від {t_lowest} до {t_highest}°C\n"
                resp_msg += f"Опис погоди: {translation}\n\n"

        await call.message.answer(resp_msg)


def register_handlers_client(dp: Dispatcher):
    # ----Commands----
    dp.register_message_handler(command_start, commands=["start", "weather", "language"], state='*')
    dp.register_message_handler(command_help, commands="help", state='*')
    # ----Set a language----
    dp.register_message_handler(process_language, text=["🇬🇧 English", "🇺🇦 Українська"], state=Form.language)
    # ----Set a city----
    dp.register_message_handler(process_city, state=Form.city)
    # ----Inline buttons----
    dp.register_callback_query_handler(return_to_main_menu, text=["⬅️ Main menu", '⬅️ Головне меню'], state=Form.city)
    dp.register_callback_query_handler(process_temperature, text=['🌡️ Temperature', '🌡️ Температура'], state=Form.city)
    dp.register_callback_query_handler(process_moon_phase, text=['🌗 Moon phase', '🌗 Фаза місяця'], state=Form.city)
    dp.register_callback_query_handler(process_visibility, text=['👁️👁️ Visibility', '👁️👁️ Видимість'], state=Form.city)
    dp.register_callback_query_handler(process_wind_speed, text=['💨 Wind speed', '💨 Швидкість вітру'], state=Form.city)
    dp.register_callback_query_handler(process_hourly_forecasts, text=['🕗 Hourly forecasts', '🕗 Погод. прогноз'], state=Form.city)
    dp.register_callback_query_handler(process_daily_forecasts, text=['📅 Daily forecasts', '📅 Щоден. прогноз'], state=Form.city)
    dp.register_callback_query_handler(process_humidity, text=['💧 Humidity', '💧 Вологість'], state=Form.city)
    dp.register_callback_query_handler(process_sun_rise_set, text=['🌇 Sunrise, sunset', '🌇 Схід, Захід'], state=Form.city)
    dp.register_callback_query_handler(process_closing, text=['🏙️ Another city', '🏙️ Інше місто'], state=Form.city)
    dp.register_callback_query_handler(hourly_forecasts_today, text=[f'{today()}'], state=Form.city)
    dp.register_callback_query_handler(hourly_forecasts_tomorrow, text=[f'{tomorrow()}'], state=Form.city)
    dp.register_callback_query_handler(hourly_forecasts_day_after_tomorrow, text=[f'{day_after_tomorrow()}'], state=Form.city)
