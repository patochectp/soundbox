import threading
import time
import os
import random
import subprocess
import config
import datetime


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty
        import sys

    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()


def play_sound(key, theme_id):
    category = config.KEY_CATEGORY_MAPPING.get(key)
    theme = config.THEME.get(theme_id % len(config.THEME))
    print(category)
    if category:
        path = os.path.join(config.SOUND_DIRECTORY, theme, category)
        print(path)
        if not os.path.exists(path):
            return
        sound_files = os.listdir(path)
        if len(sound_files) == 0:
            return
        i = random.randrange(0, len(sound_files))
        print('subprocess start')
        subprocess.Popen([config.PLAYER, os.path.join(config.SOUND_DIRECTORY, theme, category, sound_files[i])],
                         stdin=subprocess.PIPE).wait()
        print('subprocess end')


class KeyEventThread(threading.Thread):
    def run(self):
        theme_id = 0
        while True:
            key = ord(next(inp for inp in getch()))
            # key = ord(getch())
            print(key)
            if key == 120:
                break
            if key == 27:
                theme_id += 1
            if config.KEY_CATEGORY_MAPPING.get(key) is None:
                continue
            if config.THEME.get(theme_id % len(config.THEME)) is None:
                continue
            with open("stat.csv", "a") as myfile:
                myfile.write("{datetime}, {theme}, {category}\n".format(datetime=datetime.datetime.now(),
                                                                        theme=config.THEME.get(
                                                                            theme_id % len(config.THEME)),
                                                                        category=config.KEY_CATEGORY_MAPPING.get(key)))

            play_sound(key, theme_id)
            time.sleep(0.1)


kethread = KeyEventThread()
kethread.start()
