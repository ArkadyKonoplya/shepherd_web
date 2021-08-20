import datetime
from dateutil.relativedelta import relativedelta
import pytz

from django import template

register = template.Library()


def get_item(dictionary, key):

    if key not in dictionary.keys():
        try:
            return dictionary.get(str(key))
        except KeyError:
            raise ("Key not found!")
    else:
        return dictionary.get(key)


def get_latitude(point):
    return point[0]


def get_longitude(point):
    return point[1]


def get_time_diff_today(start_date):
    today = datetime.datetime.now(tz=pytz.UTC)

    return relativedelta(today, start_date)


def get_time_diff(start_date, end_date):

    return relativedelta(end_date, start_date)

register.filter("get_item", get_item)
register.filter("get_latitude", get_latitude)
register.filter("get_longitude", get_longitude)
register.filter("get_time_diff_today", get_time_diff_today)
register.filter("get_time_diff", get_time_diff)
