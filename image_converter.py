import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline


class ImageConverter:
    def __init__(self, time, temperature, description, kind):
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

        plt.xlabel('Time')  # X axis
        plt.ylabel('Temperature')  # Y axis
        plt.suptitle("Today Hourly Forecast")  # create title

        idx = range(len(self.data['time']))
        xnew = np.linspace(min(idx), max(idx), 300)

        spl = make_interp_spline(idx, self.data['temperature'], k=3)
        smooth = spl(xnew)

        plt.plot(self.data['time'], self.data['temperature'], 'o', color='#00BFFF', markersize=8)
        plt.plot(xnew, smooth, color='blue', linestyle='solid')
        plt.xticks(idx, self.data['time'])
        plt.savefig('Forecasts/Today_forecast.png')
        plt.clf()

    def tomorrow_forecast(self):

        plt.xlabel('Time')  # X axis
        plt.ylabel('Temperature')  # Y axis
        plt.suptitle("Tomorrow Hourly Forecast")  # create title

        idx = range(len(self.data['time']))
        xnew = np.linspace(min(idx), max(idx), 300)

        spl = make_interp_spline(idx, self.data['temperature'], k=3)
        smooth = spl(xnew)

        plt.plot(self.data['time'], self.data['temperature'], 'o', color='#00BFFF', markersize=8)
        plt.plot(xnew, smooth, color='blue', linestyle='solid')
        plt.xticks(idx, self.data['time'])
        plt.savefig('Forecasts/Tomorrow_forecast.png')
        plt.clf()

    def day_after_tomorrow_forecast(self):

        plt.xlabel('Time')  # X axis
        plt.ylabel('Temperature')  # Y axis
        plt.suptitle("Day After Tomorrow Hourly Forecast")  # create title

        idx = range(len(self.data['time']))
        xnew = np.linspace(min(idx), max(idx), 300)

        spl = make_interp_spline(idx, self.data['temperature'], k=3)
        smooth = spl(xnew)

        plt.plot(self.data['time'], self.data['temperature'], 'o', color='#00BFFF', markersize=8)
        plt.plot(xnew, smooth, color='blue', linestyle='solid')
        plt.xticks(idx, self.data['time'])
        plt.savefig('Forecasts/Day_After_Tomorrow_forecast.png')
        plt.clf()
