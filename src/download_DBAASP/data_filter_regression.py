import json
from src.download_DBAASP.mic_analyser import is_active, get_float, contains_only_digits

"""
Filter json raw data to get only the exact value of the MIC,
store the results in csv
"""

path_source = "../../data/inputs/samples_DBAASP/raw_data_staphylococcus_from_DBAASP.json"  # path to json file
path_store = "../../data/inputs/samples_DBAASP/reg_staphylococcus_MICs.csv"  # path to store peptides


bacteria = "Staphylococcus aureus"      # target bacteria
method = "MIC"          # Minimal Inhibitory Concentration
range_threshold = 5         # if mic contains "-" --> threshold for the range of MIC values
mic_threshold = 100         # greater than this value will not be stored

only_digits = 0
unique_sequences = []
regression_dict = {}

with open(path_source) as f:
    raw = json.load(f)

for peptide in raw:
    for feature in peptide:
        if feature == 'targetActivities':
            for target in peptide[feature]:
                if target['targetSpecies']['name'] == bacteria:
                    if target["activityMeasureGroup"] != None:
                        if target["activityMeasureGroup"]["name"] == method:
                            sequence = peptide["sequence"]
                            mic = target["concentration"]
                            # we want mic to be exact value (or very small range)
                            if (contains_only_digits(mic, range_threshold)):
                                only_digits += 1
                                if get_float(mic) <= mic_threshold:
                                    if sequence in unique_sequences:
                                        print("Duplicate :(")
                                    else:
                                        unique_sequences.append(sequence)
                                        regression_dict[sequence] = get_float(mic)
                                else:
                                    print(f"MIC value too high: {mic}")

print(f"Number of unique peptides: {len(unique_sequences)}")
print(f"Number of peptides with only digits: {only_digits}")
print(f"Number of stored peptides: {len(regression_dict)}")

# store the results in csv
with open(path_store, 'w') as file:
    for key in regression_dict.keys():
        file.write("%s,%s\n"%(key, regression_dict[key]))