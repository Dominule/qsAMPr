import requests

"""
Download json data from DBAASP database
"""

amp_id_list = [10, 57, 103]
json_list = []
default_adress = "https://dbaasp.org/peptides/"

for amp_id in amp_id_list:
    actual_adress = default_adress + str(amp_id)
    json_peptide_information = requests.get(actual_adress)
    json_list.append(json_peptide_information)
    print(f"Response: {json_peptide_information.json()}")

print(f"Json_list:\n {json_list}\n\n")