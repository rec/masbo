from . bot_description import BotDescription
from mastodon import Mastodon
import heapq
import json
import time
import traceback
import typing as t


class BotRunner:
    def __init__(self, desc: BotDescription):
        from . import bots

        self.bot = getattr(bots, self.desc.bot_name.capitalize())(self)
        self.desc = desc

        tags = desc.tags or self.bot.tags
        tags = ' '.join('#' + t.lstrip('#') for t in tags)
        self.tags = '\n\n' + tags if tags else tags

        self.max_body = desc.max_chars - len(self.tags)
        self.mastodon = Mastodon(
            access_token = desc.access_token,
            api_base_url = desc.api_base_url,
        )

    def __call__(self) -> float:
        try:
            res = self._bot()
            if self.desc.autopost and self.desc.enable:
                self.mastodon.status_post(res[:self.max_body] + self.tags)
            if self.desc.debug and res is not None:
                print(res)
        except Exception:
            traceback.print_exc()

        return self.desc.distrib()


def run(bots: t.Sequence[BotRunner]):
    heap = [(time.time(), str(b), b) for b in bots]

    while True:
        t, key, bot = heap[0]
        heapq.heapreplace(heap, (t + bot(), key, bot))
        if (next_event := heap[0][0] - time.time()) > 0:
            time.sleep(next_event)


def read(bots_file: str, tokens_file: str) -> dict[str, t.Any]:
    bots = json.load(open(bots_file))
    tokens = json.load(open(tokens_file))

    assert isinstance(bots, dict) and isinstance(tokens, dict)
    assert sorted(bots) == sorted(tokens)
    for name, bot in bots.items():
        bot.access_token = tokens[name]

    return bots
