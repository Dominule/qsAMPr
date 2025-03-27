import pickle
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List, Dict
import pandas as pd
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from plot_model import draw_roc_curves, draw_precision_recall, draw_confusion_matrix, draw_cv_plot, draw_cv_plots

"""
Interface for models
"""


class ProteinModel(ABC):
    def __init__(self):
        self.model = None
        self.grid_search = GridSearchCV(self.get_model(),
                                        self.get_hyperparam_space(),
                                        scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc'],
                                        refit="accuracy",  # podle tohohle se vybere nejlepší model
                                        verbose=0,
                                        return_train_score=True,
                                        cv=5)

    def fit(self, sequences: pd.DataFrame, targets: pd.Series):
        self.grid_search.fit(sequences, targets)
        self.model = self.grid_search.best_estimator_
        return self

    @abstractmethod
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        ...

    @abstractmethod
    def get_model(self) -> Any:
        ...

    def predict(self, sequences: pd.DataFrame) -> pd.Series:
        return self.model.predict(sequences)

    def get_grid_search(self):
        return self.grid_search


### models with hyperparameters
class SVCModel(ProteinModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            'C': [0.1, 1, 10, 100, 1000],
            'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
            'kernel': ['linear', 'rbf']
        }
    def get_model(self) -> Any:
        return SVC()

class RFCModel(ProteinModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            'n_estimators': [350, 400, 450, 550],
            'max_depth' : [3, 4, 5, 6, 7, 8],
            'criterion' :['gini', 'entropy']
        }
    def get_model(self) -> Any:
        return RandomForestClassifier()

class NBCModel(ProteinModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {}
    def get_model(self) -> Any:
        return GaussianNB()

class MPCModel(ProteinModel):
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
        return MLPClassifier()


### models pipeline with normalization
class NormalizedSVCModel(ProteinModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            "svc__C": [0.1, 1, 10, 100, 1000],
            "svc__kernel": ["linear", "rbf"],
            "svc__gamma": [1, 0.1, 0.01, 0.001, 0.0001]
        }
    def get_model(self) -> Any:
        return Pipeline([
            ("normalize", MinMaxScaler()),
            ("svc", SVC())
        ])

class NormalizedRFCModel(ProteinModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            'rf__n_estimators': [350, 400, 450, 550],
            'rf__max_depth' : [3, 4, 5, 6, 7, 8],
            'rf__criterion' :['gini', 'entropy']
        }
    def get_model(self) -> Any:
        return Pipeline([
            ("normalize", MinMaxScaler()),
            ("rf", RandomForestClassifier())
        ])

class NormalizedNBCModel(ProteinModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {}
    def get_model(self) -> Any:
        return Pipeline([
            ("normalize", MinMaxScaler()),
            ("nb", GaussianNB())
        ])

class NormalizedMPCModel(ProteinModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            'mlp__hidden_layer_sizes' : [(32*i, 16*i) for i in range(1, 11)]
                           +[(32*i, 16*i, 8*i) for i in range(1, 7)]
                           +[(32*i, 16*i, 8*i, 4*i) for i in range(1, 5)]
                           +[(32*i, 16*i, 8*i, 4*i, 2*i) for i in range(1, 5)],
            # 'activation': ['relu', 'tanh'],
            'mlp__solver': ['adam'], # 'sgd', 'lbfgs' slower
            'mlp__alpha': [0.0001, 0.001, 0.01], # regularization parameter, maybe add 0.1
            # 'batch_size': [32, 64],     # try 128
            # 'learning_rate': ['adaptive', 'constant'],
            'mlp__early_stopping':[True]
        }
    def get_model(self) -> Any:
        return Pipeline([
            ("normalize", StandardScaler()),
            ("mlp", MLPClassifier())
        ])



### evaluation functions - save the model and the metrics
def evaluate_model(model: ProteinModel, sequences: List[str], targets: List[float], folder: Path):
    file_report = folder / "metrics.txt"
    file_model = folder / "model.pkl"
    draw_cv_plot(model.grid_search.cv_results_, folder)
    draw_confusion_matrix(model.model, sequences, targets, folder)
    predictions = model.predict(sequences)
    folder.mkdir(exist_ok=True)
    with open(file_model, 'wb') as file:
        pickle.dump(model, file)
    with open(file_report, 'w') as f:
        print("Hyperparameters:\n" + str(model.grid_search.best_params_) + "\n\n", file=f)
        print(classification_report(targets, predictions, digits=3), file=f)
        print(f"Confusion matrix:\n{pd.crosstab(targets, predictions)}", file=f)

def evaluate_models(best_estimators, cv_models, names, test_sequences: List[str],
                    test_targets: List[float], folder: Path):
    # store a table with metrics
    file_report = folder / "metrics.csv"
    with open(file_report, "w") as f:
        print("model,accuracy,precision,recall,f1,roc_auc", file=f)
        for model, name in zip(best_estimators, names):
            predictions = model.predict(test_sequences)
            print(name, end=",", file=f)
            print(classification_report(test_targets, predictions, output_dict=True)["accuracy"], end=",", file=f)
            print(classification_report(test_targets, predictions, output_dict=True)["weighted avg"]["precision"], end=",", file=f)
            print(classification_report(test_targets, predictions, output_dict=True)["weighted avg"]["recall"], end=",", file=f)
            print(classification_report(test_targets, predictions, output_dict=True)["weighted avg"]["f1-score"], end=",", file=f)
            print(roc_auc_score(test_targets, predictions), end="\n", file=f)

    # save models
    for model, name in zip(cv_models, names):
        evaluate_model(model, test_sequences, test_targets, folder / name)

    # draw plots
    draw_roc_curves(best_estimators, test_sequences, test_targets, folder)
    draw_precision_recall(best_estimators, test_sequences, test_targets, folder)
    model_grids = [cv_models[i].get_grid_search() for i in range(len(cv_models))]
    draw_cv_plots(model_grids, folder)



MODELS = [SVCModel(), RFCModel(), NBCModel(), MPCModel()]
