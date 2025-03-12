# Generate 100 sequences of length from 12 to 56 AA
import random
import aminoacid_probability

minLength = aminoacid_probability.get_min_length()
maxLength = aminoacid_probability.get_max_length()
frequencies = aminoacid_probability.get_frequencies()

def get_peptides(number_of_sequencies):
    peptides = []
    for i in range(number_of_sequencies):
        length = random.randint(minLength, maxLength)
        peptide = ""
        for j in range(length):
            aminoacid = random.choices(list(frequencies.keys()), weights=list(frequencies.values()))[0]
            peptide += aminoacid
        peptides.append(peptide)
        print(peptide)
    return peptides

get_peptides(10)