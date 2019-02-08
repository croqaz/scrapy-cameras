import datetime


def utc_time():
    now = datetime.datetime.utcnow().replace(microsecond=0)
    return now.replace(tzinfo=datetime.timezone.utc).isoformat()


def is_valid_url(url):
    if not isinstance(url, (str, bytes)):
        return False
    return len(url) > 7 and url.split('://', 1)[0] in ('http', 'https')
