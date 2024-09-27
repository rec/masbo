import typing as t
from .bot_description import BotDescription
import traceback


class Bot:
    default_tags: t.Sequence[str] = ()

    def __init__(self, desc: BotDescription) -> None:
        self.desc = desc
        tags = self.desc.tags or self.default_tags
        tags = ' '.join('#' + t.lstrip('#') for t in desc.tags)
        self.tags = '\n\n' + tags if tags else tags
        self.max_body = desc.max_chars - len(self.tags)

    def run(self) -> None:
        try:
            res = self._run()
        except Exception:
            traceback.print_exc()
        else:
            self.desc.post(res[:self.max_body] + self.tags)

    def _run(self) -> str:
        raise NotImplementedError

    @staticmethod
    def create(**kwargs) -> 'Bot':
        return Bot(BotDescription(**kwargs))
