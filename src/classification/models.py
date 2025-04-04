import pickle
from pathlib import Path
from typing import Any, List, Dict

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.svm import SVC

from src.classification.plot_model import draw_roc_curves, draw_precision_recall, draw_confusion_matrix, draw_cv_plot, \
    draw_cv_plots
from src.skeleton import PeptideModel

"""
Classification models based on skeleton
"""


### models with hyperparameters
class SVCModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            'C': [0.1, 1, 10, 100, 1000],
            'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
            'kernel': ['linear', 'rbf']
        }

    def get_model(self) -> Any:
        return SVC()

    def get_mode(self) -> str:
        return "classification"


class RFCModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            'n_estimators': [350, 400, 450, 550],
            'max_depth': [3, 4, 5, 6, 7, 8],
            'criterion': ['gini', 'entropy']
        }

    def get_model(self) -> Any:
        return RandomForestClassifier()

    def get_mode(self) -> str:
        return "classification"


class NBCModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {}

    def get_model(self) -> Any:
        return GaussianNB()

    def get_mode(self) -> str:
        return "classification"


class MPCModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            'hidden_layer_sizes': [(32 * i, 16 * i) for i in range(1, 11)]
                                  + [(32 * i, 16 * i, 8 * i) for i in range(1, 7)]
                                  + [(32 * i, 16 * i, 8 * i, 4 * i) for i in range(1, 5)]
                                  + [(32 * i, 16 * i, 8 * i, 4 * i, 2 * i) for i in range(1, 5)],
            # 'activation': ['relu', 'tanh'],
            'solver': ['adam'],  # 'sgd', 'lbfgs' slower
            'alpha': [0.0001, 0.001, 0.01],  # regularization parameter, maybe add 0.1
            # 'batch_size': [32, 64],     # try 128
            # 'learning_rate': ['adaptive', 'constant'],
            'early_stopping': [True]
        }

    def get_model(self) -> Any:
        return MLPClassifier()

    def get_mode(self) -> str:
        return "classification"


### models pipeline with normalization
class NormalizedSVCModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            "svc__C": [0.1, 1, 10, 100, 1000],
            "svc__kernel": ["linear", "rbf"],
            "svc__gamma": [0.0001, 0.001, 0.01, 0.1, 1, 10, 100]
        }

    def get_model(self) -> Any:
        return Pipeline([
            ("normalize", MinMaxScaler()),
            ("svc", SVC())
        ])

    def get_mode(self) -> str:
        return "classification"


class NormalizedRFCModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            'rf__n_estimators': [50, 100, 250, 500, 1000],
            'rf__max_depth': [2, 5, 7, 10, 20, 25, 50, None],
            'rf__criterion': ['gini', 'entropy']
        }

    def get_model(self) -> Any:
        return Pipeline([
            ("normalize", MinMaxScaler()),
            ("rf", RandomForestClassifier())
        ])

    def get_mode(self) -> str:
        return "classification"


class NormalizedNBCModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {}

    def get_model(self) -> Any:
        return Pipeline([
            ("normalize", MinMaxScaler()),
            ("nb", GaussianNB())
        ])

    def get_mode(self) -> str:
        return "classification"


class NormalizedMPCModel(PeptideModel):
    def get_hyperparam_space(self) -> Dict[str, List[Any]]:
        return {
            'mlp__hidden_layer_sizes': [(32 * i, 16 * i) for i in range(1, 11)]
                                       + [(32 * i, 16 * i, 8 * i) for i in range(1, 7)]
                                       + [(32 * i, 16 * i, 8 * i, 4 * i) for i in range(1, 5)]
                                       + [(32 * i, 16 * i, 8 * i, 4 * i, 2 * i) for i in range(1, 5)],
            # 'activation': ['relu', 'tanh'],
            'mlp__solver': ['adam'],  # 'sgd', 'lbfgs' slower
            'mlp__alpha': [0.0001, 0.001, 0.01],  # regularization parameter, maybe add 0.1
            # 'batch_size': [32, 64],     # try 128
            # 'learning_rate': ['adaptive', 'constant'],
            'mlp__early_stopping': [True]
        }

    def get_model(self) -> Any:
        return Pipeline([
            ("normalize", StandardScaler()),
            ("mlp", MLPClassifier())
        ])

    def get_mode(self) -> str:
        return "classification"


### evaluation functions - save the model and the metrics
def evaluate_model(model: PeptideModel, sequences: List[str], targets: List[float], folder: Path):
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
            print(classification_report(test_targets, predictions, output_dict=True)["weighted avg"]["precision"],
                  end=",", file=f)
            print(classification_report(test_targets, predictions, output_dict=True)["weighted avg"]["recall"], end=",",
                  file=f)
            print(classification_report(test_targets, predictions, output_dict=True)["weighted avg"]["f1-score"],
                  end=",", file=f)
            print(roc_auc_score(test_targets, predictions), end="\n", file=f)

    # save models
    for model, name in zip(cv_models, names):
        evaluate_model(model, test_sequences, test_targets, folder / name)

    # draw plots
    draw_roc_curves(best_estimators, test_sequences, test_targets, folder)
    draw_precision_recall(best_estimators, test_sequences, test_targets, folder)
    model_grids = [cv_models[i].get_grid_search() for i in range(len(cv_models))]
    draw_cv_plots(model_grids, folder)

# MODELS = [SVCModel(), RFCModel(), NBCModel(), MPCModel()]
