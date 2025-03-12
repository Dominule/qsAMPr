import peptides
import pandas as pd

with open("../data/examples_random_peptides_SwissProt/negative_peptides") as f:
    # readlines without \n
    negative_peptides = f.read().splitlines()
print(negative_peptides[:5])

decsriptors_list_list = []
for i in range(len(negative_peptides)):
    print(negative_peptides[i])
    peptide = peptides.Peptide(negative_peptides[i])
    decsriptors_list_list.append(peptide.pcp_descriptors())
descriptors_negatives_df = pd.DataFrame(decsriptors_list_list)

descriptors_negatives_df.to_csv("../data/examples_random_peptides_SwissProt/pcp_descriptors_negative.csv", index=False)