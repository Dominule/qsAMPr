import pandas as pd
import peptides

"""
Create one positive dataset with staphylococcus active peptides (DBAASP)
"""

path_source = "../../data/samples_DBAASP/peptides_staphylococcus_active.csv"
path_store = "../../data/inputs/descriptors_positive_staphylococcus.csv"


# Load peptides_staphylococcus_active.csv
positive_df = pd.read_csv(path_source)

# Create a DataFrame of lists with the descriptors for each peptide
descriptors_list_list = []
for i in range(positive_df.shape[0]):
    sequence = positive_df.iloc[i,0]
    activity = positive_df.iloc[i,1]
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
