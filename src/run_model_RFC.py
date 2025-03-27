import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from models import NormalizedRFCModel, RFCModel, evaluate_model
from src.train_models_old.data_cleaner import preprocess_features

evaluation_storage_folder = Path('../data/outputs/dataset03/evaluation_RFC')

# load data
df_pos = pd.read_csv('../data/inputs/clf_descriptors_positive_staphylococcus.csv')
df_neg = pd.read_csv('../data/inputs/clf_descriptors_negative_03_dataset.csv')
df = pd.concat([df_pos, df_neg])

X = df.drop(columns=['SEQUENCE','ACTIVITY'])
y = df['ACTIVITY']
# X = preprocess_features(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# train model
model = NormalizedRFCModel()
model.fit(X_train, y_train)
print(model.model)
evaluate_model(model, X_test, y_test, evaluation_storage_folder)
