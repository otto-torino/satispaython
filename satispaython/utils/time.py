from datetime import datetime, timezone


def format_datetime(date):
    return date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'