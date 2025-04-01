import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from models import NormalizedRFRModel, RFRModel, evaluate_model
from src.train_models_old.data_cleaner import preprocess_features

evaluation_storage_folder = Path('../../data/outputs/dataset02/evaluation_RFC')

# load data
df = pd.read_csv('../../data/inputs/reg_descriptors_staphylococcus_MICs.csv')

X = df.drop(columns=['SEQUENCE','ACTIVITY'])
y = df['ACTIVITY']
# X = preprocess_features(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# train model
model = NormalizedRFRModel()
model.fit(X_train, y_train)
print(model.model)
print(model.grid_search.best_params_)
evaluate_model(model, X_test, y_test, evaluation_storage_folder)
