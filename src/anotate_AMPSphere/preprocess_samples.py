"""
Check if there are duplicate entries in the AMPSphere sample list and in our regression dataset.
Compute descriptors.
Store ampsphere samples in a separate file.
"""
import pandas as pd
import peptides

storage_path = "../../data/inputs/samples_AMPSphere/AMPs_all_preprocessed.csv"

# load the ampsphere samples
ampsphere_samples = pd.read_csv("../../data/inputs/samples_AMPSphere/AMP_all.csv", delimiter='\t')
# load the main samples (regression dataset, staphylococcus)
main_samples = pd.read_csv("../../data/inputs/samples_DBAASP/reg_staphylococcus_MICs.csv")

# print("Main samples:")
# print(ampsphere_samples.shape)
# print(main_samples.columns)
# print(main_samples.head())

# list main_sequences
main_sequences = []
for i in range(len(main_samples)):
    main_sequences.append(main_samples.iloc[i, 0])

# list amps_sequences
amps_sequences = []
for i in range(len(ampsphere_samples)):
    amps_sequences.append(ampsphere_samples.iloc[i, 1])


# check duplicates
# duplicates = []
# for i in range(len(main_sequences)):
#     if main_sequences[i] in amps_sequences:
#         duplicates.append(main_sequences[i])
# print("Duplicates - length:")
# print(len(duplicates))
# print(duplicates)


# compute descriptors
descriptors_list_list = []
for i in range(len(amps_sequences)):
    sequence = amps_sequences[i]

    # create row
    row_dict = {"SEQUENCE": sequence,
                "FAMILY": ampsphere_samples.iloc[i, 2],
                "ANTIFAM": ampsphere_samples.iloc[i, 10],
                "RNACODE": ampsphere_samples.iloc[i, 11],
                "METAPROTEOMES": ampsphere_samples.iloc[i, 12],
                "METATRANSCRIPTOMES": ampsphere_samples.iloc[i, 13],
                "COORDINATES": ampsphere_samples.iloc[i, 14]}
    descriptors = peptides.Peptide(sequence).descriptors()  # compute descriptors
    row_dict.update(descriptors)
    # add row
    descriptors_list_list.append(row_dict)
descriptors_df = pd.DataFrame(descriptors_list_list)

# store into csv
descriptors_df.to_csv(storage_path, index=False)
