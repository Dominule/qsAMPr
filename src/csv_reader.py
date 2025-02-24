import csv

peptide_ids_list = []
with open("../data/examples_DBAASP/dbaasp_staphylococcus_peptide_ids.csv") as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        peptide_ids_list.append(row[0])

print(peptide_ids_list)