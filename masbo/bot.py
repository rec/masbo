from .distribution import Distribution
from mastodon import Mastodon
import dataclasses as dc
import functools
import heapq
import json
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
    tags: list[str] = dc.field(default_factory=list)
    time_distribution: str = 'constant'
    time_mean: float = 3600
    time_var: float = 0

    def __post_init__(self) -> None:
        assert self.mean_time_interval > 1000
        tags = ' '.join('#' + t.lstrip('#') for t in self.tags)
        self._tags = '\n' + tags if tags else tags
        self.max_body = self.max_chars - len(self._tags)

    def __call__(self) -> float:
        try:
            res = self._code(self)
            if self.autopost and self.enable:
                self.mastodon.status_post(res[:self.max_body] + self._tags)
            if self.debug and res is not None:
                print(res)
        except Exception:
            traceback.print_exc()

        return self._distrib()

    @functools.cached_property
    def mastodon(self) -> Mastodon:
        return Mastodon(
            access_token = self.access_token,
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


def run(bots: dict[str, Bot]):
    heap = [(time.time(), str(b), b) for b in bots]

    while True:
        t, key, bot = heap[0]
        heapq.heapreplace(heap, (t + bot(), key, bot))
        if (next_event := heap[0][0] - time.time()) > 0:
            time.sleep(next_event)


def read(bots_file: str, tokens_file: str) -> dict[str, Bot]:
    bots = json.load(open(bots_file))
    tokens = json.load(open(tokens_file))

    assert isinstance(bots, dict) and isinstance(tokens, dict)
    assert sorted(bots) == sorted(tokens)
    for name, bot in bots.items():
        bot.access_token = tokens[name]

    return bots
