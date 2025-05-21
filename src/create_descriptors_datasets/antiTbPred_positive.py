import numpy as np
import pandas as pd
import peptides

"""
Create one positive dataset with mycobacterium tuberculosis active peptides from AntiTbPred article
"""

path_source = "../../data/inputs/samples_AntiTbPred/positive_tb.csv"
path_store = "../../data/inputs/descriptors_positive_tuberculosis.csv"


# Load sequences
df = np.loadtxt(path_source, delimiter = ',', dtype=str)
sequences = df[:].tolist()

# Create a DataFrame of lists with the descriptors for each peptide
descriptors_list_list = []
for i in range(len(sequences)):
    activity = 1
    descriptors = peptides.Peptide(sequences[i]).descriptors()  # compute descriptors

    # create row
    row_dict = {"SEQUENCE": sequences[i]}
    row_dict.update(descriptors)
    row_dict.update({"ACTIVITY": activity})
    # add row
    descriptors_list_list.append(row_dict)
descriptors_positives_df = pd.DataFrame(descriptors_list_list)

# Save the DataFrames to a CSV file
descriptors_positives_df.to_csv(path_store, index=False)
