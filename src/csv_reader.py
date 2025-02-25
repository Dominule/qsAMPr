import csv

peptide_sequences = []
peptide_MIC_values = []
with open("../data/examples_DBAASP/raw_dbaasp_staphylococcus_without_modifications.csv") as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        peptide_sequences.append(row[4])
        peptide_MIC_values.append(row[6])

with open("../data/examples_DBAASP/positive_peptides_without_modifications.csv", "w") as file:
    writer = csv.writer(file, delimiter=",")
    for i in range(len(peptide_sequences)):
        writer.writerow([peptide_sequences[i], peptide_MIC_values[i]])

# add getter