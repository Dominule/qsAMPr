import peptides
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split

from src.classification.models import RFCModel

"""
Train_test_split on all three datasets.
Get test set for AMPSPhere annotation.
Compute descriptors.
Store test samples in a separate file.
"""

# descriptors_storage_path = "../../data/inputs/test_preprocessed_sequences_classfication.csv"
prediction_storage_folder = "../../data/outputs/predictions/tested_classifiers_for_AMPSphere.tsv"


# load the test samples
df_test_01 = pd.read_csv('../../data/outputs/dataset01/evaluation_all/test_set_classification.csv')
df_test_02 = pd.read_csv('../../data/outputs/dataset02/evaluation_all/test_set_classification.csv')
df_test_03 = pd.read_csv('../../data/outputs/dataset03/evaluation_all/test_set_classification.csv')

# remove all with ACTIVITY=1 from df_test_02 and df_test_03, sort df_test_01
df_test_01 = df_test_01.sort_values(by=['ACTIVITY'], ascending=False)
df_test_02 = df_test_02[df_test_02['ACTIVITY'] == 0]
df_test_03 = df_test_03[df_test_03['ACTIVITY'] == 0]

# concat all
df = pd.concat([df_test_01, df_test_02, df_test_03])
test_sequences = list(df['SEQUENCE'])
test_activities = list(df['ACTIVITY'])

# compute descriptors
descriptors_list_list = []
for i in range(len(test_sequences)):
    sequence = test_sequences[i]

    # create row
    row_dict = {}
    descriptors = peptides.Peptide(sequence).descriptors()  # compute descriptors
    row_dict.update(descriptors)
    # add row
    descriptors_list_list.append(row_dict)
descriptors_df = pd.DataFrame(descriptors_list_list)


# predict activity of test samples using a trained models

# load the models
model_path_01 = "../../data/outputs/dataset01/evaluation_all/RFC/model.pkl"
model_path_02 = "../../data/outputs/dataset02/evaluation_all/RFC/model.pkl"
model_path_03 = "../../data/outputs/dataset03/evaluation_all/RFC/model.pkl"
with open(model_path_01, 'rb') as file:
    loaded_classifier_01: RFCModel = pickle.load(file)
with open(model_path_02, 'rb') as file:
    loaded_classifier_02: RFCModel = pickle.load(file)
with open(model_path_03, 'rb') as file:
    loaded_classifier_03: RFCModel = pickle.load(file)


# predict on test samples
predictions01 = loaded_classifier_01.predict_proba(descriptors_df)
predictions02 = loaded_classifier_02.predict_proba(descriptors_df)
predictions03 = loaded_classifier_03.predict_proba(descriptors_df)


# make dataframe from sequence, predictions
predictions_df = pd.DataFrame({
    'SEQUENCE': test_sequences,
    'PREDICTION_01': predictions01[:,1],
    'PREDICTION_02': predictions02[:,1],
    'PREDICTION_03': predictions03[:,1],
    'ACTIVITY': test_activities
})

# store predictions
predictions_df.to_csv(prediction_storage_folder, index=False, sep='\t', decimal=',')
