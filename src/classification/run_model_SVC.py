import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from models import NormalizedSVCModel, SVCModel, evaluate_model
from src.train_models_old.data_cleaner import preprocess_features

evaluation_storage_folder = Path('../../data/outputs/dataset03/evaluation_SVC')

# load data
df_pos = pd.read_csv('../../data/inputs/clf_descriptors_positive_staphylococcus.csv')
df_neg = pd.read_csv('../../data/inputs/clf_descriptors_negative_03_dataset.csv')
df = pd.concat([df_pos, df_neg])

X = df.drop(columns=['SEQUENCE','ACTIVITY'])
y = df['ACTIVITY']
# X = preprocess_features(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=43)


# train model
model = NormalizedSVCModel()
model.fit(X_train, y_train)
print("Accuracy:")
print(np.array([model.grid_search.cv_results_[f'split{i}_test_accuracy'][0] for i in range(5)]))
print("Precision:")
print(np.array([model.grid_search.cv_results_[f'split{i}_test_precision'][0] for i in range(5)]))
print("Recall:")
print(np.array([model.grid_search.cv_results_[f'split{i}_test_recall'][0] for i in range(5)]))
print("F1:")
print(np.array([model.grid_search.cv_results_[f'split{i}_test_f1'][0] for i in range(5)]))
print("ROC_AUC:")
achjo = pd.DataFrame(model.grid_search.cv_results_)
print(achjo)
# print(np.array([model.grid_search.cv_results_[f'split{i}_test_roc_auc'][0] for i in range(5)]))
#save achjo into file
achjo.to_csv("achjo.csv")
print(model.grid_search.best_params_)
evaluate_model(model, X_test, y_test, evaluation_storage_folder)
