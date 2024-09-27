from . bot_description import BotDescription
from mastodon import Mastodon
import traceback


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

    @staticmethod
    def create(**kwargs) -> 'BotRunner':
        return BotRunner(BotDescription(**kwargs))
