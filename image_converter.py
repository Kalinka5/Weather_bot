import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline


class ImageConverter:
    def __init__(self, language, time, temperature, description, kind):
        self.language = language
        self.time = time
        self.temperature = temperature
        self.description = description
        self.kind = kind

        self.data = {
            'time': self.time,
            'temperature': self.temperature,
            'description': self.description,
            'kind': self.kind
        }
        self.df = pd.DataFrame(self.data, index=self.data['time'])

    def today_forecast(self):

        if self.language == "🇬🇧 English":
            plt.xlabel('Time')  # X axis
            plt.ylabel('Temperature')  # Y axis
            plt.suptitle("Today Hourly Forecast")  # create title
        else:
            plt.xlabel('Час')  # X axis
            plt.ylabel('Температура')  # Y axis
            plt.suptitle("Погодинний Прогноз На Сьогодні")  # create title

        idx = range(len(self.data['time']))
        xnew = np.linspace(min(idx), max(idx), 300)

        spl = make_interp_spline(idx, self.data['temperature'], k=3)
        smooth = spl(xnew)

        plt.plot(self.data['time'], self.data['temperature'], 'o', color='blue', markersize=8)
        for x, y in zip(self.data['time'], self.data['temperature']):
            label = y
            plt.annotate(label, (x, y),
                         xycoords="data",
                         textcoords="offset points",
                         xytext=(0, 10), ha="center")

        plt.plot(xnew, smooth, color='#00BFFF', linestyle='solid')
        plt.xticks(idx, self.data['time'])
        plt.ylim(min(self.data['temperature'])-2, max(self.data['temperature'])+2)
        plt.savefig('Forecasts/Today_forecast.png')
        plt.clf()

    def tomorrow_forecast(self):

        if self.language == "🇬🇧 English":
            plt.xlabel('Time')  # X axis
            plt.ylabel('Temperature')  # Y axis
            plt.suptitle("Tomorrow Hourly Forecast")  # create title
        else:
            plt.xlabel('Час')  # X axis
            plt.ylabel('Температура')  # Y axis
            plt.suptitle("Погодинний Прогноз На Завтра")  # create title

        idx = range(len(self.data['time']))
        xnew = np.linspace(min(idx), max(idx), 300)

        spl = make_interp_spline(idx, self.data['temperature'], k=3)
        smooth = spl(xnew)

        plt.plot(self.data['time'], self.data['temperature'], 'o', color='blue', markersize=8)
        for x, y in zip(self.data['time'], self.data['temperature']):
            label = y
            plt.annotate(label, (x, y),
                         xycoords="data",
                         textcoords="offset points",
                         xytext=(0, 10), ha="center")

        plt.plot(xnew, smooth, color='#00BFFF', linestyle='solid')
        plt.xticks(idx, self.data['time'])
        plt.ylim(min(self.data['temperature'])-2, max(self.data['temperature'])+2)
        plt.savefig('Forecasts/Tomorrow_forecast.png')
        plt.clf()

    def day_after_tomorrow_forecast(self):

        if self.language == "🇬🇧 English":
            plt.xlabel('Time')  # X axis
            plt.ylabel('Temperature')  # Y axis
            plt.suptitle("Day After Tomorrow Hourly Forecast")  # create title
        else:
            plt.xlabel('Час')  # X axis
            plt.ylabel('Температура')  # Y axis
            plt.suptitle("Погодинний Прогноз На Післязавтра")  # create title

        idx = range(len(self.data['time']))
        xnew = np.linspace(min(idx), max(idx), 300)

        spl = make_interp_spline(idx, self.data['temperature'], k=3)
        smooth = spl(xnew)

        plt.plot(self.data['time'], self.data['temperature'], 'o', color='blue', markersize=8)
        for x, y in zip(self.data['time'], self.data['temperature']):
            label = y
            plt.annotate(label, (x, y),
                         xycoords="data",
                         textcoords="offset points",
                         xytext=(0, 10), ha="center")

        plt.plot(xnew, smooth, color='#00BFFF', linestyle='solid')
        plt.xticks(idx, self.data['time'])
        plt.ylim(min(self.data['temperature'])-2, max(self.data['temperature'])+2)
        plt.savefig('Forecasts/Day_After_Tomorrow_forecast.png')
        plt.clf()
