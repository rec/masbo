import heapq
import json
import time
from . bot import Bot


class BotCollection:
    def __init__(self, bots_file: str, tokens_file: str) -> None:
        bots = json.load(open(bots_file))
        tokens = json.load(open(tokens_file))

        assert isinstance(bots, dict) and isinstance(tokens, dict)
        assert sorted(bots) == sorted(tokens)

        for name, desc in self.descs.items():
            desc['access_token'] = tokens[name]

        self.runners = {k: Bot.create(**v) for k, v in bots.items()}

    def run(self) -> None:
        heap = [(time.time(), str(r.desc), r) for r in self.runners]

        while True:
            t, key, runner = heap[0]
            heapq.heapreplace(heap, (t + runner(), key, runner))
            if (next_event := heap[0][0] - time.time()) > 0:
                time.sleep(next_event)
