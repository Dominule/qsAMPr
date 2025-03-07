import pandas as pd
import peptides


'''
Create a dataframe with molecular descriptors for a list of peptides
'''


# Read the positive peptides from the CSV file to dataframe
positive_df = pd.read_csv("../data/examples_DBAASP/positive_peptides_without_modifications.csv")

# Create a DataFrame of lists with the descriptors for each peptide
descriptors_list_list = []
for i in range(positive_df.shape[0]):
    peptide = peptides.Peptide(positive_df.iloc[i,0])
    descriptors_list_list.append(peptide.pcp_descriptors())
descriptors_positives_df = pd.DataFrame(descriptors_list_list)


# Save the DataFrames to a CSV file
descriptors_positives_df.to_csv('../data/examples_DBAASP/descriptors_positive_staphylococcus.csv', index=False)






