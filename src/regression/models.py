import pickle
from pathlib import Path
from statistics import LinearRegression
from typing import Dict, List, Any

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR

from src.regression.plot_model import draw_scatterplot, draw_histogram
from src.skeleton import PeptideModel

"""
Regression models based on skeleton
"""

### models with hyperparameters
class RGRModel(PeptideModel):

    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            'alpha': [0.1, 1.0, 10.0, 100.0]
        }
    def get_model(self) -> Any:
        return Ridge()
    def get_mode(self) -> str:
        return 'regression'



class SVRModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            'C': [0.1, 1, 10, 100, 1000],
            'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
            'kernel': ['linear', 'rbf']
        }
    def get_model(self) -> Any:
        return SVR()
    def get_mode(self) -> str:
        return 'regression'


class RFRModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            'n_estimators': [350, 400, 450, 550],
            'max_depth' : [3, 4, 5, 6, 7, 8],
            'criterion' :['mse', 'mae']
        }
    def get_model(self) -> Any:
        return RandomForestRegressor()
    def get_mode(self) -> str:
        return 'regression'

class MPRModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            'hidden_layer_sizes' : [(32*i, 16*i) for i in range(1, 11)]
                           +[(32*i, 16*i, 8*i) for i in range(1, 7)]
                           +[(32*i, 16*i, 8*i, 4*i) for i in range(1, 5)]
                           +[(32*i, 16*i, 8*i, 4*i, 2*i) for i in range(1, 5)],
            # 'activation': ['relu', 'tanh'],
            'solver': ['adam'], # 'sgd', 'lbfgs' slower
            'alpha': [0.0001, 0.001, 0.01], # regularization parameter, maybe add 0.1
            # 'batch_size': [32, 64],     # try 128
            # 'learning_rate': ['adaptive', 'constant'],
            'early_stopping': [True]
        }

    def get_model(self) -> Any:
        return MLPRegressor()
    def get_mode(self) -> str:
        return 'regression'


### models pipeline with normalization

class NormalizedSVRModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            "svr__C": [0.1, 1, 10, 100, 1000],
            "svr__kernel": ["linear", "rbf"],
            "svr__gamma": [1, 0.1, 0.01, 0.001, 0.0001]
            # "svr__epsilon": [0.1, 0.2, 0.5, 1.0, 2.0]
        }
    def get_model(self) -> Any:
        return Pipeline([
            ("normalize", MinMaxScaler()),
            ("svr", SVR())
        ])
    def get_mode(self) -> str:
        return 'regression'

class NormalizedRFRModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            # TODO change hyperparams
            'rfr__n_estimators': [50, 100, 250, 500, 1000],
            'rfr__max_depth': [2, 5, 7, 10, 20, 25, 50, None],
            "rfr__criterion": ["gini"]
        }
    def get_model(self) -> Any:
        return Pipeline([
            ("normalize", MinMaxScaler()),
            ("rfr", RandomForestRegressor())
        ])
    def get_mode(self) -> str:
        return 'regression'

class NormalizedRGRModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            'rgr__alpha': [0.1, 1.0, 10.0, 100.0]
        }
    def get_model(self) -> Any:
        return Pipeline([
            ("normalize", MinMaxScaler()),
            ("rgr", Ridge())
        ])
    def get_mode(self) -> str:
        return 'regression'

class NormalizedMPRModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            "mpr__hidden_layer_sizes": [(64, 32), (128, 64), (64, 32, 16)],
            "mpr__solver": ["adam"],
            "mpr__alpha": [0.001, 0.01],
            "mpr__early_stopping": [True]
            # activation: ['relu', 'tanh']
            # learning_rate: ['adaptive', 'constant']
            # batch_size: [32, 64]
        }

    def get_model(self) -> Any:
        return Pipeline([
            ("normalize", MinMaxScaler()),
            ("mpr", MLPRegressor())
        ])
    def get_mode(self) -> str:
        return 'regression'




### evaluation functions - save the model and the metrics - todo
def evaluate_model(model: PeptideModel, X_test, y_test: List[float], folder: Path):
    file_report = folder / "metrics.txt"
    file_model = folder / "model.pkl"
    file_predictions = folder / "predictions.csv"

    predictions = model.predict(X_test)
    draw_scatterplot(y_test, predictions, folder)
    draw_histogram(y_test, predictions, folder)

    # draw_confusion_matrix(model.model, sequences, targets, folder)
    folder.mkdir(exist_ok=True)
    with open(file_model, 'wb') as file:
        pickle.dump(model, file)
    with open(file_report, 'w') as f:
        print("Hyperparameters:\n" + str(model.grid_search.best_params_) + "\n\n", file=f)
        # print metrics
        print("Metrics:\n", file=f)
        print("R2 score: ", model.grid_search.best_score_, file=f)
        # print("MSE: ", model.grid_search.cv_results_['mean_squared_error'], file=f)
        # print("MAE: ", model.grid_search.cv_results_['mean_absolute_error'], file=f)
    with open(file_predictions, 'w') as f:
        pd.DataFrame({'y_true': y_test, 'y_pred': predictions}).to_csv(f, index=False)