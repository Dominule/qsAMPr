import pandas as pd
import peptides

"""
Create negative dataset -02- random real sequences (UniProt from AntiTbPred)
"""

path_source = "../../data/samples_negative_SwissProt/negative_peptides"
path_store = "../../data/inputs/descriptors_negative_02_dataset.csv"
new_activity = 10000

# Load data
negative_df = pd.read_csv(path_source)

# Create a DataFrame of lists with the descriptors for each peptide
descriptors_list_list = []
for i in range(negative_df.shape[0]):
    sequence = negative_df.iloc[i,0]
    activity = new_activity
    # create row
    row_dict = {"SEQUENCE": sequence}
    descriptors = peptides.Peptide(sequence).descriptors()  # compute descriptors
    row_dict.update(descriptors)
    row_dict.update({"ACTIVITY": activity})
    # add row
    descriptors_list_list.append(row_dict)
descriptors_positives_df = pd.DataFrame(descriptors_list_list)

# Save the DataFrames to a CSV file
descriptors_positives_df.to_csv(path_store, index=False)
