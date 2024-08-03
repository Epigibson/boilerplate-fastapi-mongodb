from datetime import datetime, timedelta


def get_current_time_adjust():
    adjusted_time = datetime.now()
    return adjusted_time


def calculate_limit_date(days=30):
    limit_date = datetime.now() + timedelta(days=days)
    return limit_date


def get_first_day_of_current_month():
    now = datetime.now()
    first_day = datetime(now.year, now.month, 1)
    return first_day
