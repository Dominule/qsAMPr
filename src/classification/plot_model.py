from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import RocCurveDisplay, PrecisionRecallDisplay, ConfusionMatrixDisplay


# GridSearchCV - boxplots with metrics and standard deviations
def draw_cv_plot(cv_results: Dict, folder: Path):
    # draw roc curve
    # plot performance metrics
    file = folder / "plot_std_devs.png"

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


# RocCurveDisplay
def draw_roc_curves(models, x_test, y_test, folder: Path):
    file = folder / "roc_curves.png"

    ax = plt.gca()
    for model in models:
        RocCurveDisplay.from_estimator(model, x_test, y_test, ax=ax)
    ax.plot([0, 1], [0, 1], transform=ax.transAxes)
    ax.set_ylim([0, 1])
    plt.title('ROC curves of all models')
    plt.savefig(file)
    plt.clf()


# PrecisionRecallDisplay
def draw_precision_recall(models, x_test, y_test, folder: Path):
    file = folder / "precision_recall_curves.png"

    ax = plt.gca()
    for model in models:
        PrecisionRecallDisplay.from_estimator(model, x_test, y_test, ax=ax)
    ax.set_ylim([0, 1])
    plt.title('Precision-recall curves of all models')
    plt.savefig(file)
    plt.clf()


# ConfusionMatrixDisplay
def draw_confusion_matrix(model, x_test, y_test, folder: Path):
    file = folder / "confusion_matrix.png"
    ConfusionMatrixDisplay.from_estimator(model, x_test, y_test)
    plt.title('Confusion matrix')
    plt.savefig(file)
    plt.clf()


def draw_cv_plots(model_grids, folder: Path):
    file = folder / "plot_metrics.png"
    print(np.array([model_grids[0].cv_results_[f'split{i}_test_accuracy'][0] for i in range(5)]))
    svm_values = np.concatenate([np.array([model_grids[0].cv_results_[f'split{i}_test_accuracy'][0] for i in range(5)]),
                                 np.array([model_grids[0].cv_results_[f'split{i}_test_precision'][0] for i in range(5)]),
                                 np.array([model_grids[0].cv_results_[f'split{i}_test_recall'][0] for i in range(5)]),
                                 np.array([model_grids[0].cv_results_[f'split{i}_test_f1'][0] for i in range(5)]),
                                 np.array([model_grids[0].cv_results_[f'split{i}_test_roc_auc'][0] for i in range(5)])])
    rf_values = np.concatenate([np.array([model_grids[1].cv_results_[f'split{i}_test_accuracy'][0] for i in range(5)]),
                                np.array([model_grids[1].cv_results_[f'split{i}_test_precision'][0] for i in range(5)]),
                                np.array([model_grids[1].cv_results_[f'split{i}_test_recall'][0] for i in range(5)]),
                                np.array([model_grids[1].cv_results_[f'split{i}_test_f1'][0] for i in range(5)]),
                                np.array([model_grids[1].cv_results_[f'split{i}_test_roc_auc'][0] for i in range(5)])])
    nb_values = np.concatenate([np.array([model_grids[2].cv_results_[f'split{i}_test_accuracy'][0] for i in range(5)]),
                                np.array([model_grids[2].cv_results_[f'split{i}_test_precision'][0] for i in range(5)]),
                                np.array([model_grids[2].cv_results_[f'split{i}_test_recall'][0] for i in range(5)]),
                                np.array([model_grids[2].cv_results_[f'split{i}_test_f1'][0] for i in range(5)]),
                                np.array([model_grids[2].cv_results_[f'split{i}_test_roc_auc'][0] for i in range(5)])])
    mlp_values = np.concatenate([np.array([model_grids[3].cv_results_[f'split{i}_test_accuracy'][0] for i in range(5)]),
                                    np.array([model_grids[3].cv_results_[f'split{i}_test_precision'][0] for i in range(5)]),
                                    np.array([model_grids[3].cv_results_[f'split{i}_test_recall'][0] for i in range(5)]),
                                 np.array([model_grids[3].cv_results_[f'split{i}_test_f1'][0] for i in range(5)]),
                                 np.array([model_grids[3].cv_results_[f'split{i}_test_roc_auc'][0] for i in range(5)])])

    data = {
        'Model': ['SVC'] * 25 + ['RFC'] * 25 + ['NBC'] * 25 + ['MLPC'] * 25,    # here
        'Metric': (['Accuracy'] * 5 + ['Precision'] * 5 + ['Recall'] * 5 + ['F1'] * 5 + ['ROC_AUC'] * 5) * 4, # here
        'Value': np.concatenate([svm_values, rf_values, nb_values, mlp_values]) # here
    }
    # store data into csv
    storage = folder / "cv_results_data.csv"
    pd.DataFrame(data).to_csv(storage, index=False)

    df = pd.DataFrame(data)
    sns.boxplot(x='Model', y='Value', data=df, hue='Metric', palette='Set2')
    plt.title('Comparison of performance metrics for all models.')
    ax = plt.gca()
    ax.set_ylim([0, 1])
    plt.savefig(file)
    plt.show()
    plt.clf()

