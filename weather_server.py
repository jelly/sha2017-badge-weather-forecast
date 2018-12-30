#1/usr/bin/python

import os
from datetime import datetime, timedelta

import requests
from flask import Flask, jsonify


app = Flask(__name__)


class cached(object):
    def __init__(self, *args, **kwargs):
        self.cached_function_responses = {}
        self.default_max_age = kwargs.get("default_cache_max_age", timedelta(seconds=0))

    def __call__(self, func):
        def inner(*args, **kwargs):
            max_age = kwargs.get('max_age', self.default_max_age)
            if not max_age or func not in self.cached_function_responses or (datetime.now() - self.cached_function_responses[func]['fetch_time'] > max_age):
                if 'max_age' in kwargs:
                    del kwargs['max_age']
                res = func(*args, **kwargs)
                self.cached_function_responses[func] = {'data': res, 'fetch_time': datetime.now()}
            return self.cached_function_responses[func]['data']
        return inner


@cached(default_max_age=timedelta(minutes=30))
def fetch_weather():
    weather_code = os.getenv('WEATHER_CODE') or 2757345
    url = f'https://forecast.buienradar.nl/2.0/forecast/{weather_code}'
    r = requests.get(url)
    data = []
    for index, day in enumerate(r.json()['days']):
        if index == 4:
            break
        data.append({
            'iconcode': day['iconcode'],
            'maxtemp': day['maxtemp'],
            'mintemp': day['mintemp'],
            'precipitation': day['precipitation'],
        })
    return data


@app.route('/')
def weather():
    return jsonify(fetch_weather())


if __name__ == "__main__":
    app.run()
