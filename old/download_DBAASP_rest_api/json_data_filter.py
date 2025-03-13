import json
from integer_getter_from_range import get_float

"""
Filter json raw data to get only the necessary information,
"""

bacteria = "Staphylococcus aureus"      # target bacteria
method = "MIC"          # Minimal Inhibitory Concentration
with open('../data/samples_DBAASP/raw_data_staphylococcus_from_DBAASP.json') as f:
    raw = json.load(f)  # list of json dicts


#print(f"List of json dicts: {raw}")


# check if all peptides are active against the target bacteria
mic_value_average = 0
bad = 0
filtered = {}
for peptide in raw:
    for feature in peptide:
        if feature == 'targetActivities':
            for target in peptide[feature]:
                if target['targetSpecies']['name'] == bacteria:
                    if target["activityMeasureGroup"] != None:
                        if target["activityMeasureGroup"]["name"] == method:
                            sequence = peptide["sequence"]
                            mic_value = get_float(target["concentration"])
                            mic_value_average += mic_value
                            #print(f"ID: {peptide['id']} Sequence: {peptide['sequence']}")
                            print(f"MIC value: {mic_value}")



print(f"Number of peptides inactive against {bacteria}: {bad}")
