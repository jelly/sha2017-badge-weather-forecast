#1/usr/bin/python

import json
import requests

def main():
    url = 'https://forecast.buienradar.nl/2.0/forecast/2757345'
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
    with open('/home/jelle/public_html/weather.json', 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()
