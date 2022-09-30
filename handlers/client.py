from aiogram import types, Dispatcher
from Buttons import markups
from create_bot import client
from aiogram.dispatcher import FSMContext


# @dp.message_handler(commands=["start", "help"])
async def command_start(message: types.Message):
    await message.answer(f'Hello, {message.from_user.first_name}.\nPlease enter the city you need.')


# @dp.message_handler(content_types=['text'])
async def handle_text(message: types.Message, state: FSMContext):
    resp_msg = ''
    async with state.proxy() as data:
        if message.text == "🌡️ Temperature":
            weather = data['city']
            celsius = round((weather.current.temperature - 32) / 1.8)

            resp_msg += f'{weather.nearest_area.name}; {weather.nearest_area.country}\n'
            resp_msg += f'Current temperature: {celsius}°\n'
            resp_msg += f'State of the weather: {weather.current.type}'

            if celsius <= 10:
                resp_msg += '\n\nCool! Dress warmer!'
            else:
                resp_msg += '\n\nWarmth! Dress easier!'

        elif message.text == "🌗 Moon_phase":
            weather = data['city']
            resp_msg = 'Three-day moon phase forecast.\n'
            for forecast in weather.forecasts:
                resp_msg += f'\nForecast date: {forecast.date}\n'
                resp_msg += f'Moon phase: {forecast.astronomy.moon_phase}\n'
                resp_msg += f'Moon illumination - {forecast.astronomy.moon_illumination}%\n'

        elif message.text == "🕗 Hourly_forecasts":
            weather = data['city']
            resp_msg = 'Three-day temperature forecast.\n\n'

            for forecast in weather.forecasts:
                for hourly in forecast.hourly:
                    resp_msg += f'Time: {hourly.time}'
                    resp_msg += f'Temperature: {round((hourly.temperature - 32) / 1.8)}'
                    resp_msg += f'Description: {hourly.description}'
                    resp_msg += f'Type: {hourly.type}'

        elif message.text == "📅 Daily_forecasts":
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
        else:
            weather = await client.get(message.text)
            '''for forecast in weather.forecasts:
                forecast.date.weekday()
                for hourly in forecast.hourly:
                    hourly.time'''
            async with state.proxy() as data:
                data['city'] = weather

            await message.answer(f'Wow, cool city. Please choose what you need.', reply_markup=markups.mainMenu)

        await message.answer(resp_msg)
        await state.finish()


# @dp.message_handler()
'''async def process_city(message: types.Message, state: FSMContext):
    weather = await client.get(message.text)'''
'''for forecast in weather.forecasts:
        forecast.date.weekday()
        for hourly in forecast.hourly:
            hourly.time'''
'''async with state.proxy() as data:
        data['city'] = weather

    await message.answer(f'Wow, cool city. Please choose what you need.', reply_markup=markups.mainMenu)'''


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(handle_text)  # , content_types=['text'])
    # dp.register_message_handler(process_city)
