#! /usr/bin/python
import threading
import time
import os
import random
import subprocess
import config
import datetime
import sys
from pyxhook import HookManager

THEME = 'default'

def play_sound(key):
    category = config.KEY_CATEGORY_MAPPING.get(key)
    print(category)
    if category:
        path = os.path.join(config.SOUND_DIRECTORY, THEME, category)
        sound_files = os.listdir(path)
        if len(sound_files) == 0:
            return
        i = random.randrange(0, len(sound_files))
        print('subprocess start')
        subprocess.Popen([config.PLAYER, os.path.join(config.SOUND_DIRECTORY, THEME, category, sound_files[i])], stdin=subprocess.PIPE).wait()
        print('subprocess end')



def handle_event (event):
    key = event.Ascii
    print(key)
    if key == 120:
        sys.exit(0)
    if config.KEY_CATEGORY_MAPPING.get(key) is None:
        return
    with open("stat.csv", "a") as myfile:
        myfile.write("{datetime}, {theme}, {category}\n".format(datetime=datetime.datetime.now(), theme=THEME, category=config.KEY_CATEGORY_MAPPING.get(key)))
        play_sound(key)


hm = HookManager()
hm.HookKeyboard()
hm.KeyUp = handle_event
hm.start()
