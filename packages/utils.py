from packages.model import DataEntry

import json

def saveToJson(data : DataEntry, json_path : str):
    data_dict : dict = data.__dict__
    with open(json_path, 'r') as file:
        data = json.load(file)

    data['data'].append(data_dict)

    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)



