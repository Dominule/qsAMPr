import requests
import json
from negative_peptides_ids import get_peptide_ids

"""
Download json data from DBAASP database using REST API
"""

amp_id_list = get_peptide_ids()
#amp_id_list = ["10", "57", "103", "108"]        # for testing purposes
json_list = []
default_adress = "https://dbaasp.org/peptides/"

for amp_id in amp_id_list:
    actual_adress = default_adress + str(amp_id)
    json_peptide_information = requests.get(actual_adress).json()
    json_list.append(json_peptide_information)
    #print(f"Response: {json_peptide_information}\n\n")

#print(f"List of jsons: {json_list}")

with open('../data/examples_DBAASP/raw_data_from_DBAASP.json', 'w') as f:
    json.dump(json_list, f)
