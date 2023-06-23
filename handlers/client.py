from aiogram import types, Dispatcher
from Buttons import markups
from create_bot import client
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import date
from image_converter import ImageConverter


class Form(StatesGroup):
    city = State()  # Will be represented in storage as 'Form:city'


async def command_start(message: types.Message, state: FSMContext):
    await state.finish()
    await Form.city.set()
    await message.answer(f'Hello, {message.from_user.first_name}.\nPlease enter the city you need.')


async def command_help(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("I can tell you about the weather in all cities, "
                         "write commands\n/start or /weather to enter the city.")


async def process_city(message: types.Message, state: FSMContext):
    weather = message.text
    async with state.proxy() as data:
        data['city'] = weather

    await message.answer('Please choose information what you need about this city:',
                         reply_markup=markups.action_catalog)


async def return_to_main_menu(call: types.CallbackQuery):
    await call.message.edit_text(text='Please choose information what you need about this city:',
                                 reply_markup=markups.action_catalog)


async def process_closing(message: types.Message, state: FSMContext):
    await state.finish()
    await Form.city.set()
    await message.answer(f'Please enter the city you need.')


async def process_temperature(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        weather = await client.get(data['city'])

        celsius = weather.current.temperature

        resp_msg = f'{weather.nearest_area.name}; {weather.nearest_area.country}\n\n'
        resp_msg += f'Current temperature: {celsius}°C\n'
        resp_msg += f'Feels like: {weather.current.feels_like}°C\n'
        resp_msg += f'State of the weather: {weather.current.kind}\n'

        if celsius <= 10:
            resp_msg += '\n\nCool! Dress warmer!'
        else:
            resp_msg += '\n\nWarmth! Dress easier!'

        await call.message.answer(resp_msg)


async def process_wind_speed(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        weather = await client.get(data['city'])
        wind_speed = weather.current.wind_speed
        resp_msg = f"Wind speed: {wind_speed} km/h\n"

        if wind_speed >= 39:
            photo = open('Images/strong_wind.jpg', 'rb')
        else:
            photo = open('Images/wind.jpg', 'rb')

        await call.message.answer_photo(photo, caption=resp_msg)


async def process_visibility(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        weather = await client.get(data['city'])
        visibility = weather.current.visibility
        resp_msg = f"Visibility: {visibility} km"

        if visibility <= 2:
            photo = open('Images/bad_visibility.jpg', 'rb')
        else:
            photo = open('Images/good_visibility.jpg', 'rb')

        await call.message.answer_photo(photo, caption=resp_msg)


async def process_ultraviolet(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        weather = await client.get(data['city'])
        resp_msg = f'Current level of ultraviolet: {weather.current.ultraviolet}'

        await call.message.answer(resp_msg)


async def process_sun_rise_set(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        weather = await client.get(data['city'])
        resp_msg = 'Three day of sun information.\n\n'
        for forecast in weather.forecasts:
            resp_msg += f'Date: {forecast.date}\n'
            resp_msg += f'Sun rise: {forecast.astronomy.sun_rise}\n'
            resp_msg += f'Sun set: {forecast.astronomy.sun_set}\n\n'

        await call.message.answer(resp_msg)


async def process_moon_phase(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        weather = await client.get(data['city'])
        resp_msg = 'Three-day moon phase forecast.\n\n'
        for forecast in weather.forecasts:
            resp_msg += f'Forecast date: {forecast.date}\n'
            resp_msg += f'Moon phase: {forecast.astronomy.moon_phase}\n'
            resp_msg += f'Moon illumination - {forecast.astronomy.moon_illumination}%\n\n'

        await call.message.answer(resp_msg)


async def process_hourly_forecasts(call: types.CallbackQuery):
    await call.message.edit_text(text='Please choose day of the hourly forecast:',
                                 reply_markup=markups.hourlyForecastsCatalog)


async def hourly_forecasts_today(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        city = data['city']
        weather = await client.get(city)
        forecast_data = {'time': [], 'temperature': [], 'description': [], 'kind': []}
        for n, forecast in enumerate(weather.forecasts):
            if n == 0:
                for hourly in forecast.hourly:
                    forecast_data['time'].append(hourly.time.strftime("%H:%M"))
                    forecast_data['temperature'].append(round((hourly.temperature - 32) / 1.8))
                    forecast_data['description'].append(hourly.description)
                    forecast_data['kind'].append(hourly.kind)

        image_converter = ImageConverter(forecast_data['time'], forecast_data['temperature'],
                                         forecast_data['description'], forecast_data['kind'])
        image_converter.today_forecast()

    photo = open('Forecasts/Today_forecast.png', 'rb')

    await call.message.answer_photo(photo, caption=city)


async def hourly_forecasts_tomorrow(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        city = data['city']
        weather = await client.get(city)
        forecast_data = {'time': [], 'temperature': [], 'description': [], 'kind': []}
        for n, forecast in enumerate(weather.forecasts):
            if n == 0:
                for hourly in forecast.hourly:
                    forecast_data['time'].append(hourly.time.strftime("%H:%M"))
                    forecast_data['temperature'].append(round((hourly.temperature - 32) / 1.8))
                    forecast_data['description'].append(hourly.description)
                    forecast_data['kind'].append(hourly.kind)

        image_converter = ImageConverter(forecast_data['time'], forecast_data['temperature'],
                                         forecast_data['description'], forecast_data['kind'])
        image_converter.tomorrow_forecast()

    photo = open('Forecasts/Tomorrow_forecast.png', 'rb')
    await call.message.answer_photo(photo, caption=city)


async def hourly_forecasts_day_after_tomorrow(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        city = data['city']
        weather = await client.get(city)
        forecast_data = {'time': [], 'temperature': [], 'description': [], 'kind': []}
        for n, forecast in enumerate(weather.forecasts):
            if n == 0:
                for hourly in forecast.hourly:
                    forecast_data['time'].append(hourly.time.strftime("%H:%M"))
                    forecast_data['temperature'].append(round((hourly.temperature - 32) / 1.8))
                    forecast_data['description'].append(hourly.description)
                    forecast_data['kind'].append(hourly.kind)

        image_converter = ImageConverter(forecast_data['time'], forecast_data['temperature'],
                                         forecast_data['description'], forecast_data['kind'])
        image_converter.day_after_tomorrow_forecast()

    photo = open('Forecasts/Day_After_Tomorrow_forecast.png', 'rb')
    await call.message.answer_photo(photo, caption=city)


async def process_daily_forecasts(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        weather = await client.get(data['city'])
        resp_msg = 'Three-day temperature forecast.\n\n'

        for forecast in weather.forecasts:
            day = forecast.date
            t_lowest = round((forecast.lowest_temperature - 32) / 1.8)
            t_highest = round((forecast.highest_temperature - 32) / 1.8)
            descriptions = ", ".join(set(h.description for h in forecast.hourly))
            resp_msg += f'Date: {day}.' \
                        f'\nTemperature will be from {t_lowest} to {t_highest}°C\n' \
                        f'Description: {descriptions}\n\n'

        await call.message.answer(resp_msg)


def register_handlers_client(dp: Dispatcher):
    # ----Commands----
    dp.register_message_handler(command_start, commands=["start", "weather"], state='*')
    dp.register_message_handler(command_help, commands="help", state='*')
    dp.register_message_handler(process_closing, commands="change_city", state='*')
    # ----Set a city----
    dp.register_message_handler(process_city, state=Form.city)
    # ----Inline buttons----
    dp.register_callback_query_handler(return_to_main_menu, text=["⬅️ Main menu"], state=Form.city)
    dp.register_callback_query_handler(process_temperature, text=['🌡️ Temperature'], state=Form.city)
    dp.register_callback_query_handler(process_moon_phase, text=['🌗 Moon phase'], state=Form.city)
    dp.register_callback_query_handler(process_visibility, text=['👁️👁️ Visibility'], state=Form.city)
    dp.register_callback_query_handler(process_wind_speed, text=['💨 Wind speed'], state=Form.city)
    dp.register_callback_query_handler(process_hourly_forecasts, text=['🕗 Hourly forecasts'], state=Form.city)
    dp.register_callback_query_handler(process_daily_forecasts, text=['📅 Daily forecasts'], state=Form.city)
    dp.register_callback_query_handler(process_ultraviolet, text=['☀️ Ultraviolet'], state=Form.city)
    dp.register_callback_query_handler(process_sun_rise_set, text=['🌇 Sunrise, sunset'], state=Form.city)
    dp.register_callback_query_handler(hourly_forecasts_today, text=[f'{date.today()}'], state=Form.city)
    dp.register_callback_query_handler(hourly_forecasts_tomorrow, text=[f'{date.tomorrow()}'], state=Form.city)
    dp.register_callback_query_handler(hourly_forecasts_day_after_tomorrow, text=[f'{date.day_after_tomorrow()}'], state=Form.city)
