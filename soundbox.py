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

THEME_ID = 0

def play_sound(key, theme_id):
    category = config.KEY_CATEGORY_MAPPING.get(key)
    theme = config.THEME.get(theme_id % len(config.THEME))
    print(category)
    if category:
        path = os.path.join(config.SOUND_DIRECTORY, theme, category)
    else:
        path = os.path.join(config.SOUND_DIRECTORY, theme)
    print(path)
    if not os.path.exists(path):
        return
    sound_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    print(sound_files)
    if len(sound_files) == 0:
        return
    i = random.randrange(0, len(sound_files))
    print('subprocess start')
    if category:
        subprocess.Popen([config.PLAYER, os.path.join(config.SOUND_DIRECTORY, theme, category, sound_files[i])],
                         stdin=subprocess.PIPE).wait()
    else:
        subprocess.Popen([config.PLAYER, os.path.join(config.SOUND_DIRECTORY, theme, sound_files[i])],
                         stdin=subprocess.PIPE).wait()
    print('subprocess end')


def play_start ():
     subprocess.Popen([config.PLAYER, os.path.join(config.SOUND_DIRECTORY, "Start.mp3")],
                         stdin=subprocess.PIPE).wait()

def handle_event (event):
    global THEME_ID
    key = event.ScanCode
    print(event.ScanCode)
    if key == 53:
        sys.exit(0)
    if key == 116:
        THEME_ID += 1
    if config.THEME.get(THEME_ID % len(config.THEME)) is None:
        return
    with open("stat.csv", "a") as myfile:
        if config.KEY_CATEGORY_MAPPING.get(key):
            myfile.write("{datetime}, {theme}, {category}\n".format(datetime=datetime.datetime.now(),
                                                                    theme=config.THEME.get(
                                                                        THEME_ID % len(config.THEME)),
                                                                    category=config.KEY_CATEGORY_MAPPING.get(
                                                                        key)))

    play_sound(key, THEME_ID)
    time.sleep(0.5)

play_start()
hm = HookManager()
hm.HookKeyboard()
hm.KeyUp = handle_event
hm.start()
