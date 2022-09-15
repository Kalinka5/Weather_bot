from aiogram import Bot, Dispatcher, executor, types
import python_weather
from setings import TOKEN

# bot init
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
client = python_weather.Client(format=python_weather.IMPERIAL)


# echo
@dp.message_handler()
async def echo(message: types.Message):
    weather = await client.get(message.text)
    celsius = round((weather.current.temperature - 32) / 1.8)

    resp_msg = f'{weather.nearest_area.region}; {weather.nearest_area.country}\n'
    resp_msg += f'Current temperature: {celsius}°\n'
    resp_msg += f'State of the weather: {weather.current.type}'

    if celsius <= 10:
        resp_msg += '\n\nCool! Dress warmer!'
    else:
        resp_msg += '\n\nWarmth! Dress easier!'

    # for forecast in weather.forecasts:
    #   print(str(forecast.date), forecast.sky_text, forecast.temperature)

    await message.answer(resp_msg)

# run long-polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
