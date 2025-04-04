from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from numpy.random._examples.cffi.extending import rng
from pandas import DataFrame
from sklearn.metrics import RocCurveDisplay, PrecisionRecallDisplay, ConfusionMatrixDisplay

def draw_scatterplot(y_test, predictions, folder: Path):
    # draw roc curve
    # plot performance metrics
    file = folder / "reg_plot.png"

    plt.scatter(y_test, predictions, c='crimson')
    p1 = max(max(predictions), max(y_test))
    p2 = min(min(predictions), min(y_test))
    plt.plot([p1, p2], [p1, p2], 'b-')


    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    plt.title('Scatter plot')
    plt.axis([0, 100, 0, 100])      # todo change axis?
    plt.savefig(file)
    plt.show()
    plt.clf()


def draw_histogram(y_test, predictions, folder: Path):
    file_pred = folder / "histogram_predicted.png"
    file_actual = folder / "histogram_actual.png"

    # hist y_pred, y_test
    plt.axis([-10, 100, 0, 10])
    plt.hist(predictions, bins=100)
    plt.title('Predicted Values')
    plt.savefig(file_pred)
    plt.clf()
    plt.axis([0, 100, 0, 10])
    plt.hist(y_test, bins=100)
    plt.title('Actual Values')
    plt.savefig(file_actual)
    plt.clf()


