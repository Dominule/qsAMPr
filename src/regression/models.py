from typing import Dict, List, Any

from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR

from src.skeleton import PeptideModel

"""
Regression models based on skeleton
"""

### models with hyperparameters
class SVRModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            'C': [0.1, 1, 10, 100, 1000],
            'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
            'kernel': ['linear', 'rbf']
        }
    def get_model(self) -> Any:
        return SVR()


class RFRModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            'n_estimators': [350, 400, 450, 550],
            'max_depth' : [3, 4, 5, 6, 7, 8],
            'criterion' :['mse', 'mae']
        }
    def get_model(self) -> Any:
        return RandomForestRegressor()

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
            'early_stopping':[True]
        }

    def get_model(self) -> Any:
        return MLPRegressor()


### models pipeline with normalization

class NormalizedSVRModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            "svc__C": [0.1, 1, 10, 100, 1000],
            "svc__kernel": ["linear", "rbf"],
            "svc__gamma": [1, 0.1, 0.01, 0.001, 0.0001]
        }
    def get_model(self) -> Any:
        return Pipeline([
            ("normalize", MinMaxScaler()),
            ("svc", SVR())
        ])

class NormalizedRFRModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            "rfr__n_estimators": [350, 400, 450, 550],
            "rfr__max_depth" : [3, 4, 5, 6, 7, 8],
            "rfr__criterion" :["mse", "mae"]
        }
    def get_model(self) -> Any:
        return Pipeline([
            ("normalize", MinMaxScaler()),
            ("rfr", RandomForestRegressor())
        ])

class NormalizedMPRModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            "mpr__hidden_layer_sizes" : [(32*i, 16*i) for i in range(1, 11)]
                           +[(32*i, 16*i, 8*i) for i in range(1, 7)]
                           +[(32*i, 16*i, 8*i, 4*i) for i in range(1, 5)]
                           +[(32*i, 16*i, 8*i, 4*i, 2*i) for i in range(1, 5)],
            # 'activation': ['relu', 'tanh'],
            "mpr__solver": ["adam"], # 'sgd', 'lbfgs' slower
            "mpr__alpha": [0.0001, 0.001, 0.01], # regularization parameter, maybe add 0.1
            # 'batch_size': [32, 64],     # try 128
            # 'learning_rate': ['adaptive', 'constant'],
            "mpr__early_stopping":[True]
        }

    def get_model(self) -> Any:
        return Pipeline([
            ("normalize", MinMaxScaler()),
            ("mpr", MLPRegressor())
        ])




### evaluation functions - save the model and the metrics - todo
