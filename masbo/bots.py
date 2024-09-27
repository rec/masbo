from repcal import RepublicanDate, DecimalTime
from datetime import datetime
import subprocess

from .bot import Bot


class Fortune(Bot):
    tags = 'humor', 'unix', 'usr', 'games', 'fortune'

    def __call__(self):
        while True:
            f = subprocess.run('fortune', text=True, stdout=subprocess.PIPE).rstrip()
            if len(f) <= self.runner.max_body:
                return f

            print('...Fortune too long!', len(f))


class Revolution(Bot):
    tags = 'France', 'revolution', 'calendrier', 'liberté', 'calendar'

    def __call__(self):
        maintenant = datetime.now()
        date = RepublicanDate.from_gregorian(maintenant.date())
        temp = DecimalTime.from_standard_time(maintenant.time())
        h, m, s = str(temp).split(':')
        return f"C'est {h}ʰ {m}ᵐ {s}ˢ, {date}"
