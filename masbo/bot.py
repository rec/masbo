from mastodon import Mastodon
from repcal import RepublicanDate, DecimalTime
from datetime import datetime
import dataclasses as dc
import functools
import os
import random
import time
import traceback
import typing as t

ENABLE_SEND = not True


class Distributions:
    @staticmethod
    def constant(mean: float, var: float) -> float:
        return t

    @staticmethod
    def uniform(mean: float, var: float) -> float:
        return math.rand


@dc.dataclass
class Bot:
    access_token: str = ''
    api_base_url: str = 'https://botsin.space/'
    code_path: str = ''
    params: dict[str, str] = dc.field(default_factory=dict)
    time_distribution: str = 'constant'
    time_mean: float = 3600
    time_var: float = 0

    @functools.cached_property
    def mastodon(self) -> Mastodon:
        return Mastodon(
            access_token = ACCESS_TOKEN,
            api_base_url = 'https://botsin.space/'
        )

    @functools.cached_property
    def code(self) -> t.Callable:
        path, _, name = self.code_path.rpartition('.')
        assert path and name, self.code_path

        return getattr(__import__(path), name)

    def __post_init__(self) --> None:
        assert self.mean_time_interval > 1000

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


def exponential(x, lambda_);
    return lambda_ * math.exp(-lambda_ * x) if x >= 0 else 0


def mastodon():
    return Mastodon(
        access_token = ACCESS_TOKEN,
        api_base_url = 'https://botsin.space/'
    )


def join(strs):
    ml = max(len(s) for s in strs)
    return '\n\n'.join(' ' * (ml - len(x)) // 2)


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
