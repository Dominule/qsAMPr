import peptides
import pickle
import pandas as pd
from joblib import Parallel, delayed
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from src.classification.models import RFCModel

"""
Train_test_split on all three datasets.
Get test set for AMPSPhere annotation.
Compute descriptors.
Store test samples in a separate file.
Get best threshold for each model and store all results in a file.
"""

# descriptors_storage_path = "../../data/inputs/test_preprocessed_sequences_classfication.csv"
prediction_storage_folder = "../../data/outputs/predictions/tested_classifiers_for_AMPSphere.tsv"

# storage path for thresholds results
thresholds_results_path = "../../data/outputs/thresholds_results.csv"

# load the test samples
df_test_01 = pd.read_csv('../../data/outputs/dataset01/evaluation_all/test_set_classification.csv')
df_test_02 = pd.read_csv('../../data/outputs/dataset02/evaluation_all/test_set_classification.csv')
df_test_03 = pd.read_csv('../../data/outputs/dataset03/evaluation_all/test_set_classification.csv')

# remove all with ACTIVITY=1 from df_test_02 and df_test_03, sort df_test_01
df_test_01 = df_test_01.sort_values(by=['ACTIVITY'], ascending=False)
df_test_02 = df_test_02[df_test_02['ACTIVITY'] == 0]
df_test_03 = df_test_03[df_test_03['ACTIVITY'] == 0]

# concat all
df = pd.concat([df_test_01, df_test_02, df_test_03])
test_sequences = list(df['SEQUENCE'])
test_activities = list(df['ACTIVITY'])

# compute descriptors
descriptors_list_list = []
for i in range(len(test_sequences)):
    sequence = test_sequences[i]

    # create row
    row_dict = {}
    descriptors = peptides.Peptide(sequence).descriptors()  # compute descriptors
    row_dict.update(descriptors)
    # add row
    descriptors_list_list.append(row_dict)
descriptors_df = pd.DataFrame(descriptors_list_list)

# predict activity of test samples using a trained models

# load the models
model_path_01 = "../../data/outputs/dataset01/evaluation_all/RFC/model.pkl"
model_path_02 = "../../data/outputs/dataset02/evaluation_all/RFC/model.pkl"
model_path_03 = "../../data/outputs/dataset03/evaluation_all/RFC/model.pkl"
with open(model_path_01, 'rb') as file:
    loaded_classifier_01: RFCModel = pickle.load(file)
with open(model_path_02, 'rb') as file:
    loaded_classifier_02: RFCModel = pickle.load(file)
with open(model_path_03, 'rb') as file:
    loaded_classifier_03: RFCModel = pickle.load(file)

# predict on test samples
prediction01 = loaded_classifier_01.predict_proba(descriptors_df)[:, 1]
prediction02 = loaded_classifier_02.predict_proba(descriptors_df)[:, 1]
prediction03 = loaded_classifier_03.predict_proba(descriptors_df)[:, 1]

# make dataframe from sequence, predictions
predictions_df = pd.DataFrame({
    'SEQUENCE': test_sequences,
    'PREDICTION_01': prediction01,
    'PREDICTION_02': prediction02,
    'PREDICTION_03': prediction03,
    'ACTIVITY': test_activities
})

# store predictions
predictions_df.to_csv(prediction_storage_folder, index=False, sep='\t', decimal=',')

# threshold for each model
threshold_range = [perc / 100 for perc in range(20, 100)]
best_thr_01 = 0.5
best_thr_02 = 0.5
best_thr_03 = 0.5


def get_metrics(thr1, thr2, thr3):
    predicted = (prediction01 > thr1) & (prediction02 > thr2) & (prediction03 > thr3)
    return (
        accuracy_score(test_activities, predicted),
        f1_score(test_activities, predicted, zero_division=0),
        precision_score(test_activities, predicted, zero_division=0),
        recall_score(test_activities, predicted, zero_division=0)
    )


thresholds1 = pd.Series(prediction01).round(2).unique()
thresholds2 = pd.Series(prediction02).unique()
thresholds3 = pd.Series(prediction03).round(2).unique()
# results = Parallel(n_jobs=-1, verbose=3)(delayed(get_metrics)(i, j, k)
#                               for i in thresholds1
#                               for j in thresholds2
#                               for k in thresholds3)
# accuracies = [r[0] for r in results]
# f1s = [r[1] for r in results]
# precisions = [r[2] for r in results]
# recalls = [r[3] for r in results]
# results = pd.DataFrame({"accuracy": accuracies, "f1": f1s, "precision": precisions, "recall": recalls},
#                        index=[(i, j, k) for i in thresholds1
#                               for j in thresholds2
#                               for k in thresholds3])
results = pd.read_csv(thresholds_results_path)
results.index = [(i, j, k) for i in thresholds1
                 for j in thresholds2
                 for k in thresholds3]
results.to_csv(thresholds_results_path)
print(results)


# trash all with at least one metric < 0.5