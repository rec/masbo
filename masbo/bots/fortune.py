import subprocess


def fortune(bot):
    while True:
        f = subprocess.run('fortune', text=True, stdout=subprocess.PIPE).rstrip()
        if len(f) <= bot.max_body:
            return f

        print('...Fortune too long!', len(f))
