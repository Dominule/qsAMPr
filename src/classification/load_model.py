import pickle
import pandas as pd
import src.classification.plot_model
import src.classification.models

"""
Predict activity of AMPSphere samples using a trained model.
"""

model_path_01 = "../../data/outputs/dataset01/evaluation_all/RFC/model.pkl"
model_path_02 = "../../data/outputs/dataset02/evaluation_all/RFC/model.pkl"
model_path_03 = "../../data/outputs/dataset03/evaluation_all/RFC/model.pkl"
samples_to_predict_path = "../../data/inputs/samples_AMPSphere/AMPs_experimentally_verified.csv"

# load samples
samples_to_predict = pd.read_csv(samples_to_predict_path)
print("Samples to predict:")
print(samples_to_predict.shape)
print(samples_to_predict.columns)
print(samples_to_predict.head())

# load model - classifier
with open(model_path_02, 'rb') as file:
  loaded_classifier = pickle.load(file)


# Use the loaded model to make predictions on new data
