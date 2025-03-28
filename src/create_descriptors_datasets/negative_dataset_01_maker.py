import pandas as pd
import peptides

"""
Create negative dataset -01- staphylococcus inactive + gram negative bacteria active peptides (DBAASP)
"""

path_source_fir = "../../data/samples_DBAASP/peptides_staphylococcus_inactive.csv"
path_source_sec = "../../data/samples_DBAASP/peptides_gram_negative_bacteria_active.csv"
path_store = "../../data/inputs/descriptors_negative_01_dataset.csv"
negatives_to_keep = 224     # number of negative sequences from gram negative to keep

# Load peptides_staphylococcus_active.csv
negative_fir_df = pd.read_csv(path_source_fir)
negative_sec_df = pd.read_csv(path_source_sec)
negative_sec_df.dropna(axis=1, how='all')
print(negative_fir_df.shape)
print(negative_sec_df.shape)

# keep random 200 sequences from negative_sec_df --> together cca 500 sequences, set the activity
negative_sec_df = negative_sec_df.sample(n=negatives_to_keep, random_state=42)
negative_fir_df.columns = ['SEQUENCE', 'ACTIVITY']
negative_sec_df.columns = ['SEQUENCE']
max_activity = negative_fir_df["ACTIVITY"].max()
negative_sec_df["ACTIVITY"] = max_activity

# concat the two dataframes
negative_df = pd.concat([negative_fir_df, negative_sec_df], ignore_index=True)
print(negative_df)

# Create a DataFrame of lists with the descriptors for each peptide
descriptors_list_list = []
for i in range(negative_df.shape[0]):
    sequence = negative_df.iloc[i,0]
    activity = negative_df.iloc[i,1]
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