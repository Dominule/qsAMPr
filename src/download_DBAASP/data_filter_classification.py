import json
from mic_analyser import is_active, get_float, contains_only_digits
"""
Filter json raw data to get only the necessary information,
divide between active and inactive peptides,
store the results in csv
"""

path_source = "../../data/samples_DBAASP/raw_data_staphylococcus_from_DBAASP.json"   # path to json file
path_active = "../../data/samples_DBAASP/peptides_staphylococcus_active.csv"        # path to store active peptides
path_inactive = "../../data/samples_DBAASP/peptides_staphylococcus_inactive.csv"    # path to store inactive peptides
#path_gram_negative = "../../data/samples_DBAASP/peptides_gram_negative_bacteria_active.csv"
bacteria = "Staphylococcus aureus"      # target bacteria
method = "MIC"              # Minimal Inhibitory Concentration
mic_threshold = 100         # less than this value is considered active
new_mic_for_inactive = 100


with open(path_source) as f:
    raw = json.load(f)  # list of json dicts


only_digits = 0
unique_sequences = []
mic_value_average_positive = 0
mic_value_average_negative = 0
positive_dict = {}
negative_dict = {}

for peptide in raw:
    # gram_negative_list.append(peptide["sequence"])
    for feature in peptide:
        if feature == 'targetActivities':
            for target in peptide[feature]:
                if target['targetSpecies']['name'] == bacteria:
                    if target["activityMeasureGroup"] != None:
                        if target["activityMeasureGroup"]["name"] == method:
                            sequence = peptide["sequence"]
                            mic = target["concentration"]

                            if (is_active(mic, mic_threshold)):
                                # positive peptide
                                if sequence in unique_sequences:
                                    print("Duplicate :(")
                                else:
                                    unique_sequences.append(sequence)
                                    mic_value = get_float(target["concentration"])
                                    mic_value_average_positive += mic_value
                                    positive_dict[sequence] = mic_value
                            else:
                                # negative peptide
                                if sequence in unique_sequences:
                                    print("Duplicate :(")
                                else:
                                    unique_sequences.append(sequence)
                                    mic_value = get_float(target["concentration"])
                                    mic_value_average_negative += mic_value
                                    if (mic_value < new_mic_for_inactive):
                                        mic_value = new_mic_for_inactive
                                    negative_dict[sequence] = mic_value

print(f"Number of unique peptides: {len(unique_sequences)}")
print(f"Number of stored peptides: {len(positive_dict) + len(negative_dict)}")
print(f"Number of peptides inactive against {bacteria}: {len(negative_dict)}")
# print(f"Average MIC in negative samples: {mic_value_average_negative/len(negative_dict)}")
print(f"Number of peptides active against {bacteria}: {len(positive_dict)}")
# print(f"Average MIC in positive samples: {mic_value_average_positive/len(positive_dict)}")


# store the results in csv
with open(path_active, 'w') as file:
    for key in positive_dict.keys():
        file.write("%s,%s\n"%(key, positive_dict[key]))

with open(path_inactive, 'w') as file:
    for key in negative_dict.keys():
        file.write("%s,%s\n"%(key, negative_dict[key]))


# store unique_sequences of peptides active against gram negative bacteria
# with open(path_gram_negative, 'w') as file:
#     for sequence in gram_negative_list:
#         file.write(f"{sequence}\n")