#!/usr/bin/python

'''

Obtain the location code by querying the following URL with your city as argument.

https://api.buienradar.nl/data/search/1.0/?query=Delft&country=NL&locale=nl-NL

Check the used uri and use the number in the result for the following url.

https://api.buienradar.nl/data/forecast/1.1/daily/2757345
'''

import badge
import easywifi
import ugfx
import deepsleep
import utime
import easyrtc


import urequests as requests


WIDTH = 295
HEIGHT = 128
SMALL_FONT = "Roboto_Regular12"
FONT = 'Roboto_BlackItalic24'
LOC_CODE = 2757345

BUIENRADAR_ICONS = {
    "a": "\uf00d",
    "b": "\uf002",
    "c": "\uf041",
    "d": "\uf001",
    "f": "\uf019",
    "g": "\uf01e",
    "h": "\uf019",
    "i": "\uf026",
    "j": "\uf002",
    "k": "\uf019",
    "l": "\uf019",
    "m": "\uf01c",
    "n": "\uf021",
    "o": "\uf002",
    "q": "\uf019",
    "r": "\uf002",
    "s": "\uf01e",
    "t": "\uf01b",
    "u": "\uf01b",
    "v": "\uf01b",
    "w": "\uf01b",
}

WEEKDAYS = {
    1: 'Sun',
    2: 'Mon',
    3: 'Tue',
    4: 'Wed',
    5: 'Thu',
    6: 'Fri',
    7: 'Sat',
}


def clear_screen():
    ugfx.clear(ugfx.BLACK)
    ugfx.flush()
    ugfx.clear(ugfx.WHITE)
    ugfx.flush()


def init():
    badge.init()
    ugfx.init()
    easywifi.enable()
    easyrtc.configure()
    clear_screen()


def get_days(temp):
    url = 'https://dedi.vdwaa.nl/~jelle/weather.json'
    r = requests.get(url)
    data = r.json()

    xpos = 0
    weekday = utime.localtime()[6]
    for index, day_data in enumerate(data):
        if index == 4:
            break

        ypos = 0

        text = WEEKDAYS[weekday]
        twidth = ugfx.get_string_width(text, FONT)
        ugfx.string(xpos, ypos, text, FONT, ugfx.BLACK)

        ypos += 22
        iconcode = day_data['iconcode']
        icon = BUIENRADAR_ICONS.get(iconcode)
        # Add xpos a bit since icons are weird
        ugfx.string(xpos + 10, ypos, icon, "weather42", ugfx.BLACK)

        # Min / Max / Rain
        ypos += 44

        text = str(int(day_data['maxtemp'])) + 'C'
        ugfx.string(xpos, ypos, text, FONT, ugfx.BLACK)

        ypos += 20

        text = str(int(day_data['mintemp'])) + 'C'
        ugfx.string(xpos, ypos, text, FONT, ugfx.BLACK)

        ypos += 20

        text = str(int(day_data['precipitation'])) + 'mm'
        ugfx.string(xpos, ypos, text, FONT, ugfx.BLACK)

        xpos += twidth + 24

        if weekday == 7:
            weekday = 1
        else:
            weekday += 1


init()
get_days(temp)

badge.eink_busy_wait()
ugfx.flush(ugfx.LUT_FULL)
badge.eink_busy_wait()

# Sleep for 10 minutes
deepsleep.start_sleeping(600000)
