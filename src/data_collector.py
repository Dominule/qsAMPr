import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors
from peptide_generator import get_peptides


'''
Create a dataframe with molecular descriptors for a list of peptides
'''


# Read the positive peptides from the CSV file, generate negative peptides
df_peptides = pd.read_csv('../data/examples/peptides.csv', delimiter=';')
list_of_positives = df_peptides['peptide'].tolist()
list_of_negatives = get_peptides()


# Check if the negative peptides are in the positive peptides list
for pep in list_of_negatives:
    if pep in list_of_positives:
        print("Negative peptide is in the positive peptides list")
# TODO: rewrite, regenerate negative peptides if they are in the positive list


# Convert the AA sequences to RDKit molecules
mols_positives = [Chem.MolFromSequence(peptide) for peptide in list_of_positives]
mols_negatives = [Chem.MolFromSequence(peptide) for peptide in list_of_negatives]


# Calculate the molecular descriptors
# TODO: use MorganGenerator instead
descriptors_of_positives = []
descriptors_of_negatives = []
for mol in mols_positives:
    mol_descriptors = Descriptors.CalcMolDescriptors(mol)
    descriptors_of_positives.append(mol_descriptors)
for mol in mols_negatives:
    molDesriptors = Descriptors.CalcMolDescriptors(mol)
    descriptors_of_negatives.append(molDesriptors)



# Create a pandas DataFrame from the list of peptide descriptors
df_positives = pd.DataFrame.from_dict(descriptors_of_positives)
df_negatives = pd.DataFrame.from_dict(descriptors_of_negatives)

# assign antibios boolean property
df_positives['antibios'] = True
df_negatives['antibios'] = False

# Merge the positive and negative DataFrames
df_descriptors = pd.concat([df_positives, df_negatives], ignore_index=True)
# TODO: why ignore_index???


# Save the DataFrames to a CSV file
df_positives.to_csv('../data/examples/positive_peptides_descriptors.csv', index=False)
df_negatives.to_csv('../data/examples/negative_peptides_descriptors.csv', index=False)
df_descriptors.to_csv('../data/examples/peptides_descriptors.csv', index=False)





