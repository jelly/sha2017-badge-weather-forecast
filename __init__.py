#!/usr/bin/python

'''

Obtain the location code by querying the following URL with your city as argument.

https://api.buienradar.nl/data/search/1.0/?query=Delft&country=NL&locale=nl-NL

Check the used uri and use the number in the result for the following url.

https://api.buienradar.nl/data/forecast/1.1/daily/2757345
'''

import gc
import badge
import easywifi
import ugfx
import utime
import deepsleep

import urequests as requests

WIDTH = 295
HEIGHT = 128
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


def clear_screen():
    ugfx.clear(ugfx.BLACK)
    ugfx.flush()
    ugfx.clear(ugfx.WHITE)
    ugfx.flush()


def init():
    easywifi.enable()
    clear_screen()


def get_days():
    url = 'https://api.buienradar.nl/data/forecast/1.1/daily/{}'.format(LOC_CODE)
    r = requests.get(url)
    data = r.json()

    xpos = 0
    for index, day_data in enumerate(data['days']):
        if index == 4:
            break

        ypos = 0

        # 2018-06-24T00:00:00
        date = day_data['date'].split('T')[0]
        # Strip year
        date = date[5:]
        month, day = date.split('-')

        text = '{}-{}'.format(day, month)
        twidth = ugfx.get_string_width(text, FONT)
        ugfx.string(xpos, ypos, text, FONT, ugfx.BLACK)

        ypos += 22
        iconcode = day_data['iconcode']
        icon = BUIENRADAR_ICONS.get(iconcode)
        # Add xpos a bit since icons are weird
        ugfx.string(xpos + 10, ypos, icon, "weather42", ugfx.BLACK)

        # Min / Max / Rain
        ypos += 44

        text = str(int(day_data['maxtemperature'])) + 'C'
        ugfx.string(xpos, ypos, text, FONT, ugfx.BLACK)

        ypos += 20

        text = str(int(day_data['mintemperature'])) + 'C'
        ugfx.string(xpos, ypos, text, FONT, ugfx.BLACK)

        ypos += 20

        text = str(int(day_data['precipitationmm'])) + 'mm'
        ugfx.string(xpos, ypos, text, FONT, ugfx.BLACK)

        xpos += twidth + 2



init()
get_days()

badge.eink_busy_wait()
ugfx.flush(ugfx.LUT_FULL)
badge.eink_busy_wait()

# Sleep for 30 minutes
deepsleep.start_sleeping(1800000)
