from aiogram import types  # , Dispatcher
from Buttons import markups
from create_bot import client
from aiogram.dispatcher import FSMContext
from create_bot import dp


# @dp.message_handler(commands=["start", "help"])
async def command_start(message: types.Message):
    await message.answer(f'Hello, {message.from_user.first_name}.\nPlease enter the city you need.')


@dp.message_handler(content_types=['text'])
def handle_text(message, state: FSMContext):
    if message.text == "🌡️ Temperature":
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
    elif message.text == "🌗 Moon_phase":
        async with state.proxy() as data:
            weather = data['city']
            resp_msg = 'Three-day moon phase forecast.\n'
            for forecast in weather.forecasts:
                resp_msg += f'\nForecast date: {forecast.date}\n'
                resp_msg += f'Moon phase: {forecast.astronomy.moon_phase}\n'
                resp_msg += f'Moon illumination - {forecast.astronomy.moon_illumination}%\n'

            await message.answer(resp_msg)
            await state.finish()
    elif message.text == "🕗 Hourly_forecasts":
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
    elif message.text == "📅 Daily_forecasts":
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
                # resp_msg += f'{forecast.date:%a}: {t}, {descriptions}. {emoji}'

            await message.answer(resp_msg)
            await state.finish()
    else:
        weather = await client.get(message.text)
        async with state.proxy() as data:
            data['city'] = weather
        dp.send_message(message.from_user.id, parse_mode='markdown', reply_markup=markups.mainMenu)


'''# @dp.message_handler(commands=["Temperature"])
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
                resp_msg += f'Time: {hourly.time}'
                resp_msg += f'Temperature: {round((hourly.temperature - 32) / 1.8)}'
                resp_msg += f'Description: {hourly.description}'
                resp_msg += f'Type: {hourly.type}'

        await message.answer(resp_msg)
        await state.finish()


# @dp.message_handler(commands=["Daily_forecasts"])
async def daily_forecasts_command(message: types.Message, state: FSMContext):
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
            # resp_msg += f'{forecast.date:%a}: {t}, {descriptions}. {emoji}'

        await message.answer(resp_msg)
        await state.finish()


# @dp.message_handler()
async def process_city(message: types.Message, state: FSMContext):
    weather = await client.get(message.text)'''
'''for forecast in weather.forecasts:
        forecast.date.weekday()
        for hourly in forecast.hourly:
            hourly.time'''
'''async with state.proxy() as data:
        data['city'] = weather

    await message.answer(f'Wow, cool city. Please choose what you need.', reply_markup=markups.mainMenu)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(temperature_command, commands=["🌡️ Temperature"])
    dp.register_message_handler(moon_phase_command, commands=["🌗 Moon_phase"])
    dp.register_message_handler(hourly_forecasts_command, commands=["🕗 Hourly_forecasts"])
    dp.register_message_handler(daily_forecasts_command, commands=["📅 Daily_forecasts"])
    dp.register_message_handler(process_city)'''
