from repcal import RepublicanDate, DecimalTime
from datetime import datetime


def join(strs):
    ml = max(len(s) for s in strs)
    return '\n\n'.join(' ' * (ml - len(x)) // 2)


def revolution(bot):
    maintenant = datetime.now()
    date = RepublicanDate.from_gregorian(maintenant.date())
    temp = DecimalTime.from_standard_time(maintenant.time())
    h, m, s = str(temp).split(':')
    return f'{h}ʰ {m}ᵐ {s}ˢ\n\n{date}\n'
