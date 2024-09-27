import dataclasses as dc
from .distribution import Distribution
import functools
from mastodon import Mastodon
import typing as t

if t.TYPE_CHECKING:
    from . bot import Bot

ENABLE_SEND = not True


@dc.dataclass
class BotDescription:
    access_token: str = ''
    api_base_url: str = 'https://botsin.space/'
    autopost: str = True
    bot_name: str = ''
    debug: bool = True
    enable: bool = ENABLE_SEND,
    kwargs: dict[str, str] = dc.field(default_factory=dict)
    max_chars: int = 500
    tags: list[str] = dc.field(default_factory=list)
    time_distribution: str = 'constant'
    time_mean: float = 3600
    time_var: float = 0

    def __post_init__(self):
        assert self.mean_time_interval > 1000

    @functools.cached_property
    def bot(self) -> 'Bot':
        from . import bots

        return getattr(bots, self.bot_name.capitalize())(self)

    @functools.cached_property
    def distrib(self) -> Distribution:
        return Distribution.create(
            self.time_distribution,
            self.time_mean,
            self.time_var,
        )

    @functools.cached_property
    def mastodon(self) -> Mastodon:
        return Mastodon(
            access_token = self.access_token,
            api_base_url = self.api_base_url,
        )

    def post(self, s: str) -> None:
        if self.autopost and self.enable:
            self.mastodon.status_post(s)
        if self.desc.debug:
            print(s)
