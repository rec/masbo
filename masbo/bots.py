import heapq
from .bot import Bot
import json
import time


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
