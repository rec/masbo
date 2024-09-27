from mastodon import Mastodon
from repcal import RepublicanDate, DecimalTime
from datetime import datetime
import os
import time
import traceback

IS_HOURLY = 'HOURLY' in os.environ

ENABLE_SEND = not True
try:
    ACCESS_TOKEN = open('access-token.txt').read().strip()
except Exception as e:
    print(e)
BASE_URL = 'https://botsin.space/'

HOUR_DELAY = 3601
DAY_DELAY = 24 * 3600 + 11
DELAY = HOUR_DELAY if IS_HOURLY else DAY_DELAY
MAX_LEN = 500

TAGS = '#France #revolution #calendrier #liberté #calendar'
MSG_LEN = MAX_LEN - len(TAGS)


def mastodon():
    return Mastodon(
        access_token = ACCESS_TOKEN,
        api_base_url = 'https://botsin.space/'
    )


def join(strs):
    ml = max(len(s) for s in strs)
    return '\n\n'.join(' ' * (ml - len(s)) // 2 for s in strs)


def temp_date():
    maintenant = datetime.now()
    date = RepublicanDate.from_gregorian(maintenant.date())
    temp = DecimalTime.from_standard_time(maintenant.time())
    h, m, s = str(temp).split(':')
    return f'{h}ʰ {m}ᵐ {s}ˢ', str(date)

def main():
    while True:
        s = '\n\n'.join((*temp_date(), TAGS))
        print(s, len(s))
        if ENABLE_SEND:
            try:
                mastodon().status_post(s)
            except Exception:
                traceback.print_exc()
        time.sleep(DELAY)


if __name__ == '__main__':
    main()
