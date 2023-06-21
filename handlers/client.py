from aiogram import types, Dispatcher
from Buttons import markups
from create_bot import client
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import date
from image_converter import ImageConverter


class Form(StatesGroup):
    city = State()  # Will be represented in storage as 'Form:city'
    choice = State()


async def command_start(message: types.Message):
    # Set state
    await Form.city.set()

    await message.answer(f'Hello, {message.from_user.first_name}.\nPlease enter the city you need.')


async def process_city(message: types.Message, state: FSMContext):
    weather = message.text
    async with state.proxy() as data:
        data['city'] = weather

    await Form.next()
    await message.answer(f'Wow, cool city. Please choose what you need.', reply_markup=markups.mainMenu)


async def return_to_main_menu(message: types.Message):
    await message.answer('Main menu', reply_markup=markups.mainMenu)


async def process_temperature(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        resp_msg = ''
        weather = await client.get(data['city'])

        celsius = round((weather.current.temperature - 32) / 1.8)

        resp_msg += f'{weather.nearest_area.name}; {weather.nearest_area.country}\n'
        resp_msg += f'Current temperature: {celsius}°C\n'
        resp_msg += f'State of the weather: {weather.current.kind}'

        if celsius <= 10:
            resp_msg += '\n\nCool! Dress warmer!'
        else:
            resp_msg += '\n\nWarmth! Dress easier!'

        await message.answer(resp_msg)


async def process_moon_phase(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        weather = await client.get(data['city'])
        resp_msg = 'Three-day moon phase forecast.\n'
        for forecast in weather.forecasts:
            resp_msg += f'\nForecast date: {forecast.date}\n'
            resp_msg += f'Moon phase: {forecast.astronomy.moon_phase}\n'
            resp_msg += f'Moon illumination - {forecast.astronomy.moon_illumination}%\n'

        await message.answer(resp_msg)


async def process_hourly_forecasts(message: types.Message):
    await message.answer('🕗 Hourly_forecasts', reply_markup=markups.hourlyForecastsMenu)


async def hourly_forecasts_today(message: types.Message, state: FSMContext):
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
    await message.answer_photo(photo, caption=city)


async def hourly_forecasts_tomorrow(message: types.Message, state: FSMContext):
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
    await message.answer_photo(photo, caption=city)


async def hourly_forecasts_day_after_tomorrow(message: types.Message, state: FSMContext):
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
    await message.answer_photo(photo, caption=city)


async def process_daily_forecasts(message: types.Message, state: FSMContext):
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

        await message.answer(resp_msg)


async def process_closing(message: types.Message, state: FSMContext):
    await state.finish()
    await Form.city.set()
    await message.answer(f'Please enter the city you need.')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(return_to_main_menu, text=["⬅️ Main menu"], state=Form.choice)
    dp.register_message_handler(process_temperature, text=['🌡️ Temperature'], state=Form.choice)
    dp.register_message_handler(process_moon_phase, text=['🌗 Moon_phase'], state=Form.choice)
    dp.register_message_handler(process_hourly_forecasts, text=['🕗 Hourly_forecasts'], state=Form.choice)
    dp.register_message_handler(hourly_forecasts_today, text=[f'📅 {date.today()}'], state=Form.choice)
    dp.register_message_handler(hourly_forecasts_tomorrow, text=[f'📅 {date.tomorrow()}'], state=Form.choice)
    dp.register_message_handler(hourly_forecasts_day_after_tomorrow, text=[f'📅 {date.day_after_tomorrow()}'], state=Form.choice)
    dp.register_message_handler(process_daily_forecasts, text=['📅 Daily_forecasts'], state=Form.choice)
    dp.register_message_handler(process_closing, text=['🏙️ Another city'], state=Form.choice)
    dp.register_message_handler(process_city, state=Form.city)
