# Generate 100 sequences of length from 12 to 56 AA
import random

minLength = 12
maxLength = 56

def get_peptides():
    peptides = []
    for i in range(100):
        length = random.randint(minLength, maxLength)
        sequence = ''.join(random.choices('ACDEFGHIKLMNPQRSTVWY', k=length))
        peptides.append(sequence)
    return peptides
