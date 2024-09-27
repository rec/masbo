import dataclasses as dc
from .bot import Bot


@dc.dataclass
class Bots:
    bots: list[Bot]

    _bot_heap: list[tuple[float, str, Bot]] = dc.field(default_factory=list)

    def play_next(self, time: float) -> float:
        if not self._bot_heap:
            self._bot_heap.extend((time, str(b), b) for b in self.bots)

        _, sbot, bot = self._bot_heap.pop()
        bot()
