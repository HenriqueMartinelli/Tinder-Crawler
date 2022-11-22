import requests
import logging
import logging.handlers
import sys
import datetime
from datetime import date 

from src.utils.salvar import salvar_csv
from src.utils.start import start_function
from src.uf_geolocation.trocar_geolocalizacao import trocar_geolocalizacao
from src.utils.negativar_ids import negativar_ids
from src.sep_interesses.sep_interesses import sep_interesses
from src.utils.dict_uf import dict_uf
from src.utils.calcular_idade import calcular_idade


date_  = str(datetime.datetime.now()).replace(':', '_')
FILE_PATH = 'log/log_bot_' + date_

file_handler = logging.FileHandler(FILE_PATH)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        file_handler,
        console_handler
    ]
)

class Crawler():

    def __exit__(self, type, value, traceback):
        pass
    
    def __enter__(self):
        self.AUTH_TOKEN = input("Passe o Token de Autenticacao:").strip()
        self.FILE_PATH = input("Informe no do arquivo csv:").strip()

        escolha = str
        while escolha not in ('1', '2', '3'):
            escolha = input('Escolha o estado desejado:\n1 - Rio de Janeiro\n2 - São Paulo\n3 - Minas Gerais\nNúmero:').strip()
        
        uf = dict_uf(escolha)
        
        lat, long, self.UF = uf.get('-lat'), uf.get('-long'), uf.get('-title'), 
        trocar_geolocalizacao(self, lat, long)
        

        return self



    def buscar_json(self):
        logging.info('Buscar json')

        self.headers = {
            'x-auth-token': self.AUTH_TOKEN,
            }

        json_group = requests.request('GET', self.URL_API, headers=self.headers, timeout=10).json()
        if 'RATE_LIMITED' in str(json_group):
            logging.warning('RATE_LIMITED ATINGIDO')
            input('LIMITE DA CONTA ATIGINDO, TENTE APÓS 24H')
            exit()

        return json_group
            


    def extrair_dados(self, json_group):
        logging.info('Extrair Dados')
        dados = list()
        resultList = json_group['data']['results']
        
        for result in resultList:
            data = dict()
            results = result['user']

            try: emprego = results.get('jobs')[0]['title']['name'] if results.get('jobs') != [] else ''
            except: emprego = results.get('jobs')[0]['company']['name'] if results.get('jobs') != [] else ''

            infos = {
                    'ID_USER': results.get('_id'),
                    'Nome': results.get('name', ''), 
                    'Empregos': emprego,
                    'Idade': int(results.get('birth_date', '').split('T')[0].split('-')[0]),
                    'Educação': results.get('schools')[0]['name'] if results.get('schools') else '',
                    'Cidade': results.get('city')['name'] if results.get('city') else '',
                    'Perfil': results.get('bio', '')    
                }
                
            
            if 'selected_descriptors' in result['user']:
                for desc in result['user']['selected_descriptors']: 
                    infos.update({
                        desc['name']: desc['choice_selections'][0]['name']
                    })

            if 'experiment_info' in result:
                listnterests = [item['name'] for item in result['experiment_info']['user_interests']['selected_interests']]
            else: listnterests = []
            
            data["ID_USER"] = infos['ID_USER']
            data["Nome"] = infos['Nome']
            data["Empregos"] = infos['Empregos']
            data["Educação"] = infos['Educação']
            data["Cidade"] = infos['Cidade']
            data['Geolocation'] = self.UF
            data["Idade"] = calcular_idade(date(infos.get('Idade'), 1, 1)) if infos.get('Idade') != '' else ''
            data["Zodiac"] = infos.get('Zodiac', '')
            data["Communication Style"] = infos.get('Communication Style', '')
            data["Pets"] = infos.get('Pets', '')
            data["Drink of Choice"] = infos.get('Drink of Choice', '')
            data["Dietary Preference"] = infos.get('Dietary Preference', '')
            data["Smoking"] = infos.get('Smoking', '')
            data["Social Media"] = infos.get('Social Media', '')
            data["Education"] = infos.get('Education', '')
            data["Workout"] = infos.get('Workout', '')
            data["Perfil"] = infos.get('Perfil')
            data["MBTI"] = infos.get('MBTI', '')
            sep_interesses(data, listnterests)
            
            negativar_ids(self, result['s_number'], results.get('_id'))
        
            dados.append(data) 


        return dados     


    def start(self):
        return start_function(self)


    def salvar(self, valor):
        return salvar_csv(self, valor)
            

class Tinder(Crawler):
    def __init__(self):
        self.URL_BASE = 'https://api.gotinder.com'
        self.URL_API = self.URL_BASE + '/v2/recs/core?locale=pt'
        self.URL_PASSPORT = self.URL_BASE + '/passport/user/travel?locale=pt'
        self.URL_PASS = self.URL_BASE + '/pass/'

with Tinder() as t:
    t.start() 