import datetime


def utc_time():
    now = datetime.datetime.utcnow().replace(microsecond=0)
    return now.replace(tzinfo=datetime.timezone.utc).isoformat()
