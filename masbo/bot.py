import typing as t
from .bot_runner import BotRunner


class Bot:
    runner: BotRunner
    tags: t.Sequence[str]

    def __init__(self, runner: BotRunner):
        self.runner = runner

    def __call__(self) -> str:
        raise NotImplementedError
