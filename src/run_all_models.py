import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from models import (evaluate_models, NormalizedNBCModel, NormalizedRFCModel,
                    NormalizedSVCModel, NormalizedMPCModel)
from src.train_models.data_cleaner import preprocess_features

evaluation_storage_folder = Path('../data/outputs/dataset03/evaluation_all')


# load data
df_pos = pd.read_csv('../data/inputs/clf_descriptors_positive_staphylococcus.csv')
df_neg = pd.read_csv('../data/inputs/clf_descriptors_negative_03_dataset.csv')
df = pd.concat([df_pos, df_neg])
X = df.drop(columns=['SEQUENCE','ACTIVITY'])
y = df['ACTIVITY']
# X = preprocess_features(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

MODELS = [ NormalizedSVCModel(), NormalizedRFCModel(), NormalizedNBCModel(), NormalizedMPCModel()]
names = ["SVC", "RFC", "NBC", "MPC"]
cv_models = []
best_estimators = []
for model in MODELS:
    model.fit(X_train, y_train)
    cv_models.append(model)
    best_estimators.append(model.model)

evaluate_models(best_estimators, cv_models, names, X_test, y_test, evaluation_storage_folder)
