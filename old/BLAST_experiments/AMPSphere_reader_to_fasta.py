import csv

"""
AMPSphere --> fasta for exploration analysis
"""

input_file = "../../data/samples_AMPSphere/AMP_peptides_100.csv"
output_file = "../data/samples_AMPSphere/sequences_AMPSphere.fasta"


peptide_sequences = []
with open(input_file) as file:
    reader = csv.reader(file, delimiter=";")
    for row in reader:
        peptide_sequences.append(row[1])

peptide_sequences.pop(0)

with open (output_file, "w") as file:
    for i in range(len(peptide_sequences)):
        line = ">AMP_AMPSphere_" + str(i) + "\n" + peptide_sequences[i] + "\n"
        file.write(line)