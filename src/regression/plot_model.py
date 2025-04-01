from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import RocCurveDisplay, PrecisionRecallDisplay, ConfusionMatrixDisplay

def draw_regression(model, folder: Path):
    # draw roc curve
    # plot performance metrics
    file = folder / "reg_plot.png"

    accuracy = np.array([cv_results[f'split{i}_test_accuracy'][0] for i in range(5)])
    precision = np.array([cv_results[f'split{i}_test_precision'][0] for i in range(5)])
    recall = np.array([cv_results[f'split{i}_test_recall'][0] for i in range(5)])
    roc_auc = np.array([cv_results[f'split{i}_test_roc_auc'][0] for i in range(5)])
    std_devs = np.array([np.array(cv_results['std_test_accuracy'][0]),
                             np.array(cv_results['std_test_precision'][0]),
                             np.array(cv_results['std_test_recall'][0]),
                             np.array(cv_results['std_test_roc_auc'][0])])
    means = np.array([np.array(cv_results['mean_test_accuracy'][0]),
                          np.array(cv_results['mean_test_precision'][0]),
                          np.array(cv_results['mean_test_recall'][0]),
                          np.array(cv_results['mean_test_roc_auc'][0])])
    data = accuracy, precision, recall, roc_auc
    plt.boxplot(data, tick_labels=['Accuracy', 'Precision', 'Recall', 'ROC_AUC'])
    # Adds mean as red dots
    for i in range(len(means)):
        plt.plot(i + 1, means[i], 'ro')
    # Adds standard deviations as error bars
    for i in range(len(std_devs)):
        plt.errorbar(i + 1, means[i], yerr=std_devs[i], fmt='o', color='red')
    # Plots graph
    plt.title('Performance metrics')
    ax = plt.gca()
    ax.set_ylim([0, 1])
    plt.xlabel('Dataset')
    plt.ylabel('Value')
    plt.savefig(file)
    plt.clf()