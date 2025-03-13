import pandas as pd
import peptides
import peptide_generator

"""
Create negative dataset -03- random generated sequences
(with the same amino acid distribution as the positive dataset)
"""

path_store = "../../data/inputs/descriptors_negative_03_dataset.csv"
new_activity = 10000
number_of_peptides_generated = 443

# Generate peptides
negative_list = peptide_generator.get_peptides(number_of_peptides_generated)

# Create a DataFrame of lists with the descriptors for each peptide
descriptors_list_list = []
for i in range(len(negative_list)):
    sequence = negative_list[i]
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
