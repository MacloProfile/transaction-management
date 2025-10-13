import requests

from local_settings import YANDEX_API_KEY


def get_geocode(address: str):
    if not address:
        return None

    url = 'https://geocode-maps.yandex.ru/1.x/'
    params = {
        'geocode': address,
        'apikey': YANDEX_API_KEY,
        'format': 'json'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        try:
            pos = response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            lon, lat = map(float, pos.split())
            return [lat, lon]
        except (IndexError, KeyError):
            return None
    return None
