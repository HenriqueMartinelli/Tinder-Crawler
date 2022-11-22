# import keyboard
import logging


def start_function(self):
    loop = True
    qnt_falhas = 0
    while loop:

        try:
            _json = self.buscar_json()

        except Exception as e:
            logging.warning(str(e))
            raise e

        try:
            dados = self.extrair_dados(_json)
            if dados:
                self.salvar(dados)
        except Exception as e:
            qnt_falhas += 1
            logging.error('ERRO AO EXTRAIR OS DADOS - ' + str(e))
        
        if qnt_falhas:
            logging.warning(f'Total de Falhas: {qnt_falhas}')
            lopp = False

        if qnt_falhas > 10:
            input('Falha Geral no Bot, recomendado a salvar o arquivo log')
            loop = False

