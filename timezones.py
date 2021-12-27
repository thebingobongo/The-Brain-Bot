from datetime import datetime, date
import pytz

def get_time(timezone):
    timezone = pytz.timezone(timezone)
    timezone_date_and_time = datetime.now(timezone)
    return timezone_date_and_time.strftime("%H:%M:%S")

def get_EST():
    return get_time('EST')


def get_PST():
    return get_time('PST8PDT')


def get_GMT():
    return get_time('GMT')


def get_CET():
    return get_time("CET")


def get_EET():
    return get_time('EET')


def get_PKT():
    return get_time('Etc/GMT-5')


def get_Today():
    today = date.today()
    d = today.strftime("%b %d, %Y")
    return d
