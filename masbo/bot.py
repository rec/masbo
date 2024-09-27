from . import distribution
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


@dc.dataclass
class Bot:
    access_token: str = ''
    api_base_url: str = 'https://botsin.space/'
    autopost: str = True
    code_path: str = ''
    debug: bool = True
    enable: bool = ENABLE_SEND,
    kwargs: dict[str, str] = dc.field(default_factory=dict)
    max_chars: int = 500
    time_distribution: str = 'constant'
    time_mean: float = 3600
    time_var: float = 0

    def __call__(self):
        res = self._code(self)
        if self.autopost:
            self.mastodon.status_post(res[:self.max_chars])

        if self.debug and res is not None:
            print(res)

    @functools.cached_property
    def mastodon(self) -> Mastodon:
        return Mastodon(
            access_token = ACCESS_TOKEN,
            api_base_url = 'https://botsin.space/'
        )

    @functools.cached_property
    def _code(self) -> t.Callable:
        path, _, name = self.code_path.rpartition('.')
        assert path and name, self.code_path

        return getattr(__import__(path), name)

    @functools.cached_property
    def _distrib(self) -> Distribution:
        return Distribution.get(self.time_distribution)(self.time_mean, self.time_var)

    def distrib(self) -> float:
        return self._distrib()

    def __post_init__(self) --> None:
        assert self.mean_time_interval > 1000
