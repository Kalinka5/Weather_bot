import python_weather


def data_forecast(weather: python_weather.Client.get, day: int):
    forecast_data = {'time': [], 'temperature': [], 'description': [], 'kind': []}
    for n, forecast in enumerate(weather.forecasts):
        if n == day:
            for hourly in forecast.hourly:
                forecast_data['time'].append(hourly.time.strftime("%H:%M"))
                forecast_data['temperature'].append(hourly.temperature)
                forecast_data['description'].append(hourly.description)
                forecast_data['kind'].append(hourly.kind)

    return forecast_data
