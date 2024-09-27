import heapq
from .bot import Bot
import json


class Bots:
    def __init__(self, bots: dict[str, Bot]) -> None:
        self._bot_heap[:] = ((0, str(b), b) for b in bots)

    def __call__(self) -> float:
        time, key, bot = self._bot_heap[0]
        time += bot()
        heapq.heapreplace(self._bot_heap, (time, key, bot))
        return time


def read(bots_file: str, tokens_file: str) -> Bots:
    bots = json.load(open(bots_file))
    tokens = json.load(open(tokens_file))

    assert isinstance(bots, dict) and isinstance(tokens, dict)
    assert sorted(bots) == sorted(tokens)
    for name, bot in bots.items():
        bot.access_token = tokens[name]

    return Bots(bots)
