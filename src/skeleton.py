from abc import ABC, abstractmethod
from typing import Any, List, Dict
import pandas as pd
from sklearn.model_selection import GridSearchCV

"""
Interface for models
"""


class PeptideModel(ABC):
    def __init__(self):
        self.model = None

        # TODO - scoring for regression!
        if (self.get_mode() == 'classification'):
            self.grid_search = GridSearchCV(self.get_model(),
                                            self.get_hyperparam_space(),
                                            scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc'],
                                            refit="f1",  # podle tohohle se vybere nejlepší model
                                            verbose=0,
                                            return_train_score=True,
                                            cv=5, n_jobs=-1)
        elif (self.get_mode() == 'regression'):
            self.grid_search = GridSearchCV(self.get_model(),
                                            self.get_hyperparam_space(),
                                            scoring=['neg_mean_squared_error', 'r2'],
                                            refit="r2",
                                            verbose=0,
                                            return_train_score=True,
                                            cv=5, n_jobs=-1)

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

    @abstractmethod
    def get_mode(self) -> str:
        ...

    def predict(self, sequences: pd.DataFrame) -> pd.Series:
        return self.model.predict(sequences)

    def get_grid_search(self):
        return self.grid_search
