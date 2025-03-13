import csv

"""
Open raw data and save just interesting columns (sequence and MIC value) to csv file
Create a csv file with just the peptide sequences
"""

peptide_sequences = []
peptide_MIC_values = []
with open("../../data/samples_DBAASP/raw_dbaasp_staphylococcus_without_modifications.csv") as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        peptide_sequences.append(row[4])
        peptide_MIC_values.append(row[6])

# for model training create csv from sequences and MIC values
output_csv = "../data/samples_DBAASP/positive_peptides_without_modifications.csv"
with open(output_csv, "w") as file:
    writer = csv.writer(file, delimiter=",")
    for i in range(len(peptide_sequences)):
        writer.writerow([peptide_sequences[i], peptide_MIC_values[i]])

# for exploration analysis create fasta from sequences
output_fasta = "../data/samples_DBAASP/sequences_staphylococcus_DBAASP.fasta"
with open (output_fasta, "w") as file:
    for i in range(len(peptide_sequences)):
        if i == 0:
            continue
        line = ">AMP_staphylococcus_" + str(i) + "\n" + peptide_sequences[i] + "\n"
        file.write(line)

