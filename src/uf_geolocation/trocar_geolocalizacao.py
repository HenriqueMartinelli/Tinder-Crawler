import logging
import requests

def trocar_geolocalizacao(self, lat, long):

    headers = {
            'x-auth-token': self.AUTH_TOKEN,
            }

    json_data = {
        'lat': lat,
        'lon': long,
        }

    passport = requests.request('POST', self.URL_PASSPORT, headers=headers, json=json_data, timeout=10)
    print(passport)
    if passport.status_code != 200:
        logging.error('Falha ao trocar de UF')
        input('Falha ao trocar de UF')
        exit()