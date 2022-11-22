import json

def sep_interesses(data, interesses):
    f = open('interesses.json')
    json_ = json.load(f)
    del json_['Social Media']
    
    dic = dict()
    for key in json_.keys():
        for item in interesses:
            if item.strip() == key: 
                dic.update({key: 1})

    data.update(json_)
    if dic != {}: 
        data.update(dic)

