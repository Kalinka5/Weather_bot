from aiogram import Bot, Dispatcher, executor, types
import python_weather
from setings import TOKEN

# bot init
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
client = python_weather.Client(format=python_weather.IMPERIAL, locale='ru-RU')


# echo
@dp.message_handler()
async def echo(message: types.Message):
    weather = await client.find(message.text)
    celsius = round((weather.current.temperature - 32) / 1.8)

    resp_msg = weather.location_name + '\n'
    resp_msg += f'Текущая температура: {celsius}°\n'
    resp_msg += f'Состояние погоды: {weather.current.sky_text}'

    if celsius <= 10:
        resp_msg += '\n\nПрохладно! Одевайся теплее!'
    else:
        resp_msg += '\n\nТепло! Одевайся легче!'

    # for forecast in weather.forecasts:
    #   print(str(forecast.date), forecast.sky_text, forecast.temperature)

    await message.answer(resp_msg)

# run long-polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
