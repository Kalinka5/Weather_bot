from aiogram import types, Dispatcher
from Buttons import markups
from create_bot import client
from aiogram.dispatcher import FSMContext


# @dp.message_handler(commands=["start", "help"])
async def command_start(message: types.Message):
    await message.answer(f'Hello, {message.from_user.first_name}.\nPlease enter the city you need.')


# @dp.message_handler(commands=["Temperature"])
async def temperature_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        weather = data['city']
        celsius = round((weather.current.temperature - 32) / 1.8)
        resp_msg = ''

        resp_msg += f'{weather.nearest_area.name}; {weather.nearest_area.country}\n'
        resp_msg += f'Current temperature: {celsius}°\n'
        resp_msg += f'State of the weather: {weather.current.type}'

        if celsius <= 10:
            resp_msg += '\n\nCool! Dress warmer!'
        else:
            resp_msg += '\n\nWarmth! Dress easier!'

        await message.answer(resp_msg)
        await state.finish()


# @dp.message_handler(commands=["Moon_phase"])
async def moon_phase_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        weather = data['city']
        resp_msg = 'Three-day moon phase forecast.\n'
        for forecast in weather.forecasts:
            resp_msg += f'\nForecast date: {forecast.date}\n'
            resp_msg += f'Moon phase: {forecast.astronomy.moon_phase}\n'
            resp_msg += f'Moon illumination - {forecast.astronomy.moon_illumination}%\n'

        await message.answer(resp_msg)
        await state.finish()


# @dp.message_handler(commands=["Hourly_forecasts"])
async def hourly_forecasts_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        weather = data['city']
        resp_msg = 'Three-day temperature forecast.\n\n'

        for forecast in weather.forecasts:
            for hourly in forecast.hourly:
                resp_msg += f'Time: {hourly.time.real}\n'
                resp_msg += f'Temperature --> {round((hourly.temperature - 32) / 1.8)}°\n'
                resp_msg += f'Description --> {hourly.description}\n'
                resp_msg += f'Type --> {hourly.type}\n'
                resp_msg += '\n'

        await message.answer(resp_msg)
        await state.finish()


# @dp.message_handler()
async def process_city(message: types.Message, state: FSMContext):
    weather = await client.get(message.text)
    '''for forecast in weather.forecasts:
        for hourly in forecast.hourly:
            hourly.time.imag'''
    async with state.proxy() as data:
        data['city'] = weather

    await message.answer(f'Wow, cool city. Please choose what you need.', reply_markup=markups.mainMenu)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(temperature_command, commands=["Temperature"])
    dp.register_message_handler(moon_phase_command, commands=["Moon_phase"])
    dp.register_message_handler(hourly_forecasts_command, commands=["Hourly_forecasts"])
    dp.register_message_handler(process_city)