import pickle

import pandas as pd

from src.classification.models import RFCModel

"""
Predict activity of AMPSphere samples using a trained model.
"""

prediction_storage_folder = "../../data/outputs/predictions/ampsphere_100_samples.tsv"

model_path_01 = "../../data/outputs/dataset01/evaluation_all/RFC/model.pkl"
model_path_02 = "../../data/outputs/dataset02/evaluation_all/RFC/model.pkl"
model_path_03 = "../../data/outputs/dataset03/evaluation_all/RFC/model.pkl"
samples_to_predict_path = "../../data/samples_AMPSphere/ampsphere_descriptors.csv"

# load samples
samples_to_predict = pd.read_csv(samples_to_predict_path)
sequences = samples_to_predict['SEQUENCE']
samples_to_predict = samples_to_predict.drop(columns=['SEQUENCE'])

# load model - classifier
with open(model_path_01, 'rb') as file:
    loaded_classifier_01: RFCModel = pickle.load(file)
with open(model_path_02, 'rb') as file:
    loaded_classifier_02: RFCModel = pickle.load(file)
with open(model_path_03, 'rb') as file:
    loaded_classifier_03: RFCModel = pickle.load(file)


# Use the loaded model to make predictions on new data
predictions01 = loaded_classifier_01.predict_proba(samples_to_predict)
predictions02 = loaded_classifier_02.predict_proba(samples_to_predict)
predictions03 = loaded_classifier_03.predict_proba(samples_to_predict)


# make dataframe from sequence, predictions
predictions_df = pd.DataFrame({
    'SEQUENCE': sequences,
    'PREDICTION_01': predictions01[:,1],
    'PREDICTION_02': predictions02[:,1],
    'PREDICTION_03': predictions03[:,1]
})

# # store predictions
predictions_df.to_csv(prediction_storage_folder, index=False, sep='\t', decimal=',')