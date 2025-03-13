import csv
import json
import requests
from ids_getter import get_positive_ids, get_raw, get_gram_negative_ids

"""
Download data to json from DBAASP
"""

storage_path = '../../data/samples_DBAASP/raw_data_gram_negative_from_DBAASP.json'
amp_id_list = get_gram_negative_ids()


#amp_id_list = ["10", "57", "103", "108"]        # for testing purposes
json_list = []
default_adress = "https://dbaasp.org/peptides/"


for amp_id in amp_id_list:
    print(amp_id)
    actual_adress = default_adress + str(amp_id)
    json_peptide_information = requests.get(actual_adress).json()
    json_list.append(json_peptide_information)


with open(storage_path, 'w') as f:
    json.dump(json_list, f)