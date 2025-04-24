import pickle
import pandas as pd
import matplotlib.pyplot as plt
import src.classification.plot_model
from src.classification.models import RFCModel

"""
Get feature importances from trained model and store.
"""


# Model paths
model_path_01 = "../../data/outputs/dataset01/evaluation_all/RFC/model.pkl"
model_path_02 = "../../data/outputs/dataset02/evaluation_all/RFC/model.pkl"
model_path_03 = "../../data/outputs/dataset03/evaluation_all/RFC/model.pkl"

# Dataset path
dataset = pd.read_csv("../../data/inputs/clf_descriptors_negative_01_dataset.csv")

# Storage path for importance graph
storage_file_first_ten = "../../data/outputs/feature_importance_first_ten.txt"
storage_file_plot_01 = '../../data/outputs/feature_importance_model01.png'
storage_file_plot_02 = '../../data/outputs/feature_importance_model02.png'
storage_file_plot_03 = '../../data/outputs/feature_importance_model03.png'


# Load model - classifier
with open(model_path_01, 'rb') as file:
    clf01: RFCModel = pickle.load(file)
with open(model_path_02, 'rb') as file:
    clf02: RFCModel = pickle.load(file)
with open(model_path_03, 'rb') as file:
    clf03: RFCModel = pickle.load(file)

# Get feature importances
importances01 = clf01.model['rf'].feature_importances_
importances02 = clf02.model['rf'].feature_importances_
importances03 = clf03.model['rf'].feature_importances_
dataset = dataset.drop(columns=['ACTIVITY', 'SEQUENCE'])
feature_names = dataset.columns.tolist()

# Create a DataFrame for better visualization
importance_df01 = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importances01
}).sort_values(by='Importance', ascending=False)

importance_df02 = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importances02
}).sort_values(by='Importance', ascending=False)

importance_df03 = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importances03
}).sort_values(by='Importance', ascending=False)


# Store first 10 features of each model
with open(storage_file_first_ten, 'w') as file:
    print("Feature importance\t\tModel 01\n", file=file)
    print(importance_df01.head(10), file=file)
    print("\n\n\nFeature importance\t\tModel 02\n", file=file)
    print(importance_df02.head(10), file=file)
    print("\n\n\nFeature importance\t\tModel 03\n", file=file)
    print(importance_df03.head(10), file=file)

# Plot feature importances
plt.figure(figsize=(10, 20))
plt.barh(importance_df01['Feature'], importance_df01['Importance'])
plt.xlabel('Importance')
plt.title('Feature Importances')
# plt.yticks(rotation=45)
plt.savefig(storage_file_plot_01)

plt.figure(figsize=(10, 20))
plt.barh(importance_df02['Feature'], importance_df02['Importance'])
plt.xlabel('Importance')
plt.title('Feature Importances')
# plt.yticks(rotation=45)
plt.savefig(storage_file_plot_02)

plt.figure(figsize=(10, 20))
plt.barh(importance_df03['Feature'], importance_df03['Importance'])
plt.xlabel('Importance')
plt.title('Feature Importances')
# plt.yticks(rotation=45)
plt.savefig(storage_file_plot_03)
