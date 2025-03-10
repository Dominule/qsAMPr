import csv

"""
AMPSphere --> fasta for exploration analysis
"""

peptide_sequences = []
with open("../data/examples_AMPSphere/AMP_peptides_100.csv") as file:
    reader = csv.reader(file, delimiter=";")
    for row in reader:
        peptide_sequences.append(row[1])

peptide_sequences.pop(0)

output_fasta = "../data/examples_AMPSphere/sequences_AMPSphere.fasta"
with open (output_fasta, "w") as file:
    for i in range(len(peptide_sequences)):
        line = ">AMP_AMPSphere_" + str(i) + "\n" + peptide_sequences[i] + "\n"
        file.write(line)