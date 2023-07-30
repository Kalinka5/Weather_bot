import datetime


def today():
    today_date = datetime.datetime.today().strftime("%d.%m.%Y")
    return today_date


def tomorrow():
    tomorrow_date = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%d.%m.%Y")
    return tomorrow_date


def day_after_tomorrow():
    day_after_tomorrow_date = (datetime.datetime.today() + datetime.timedelta(days=2)).strftime("%d.%m.%Y")
    return day_after_tomorrow_date
