import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline


class ImageConverter:
    def __init__(self, language: str, time: list, temperature: list, description: list, kind: list):
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

    def forecast(self, day: str):
        if self.language == "🇬🇧 English":
            plt.xlabel('Time')  # X axis
            plt.ylabel('Temperature')  # Y axis
        else:
            plt.xlabel('Час')  # X axis
            plt.ylabel('Температура')  # Y axis

        if day == "today":
            if self.language == "🇬🇧 English":
                plt.suptitle("Today Hourly Forecast")  # create title
            else:
                plt.suptitle("Погодинний Прогноз На Сьогодні")  # create title
        elif day == "tomorrow":
            if self.language == "🇬🇧 English":
                plt.suptitle("Tomorrow Hourly Forecast")  # create title
            else:
                plt.suptitle("Погодинний Прогноз На Завтра")  # create title
        else:
            if self.language == "🇬🇧 English":
                plt.suptitle("Day After Tomorrow Hourly Forecast")  # create title
            else:
                plt.suptitle("Погодинний Прогноз На Післязавтра")  # create title

        # Make waves chart
        idx = range(len(self.data['time']))
        xnew = np.linspace(min(idx), max(idx), 300)

        spl = make_interp_spline(idx, self.data['temperature'], k=3)
        smooth = spl(xnew)

        plt.plot(self.data['time'], self.data['temperature'], 'o', color='blue', markersize=8)  # Create nodes
        for x, y in zip(self.data['time'], self.data['temperature']):
            label = y
            # Create node's labels
            plt.annotate(label, (x, y),
                         xycoords="data",
                         textcoords="offset points",
                         xytext=(0, 10), ha="center")

        plt.plot(xnew, smooth, color='#00BFFF', linestyle='solid')
        plt.xticks(idx, self.data['time'])
        plt.ylim(min(self.data['temperature'])-2, max(self.data['temperature'])+2)

        if day == "today":
            plt.savefig('Forecasts/Today_forecast.png')
        elif day == "tomorrow":
            plt.savefig('Forecasts/Tomorrow_forecast.png')
        else:
            plt.savefig('Forecasts/Day_After_Tomorrow_forecast.png')

        plt.clf()  # Clear plt
