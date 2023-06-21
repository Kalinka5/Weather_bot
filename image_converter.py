import matplotlib.pyplot as plt
import pandas as pd


class ImageConverter:
    def __init__(self, time, temperature, description, kind):
        self.time = time
        self.temperature = temperature
        self.description = description
        self.kind = kind

        data = {
            'time': self.time,
            'temperature': self.temperature,
            'description': self.description,
            'kind': self.kind
        }
        self.df = pd.DataFrame(data, index=data['time'])

    def today_forecast(self):
        self.df[['temperature']].plot(kind="line", legend=True, color=['#FF0000'])
        plt.xlabel('Time')  # X axis
        plt.ylabel('Temperature')  # Y axis
        plt.suptitle("Today Hourly Forecast")  # create title
        plt.savefig('Forecasts/Today_forecast.png')

    def tomorrow_forecast(self):
        self.df[['temperature']].plot(kind="line", legend=True, color=['#FF0000'])
        plt.xlabel('Time')  # X axis
        plt.ylabel('Temperature')  # Y axis
        plt.suptitle("Tomorrow Hourly Forecast")  # create title
        plt.savefig('Forecasts/Tomorrow_forecast.png')

    def day_after_tomorrow_forecast(self):
        self.df[['temperature']].plot(kind="line", legend=True, color=['#FF0000'])
        plt.xlabel('Time')  # X axis
        plt.ylabel('Temperature')  # Y axis
        plt.suptitle("Day After Tomorrow Hourly Forecast")  # create title
        plt.savefig('Forecasts/Day_After_Tomorrow_forecast.png')
