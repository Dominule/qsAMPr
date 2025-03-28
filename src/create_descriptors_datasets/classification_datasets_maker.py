# load datasets
import pandas as pd
import numpy as np

"""
Transform regression datasets into classification datasets (activity - 0,1)
"""

# positive
df_pos = pd.read_csv('../../data/inputs/descriptors_positive_staphylococcus.csv')
# negative against staphylococcus but amps
df_neg_01 = pd.read_csv('../../data/inputs/descriptors_negative_01_dataset.csv')
# negative - real peptides
df_neg_02 = pd.read_csv('../../data/inputs/descriptors_negative_02_dataset.csv')
# negative - random peptides
df_neg_03 = pd.read_csv('../../data/inputs/descriptors_negative_03_dataset.csv')


# get overview
# print(df_pos['ACTIVITY'].describe())
# print(df_neg_01['ACTIVITY'].describe())
# print(df_neg_02['ACTIVITY'].describe())
# print(df_neg_03['ACTIVITY'].describe())


# replace all values in "ACTIVITY" column to 1
df_pos['ACTIVITY'] = 1
df_neg_01['ACTIVITY'] = 0
df_neg_02['ACTIVITY'] = 0
df_neg_03['ACTIVITY'] = 0

# store the datasets
df_pos.to_csv('../../data/inputs/clf_descriptors_positive_staphylococcus.csv', index=False)
df_neg_01.to_csv('../../data/inputs/clf_descriptors_negative_01_dataset.csv', index=False)
df_neg_02.to_csv('../../data/inputs/clf_descriptors_negative_02_dataset.csv', index=False)
df_neg_03.to_csv('../../data/inputs/clf_descriptors_negative_03_dataset.csv', index=False)