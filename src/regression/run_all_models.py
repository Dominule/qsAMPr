import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from src.regression.models import (evaluate_models, NormalizedSVRModel, NormalizedRFRModel,
                                       NormalizedRGRModel, NormalizedMPRModel)
from src.train_models_old.data_cleaner import preprocess_features

evaluation_storage_folder = Path('../../data/outputs/regression_dataset/evaluation_all')

# load data
df = pd.read_csv('../../data/inputs/reg_descriptors_staphylococcus_MICs.csv')
X = df.drop(columns=['SEQUENCE', 'ACTIVITY'])
y = df['ACTIVITY']
# X = preprocess_features(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=30)

MODELS = [NormalizedSVRModel(), NormalizedRFRModel(), NormalizedRGRModel(), NormalizedMPRModel()]
names = ["SVR", "RFR", "RGR", "MPR"]
cv_models = []
best_estimators = []
for model in MODELS:
    model.fit(X_train, y_train)
    cv_models.append(model)
    best_estimators.append(model.model)

evaluate_models(best_estimators, cv_models, names, X_test, y_test, evaluation_storage_folder)
if __name__ == '__main__':
    ...
