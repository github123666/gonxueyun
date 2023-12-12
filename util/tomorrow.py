from datetime import datetime, timedelta


def tomorrow_1_clock() -> int:
    """
    tomorrow 1.am ctime
    :return:
    """
    now = datetime.now()
    tomorrow = datetime(now.year, now.month, now.day, 1, 0, 0) + timedelta(days=1)
    return int(tomorrow.timestamp())


def next_week_submit_time() -> int:
    """
    next week submit time
    :return:
    """
    now = datetime.now()
    tomorrow = datetime(now.year, now.month, now.day, 1, 0, 0) + timedelta(days=7)
    return int(tomorrow.timestamp())


def next_submit_month_time() -> int:
    """
    next submit month report time
    :return:
    """
    now = datetime.now()
    if now.month == 12:
        return int(datetime(now.year + 1, 1, 1).timestamp())
    else:
        return int(datetime(now.year, now.year + 1, 1).timestamp())


if __name__ == '__main__':
    print(tomorrow_1_clock())
