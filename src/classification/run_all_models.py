import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from src.classification.models import (evaluate_models, NormalizedNBCModel, NormalizedRFCModel,
                                       NormalizedSVCModel, NormalizedMPCModel)
from src.train_models_old.data_cleaner import preprocess_features


"""
Run all models.
Store the evaluation results in the evaluation_storage_folder.
Store train and test sequences in the test_storage_folder.
"""

# change this to the dataset you want to use: 01, 02, 03
dst = '03'

# set storage paths
evaluation_storage_folder = Path(f'../../data/outputs/dataset{dst}/evaluation_all')
test_storage_file = Path(f'../../data/outputs/dataset{dst}/evaluation_all/test_set_classification.csv')
train_storage_file = Path(f'../../data/outputs/dataset{dst}/evaluation_all/train_set_classification.csv')

# load data
df_pos = pd.read_csv('../../data/inputs/clf_descriptors_positive_staphylococcus.csv')
df_neg = pd.read_csv(f'../../data/inputs/clf_descriptors_negative_{dst}_dataset.csv')
df = pd.concat([df_pos, df_neg])
X = df.drop(columns=['ACTIVITY'])
y = df['ACTIVITY']
# X = preprocess_features(X)        # my preprocessing function which is apparently worse than simple scaling
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=30)
X_train_seqs = X_train['SEQUENCE']
X_test_seqs = X_test['SEQUENCE']
X_train = X_train.drop(columns=['SEQUENCE'])
X_test = X_test.drop(columns=['SEQUENCE'])

# train models
MODELS = [NormalizedSVCModel(), NormalizedRFCModel(), NormalizedNBCModel(), NormalizedMPCModel()]
names = ["SVC", "RFC", "NBC", "MPC"]
cv_models = []
best_estimators = []
for model in MODELS:
    model.fit(X_train, y_train)
    cv_models.append(model)
    best_estimators.append(model.model)

# evaluate and store models
evaluate_models(best_estimators, cv_models, names, X_test, y_test, evaluation_storage_folder)


# create dataframes with columns SEQUENCE and ACTIVITY
df_test = pd.DataFrame(columns=['SEQUENCE', 'ACTIVITY'])
df_test['SEQUENCE'] = X_test_seqs
df_test['ACTIVITY'] = y_test
df_train = pd.DataFrame(columns=['SEQUENCE', 'ACTIVITY'])
df_train['SEQUENCE'] = X_train_seqs
df_train['ACTIVITY'] = y_train

# store test and train sequences
df_test.to_csv(test_storage_file, index=False)
df_train.to_csv(train_storage_file, index=False)
