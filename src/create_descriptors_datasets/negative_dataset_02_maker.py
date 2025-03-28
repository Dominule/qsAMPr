import pandas as pd
import peptides

"""
Create negative dataset -02- random real sequences (UniProt from AntiTbPred)
"""

path_source_fir = "../../data/samples_negative_SwissProt/negative_peptides"
path_source_sec = "../../data/samples_amPEPpy/peptides_nonAMPs_amPEPpy.csv"
path_store = "../../data/inputs/descriptors_negative_02_dataset.csv"
new_activity = 10000
number_to_keep = 218

# Load data
negative_fir_df = pd.read_csv(path_source_fir)
negative_sec_df = pd.read_csv(path_source_sec)
print(negative_fir_df.shape)
print(negative_sec_df.shape)


negative_fir_df.columns = ['SEQUENCE']
negative_sec_df.columns = ['SEQUENCE']
negative_fir_df["ACTIVITY"] = new_activity
negative_sec_df["ACTIVITY"] = new_activity
# filter sequences
negative_sec_df = negative_sec_df[negative_sec_df["SEQUENCE"].str.len() <= 100]
# keep random 200 sequences from negative_sec_df --> together cca 450 sequences
negative_sec_df = negative_sec_df.sample(n=number_to_keep, random_state=42)
print(negative_sec_df.shape)
negative_df = pd.concat([negative_fir_df, negative_sec_df], ignore_index=True)
print(negative_df.shape)


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
