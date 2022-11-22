import json

def dict_uf(idx):
    escolha = {'1': 'BR-RJ',
               '2': 'BR-SP',
               '3': 'BR-MG'}[idx]

    f = open('map.json')
    map = json.load(f)
    
    for uf in map:
        if uf.get('-id') == escolha:
            return uf
