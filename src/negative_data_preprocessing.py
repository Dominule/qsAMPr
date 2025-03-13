import peptides
import pandas as pd
import peptide_generator

# with open("../data/samples_negative_SwissProt/negative_peptides") as f:
#     # readlines without \n
#     negative_peptides = f.read().splitlines()
# print(negative_peptides[:5])
negative_peptides = peptide_generator.get_peptides(100)

decsriptors_list_list = []
for i in range(len(negative_peptides)):
    print(negative_peptides[i])
    peptide = peptides.Peptide(negative_peptides[i])
    decsriptors_list_list.append(peptide.descriptors())
descriptors_negatives_df = pd.DataFrame(decsriptors_list_list)

descriptors_negatives_df.to_csv("../data/samples_negative_generated/descriptors_negative_generated_100.csv", index=False)