import pandas as pd
import peptides

"""
Compute probability of each aminoacid and store dataframe
"""

def get_data():
    # load sequences
    sequences = []
    positive_df = pd.read_csv("../../data/inputs/descriptors_positive_staphylococcus.csv")
    for i in range(positive_df["SEQUENCE"].shape[0]):
        sequences.append(positive_df["SEQUENCE"][i])
    return sequences

def get_frequencies():
    sequences = get_data()

    # compute frequencies
    frequencies_list_of_dicts = []
    for seq in sequences:
        peptide = peptides.Peptide(seq)
        frequencies_list_of_dicts.append(peptide.frequencies())

    # compute average frequencies to dictionary
    averages = {}
    length = len(frequencies_list_of_dicts)
    aa = ["A", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "Y"]
    for a in aa:
        sum = 0
        for f in frequencies_list_of_dicts:
            sum += f[a]
        average_frequency = sum / length
        averages[a] = average_frequency
    return averages

def get_min_length():
    sequences = get_data()
    min_length = len(sequences[0])
    for seq in sequences:
        if len(seq) < min_length:
            min_length = len(seq)
    return min_length

def get_max_length():
    sequences = get_data()
    max_length = len(sequences[0])
    for seq in sequences:
        if len(seq) > max_length:
            max_length = len(seq)
    return max_length
