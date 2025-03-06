import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors


'''
Create a dataframe with molecular descriptors for a list of peptides
'''


# Read the positive peptides from the CSV file to dataframe
positive_df = pd.read_csv("../data/examples_DBAASP/positive_peptides_without_modifications.csv")


# Convert the AA sequences to RDKit molecules
#mols_positives = [Chem.MolFromSequence(peptide) for peptide in positive_df['SEQUENCE']]


# Calculate the molecular descriptors
# # TODO: use MorganGenerator instead
# descriptors_positives_list = []
# for mol in range(len(mols_positives)):
#     mol_descriptors = Descriptors.CalcMolDescriptors(mol)
#     descriptors_positives_list.append(mol_descriptors)


# Create a pandas DataFrame from the list of peptide descriptors
#descriptors_positives_df = pd.DataFrame.from_dict(descriptors_positives_list)

# Save the DataFrames to a CSV file
#descriptors_positives_df.to_csv('../data/examples_DBAASP/descriptors_positive_staphylococcus.csv', index=False)






