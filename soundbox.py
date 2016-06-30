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

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
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
THEME = 'default'

def play_sound(key):
    category = config.KEY_CATEGORY_MAPPING.get(key)
    if category:
        path = os.path.join(config.SOUND_DIRECTORY, THEME, category)
        sound_files = os.listdir(path)
        if len(sound_files) == 0:
            return
        i = random.randrange(0, len(sound_files))
        print('subprocess start')
        subprocess.Popen([config.PLAYER, os.path.join(config.SOUND_DIRECTORY, THEME, category, sound_files[i])], stdin=subprocess.PIPE).wait()
        print('subprocess end')

class KeyEventThread(threading.Thread):
    def run(self):
        keep_going = True
        while keep_going:
            key = getch()
            if key == 'x':
                break
            if config.KEY_CATEGORY_MAPPING.get(key) is None:
                continue 
	    with open("stat.csv", "a") as myfile:
    	        myfile.write("{datetime}, {theme}, {category}\n".format(datetime=datetime.datetime.now(), theme=THEME, category=config.KEY_CATEGORY_MAPPING.get(key)))

            play_sound(key)
            time.sleep(0.1)

kethread = KeyEventThread()
kethread.start()
