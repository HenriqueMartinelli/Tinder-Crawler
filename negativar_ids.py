import logging
import requests

def negativar_ids(self, s_number, _id):

    headers = {
        'origin': 'https://tinder.com',
        'referer': 'https://tinder.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }

    params = {
        'locale': 'pt',
        's_number': s_number,

    }
    try:
        requests.request('OPTIONS',self.URL_PASS + _id, params=params, headers=headers, timeout=2)

        headers.update({
            'x-auth-token': self.AUTH_TOKEN,
        })

        requests.request('GET', self.URL_PASS + _id, params=params, headers=headers, timeout=2)
    except: 
        logging.info('Erro ao excluir Id')
        return False