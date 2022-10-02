from aiogram import types, Dispatcher
from Buttons import markups
from create_bot import client
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    city = State()  # Will be represented in storage as 'Form:city'
    choice = State()


# @dp.message_handler(commands=["start", "help"])
async def command_start(message: types.Message):
    # Set state
    await Form.city.set()

    await message.answer(f'Hello, {message.from_user.first_name}.\nPlease enter the city you need.')


# @dp.message_handler(state=Form.city)
async def process_city(message: types.Message, state: FSMContext):
    weather = await client.get(message.text)
    '''for forecast in weather.forecasts:
        forecast.date.weekday()
        for hourly in forecast.hourly:
            hourly.time'''
    async with state.proxy() as data:
        data['city'] = weather

    await Form.next()
    await message.answer(f'Wow, cool city. Please choose what you need.', reply_markup=markups.mainMenu)


# @dp.message_handler(lambda message: message.text == '🌡️ Temperature', state=Form.choice)
async def process_temperature(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        resp_msg = ''
        weather = data['city']
        celsius = round((weather.current.temperature - 32) / 1.8)

        resp_msg += f'{weather.nearest_area.name}; {weather.nearest_area.country}\n'
        resp_msg += f'Current temperature: {celsius}°\n'
        resp_msg += f'State of the weather: {weather.current.type}'

        if celsius <= 10:
            resp_msg += '\n\nCool! Dress warmer!'
        else:
            resp_msg += '\n\nWarmth! Dress easier!'

        await message.answer(resp_msg)
    await state.finish()


# @dp.message_handler(lambda message: message.text == '🌗 Moon_phase', state=Form.choice)
async def process_moon_phase(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        weather = data['city']
        resp_msg = 'Three-day moon phase forecast.\n'
        for forecast in weather.forecasts:
            resp_msg += f'\nForecast date: {forecast.date}\n'
            resp_msg += f'Moon phase: {forecast.astronomy.moon_phase}\n'
            resp_msg += f'Moon illumination - {forecast.astronomy.moon_illumination}%\n'

        await message.answer(resp_msg)
    await state.finish()


# @dp.message_handler(lambda message: message.text == '🕗 Hourly_forecasts', state=Form.choice)
async def process_hourly_forecasts(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        weather = data['city']
        resp_msg = 'Three-day temperature forecast.\n\n'

        for forecast in weather.forecasts:
            for hourly in forecast.hourly:
                resp_msg += f'Time: {hourly.time}'
                resp_msg += f'Temperature: {round((hourly.temperature - 32) / 1.8)}'
                resp_msg += f'Description: {hourly.description}'
                resp_msg += f'Type: {hourly.type}'

        await message.answer(resp_msg)
    await state.finish()


# @dp.message_handler(lambda message: message.text == '📅 Daily_forecasts', state=Form.choice)
async def process_daily_forecasts(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        weather = data['city']
        resp_msg = 'Three-day temperature forecast.\n\n'

        for forecast in weather.forecasts:
            day = f"{forecast.date}"
            t_lowest = f"{round((forecast.lowest_temperature - 32) / 1.8)}"
            t_highest = f"{round((forecast.highest_temperature - 32) / 1.8)}"
            descriptions = ", ".join(set(h.description for h in forecast.hourly))
            # emoji = "".join(map(repr, set(h.type for h in forecast.hourly)))
            resp_msg += f'Date: {day}.' \
                        f'\nTemperature will be from {t_lowest} to {t_highest}°C\n' \
                        f'Description: {descriptions}\n\n'
            # resp_msg += f'{forecast.date:%a}: {t}, {adescriptions}. {emoji}'

        await message.answer(resp_msg)
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(process_temperature,
                                lambda message: message.text == ['🌡️ Temperature'],
                                state=Form.choice)
    dp.register_message_handler(process_moon_phase,
                                lambda message: message.text == ['🌗 Moon_phase'],
                                state=Form.choice)
    dp.register_message_handler(process_hourly_forecasts,
                                lambda message: message.text == ['🕗 Hourly_forecasts'],
                                state=Form.choice)
    dp.register_message_handler(process_daily_forecasts,
                                lambda message: message.text == ['📅 Daily_forecasts'],
                                state=Form.choice)
    dp.register_message_handler(process_city, state=Form.city)
