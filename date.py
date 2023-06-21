import datetime


class Date:
    def __init__(self):
        self.__current_year = datetime.date.today().year
        self.__current_month = datetime.date.today().month
        self.__current_day = datetime.date.today().day
        self.__tomorrow = int(self.__current_day) + 1
        self.__day_after_tomorrow = int(self.__current_day) + 2
        self.__some_date = datetime.date(2023, 6, 19).strftime("%d.%m.%Y")

    def today(self):
        today_date = datetime.date(2023, 6, self.__current_day).strftime("%d.%m.%Y")
        return today_date

    def tomorrow(self):
        tomorrow_date = datetime.date(2023, 6, self.__tomorrow).strftime("%d.%m.%Y")
        return tomorrow_date

    def day_after_tomorrow(self):
        day_after_tomorrow_date = datetime.date(2023, 6, self.__day_after_tomorrow).strftime("%d.%m.%Y")
        return day_after_tomorrow_date
