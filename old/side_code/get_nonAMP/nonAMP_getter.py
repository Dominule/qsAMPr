import pandas as pd

# read fasta sequences to list
sequences = []
with open("../../../data/samples_amPEPpy/nonAMPs_amPEPpy.fasta") as f:
    for line in f:
        if line.startswith('>'):
            continue
        sequences.append(line.strip())

# store to csv
df = pd.DataFrame(sequences, columns=["SEQUENCE"])
df.to_csv("../../../data/samples_amPEPpy/peptides_nonAMPs_amPEPpy.csv", index=False)

