"""
Compute descriptors for all AMPSphere sequences.
Make predictions.
"""
import pickle
from src.classification.models import RFCModel
import pandas as pd
import peptides

# storage
storage_path = "../../data/outputs/predictions/AMPs_all_predicted.csv"

# paths to models
model_path_01 = "../../data/outputs/dataset01/evaluation_all/RFC/model.pkl"
model_path_02 = "../../data/outputs/dataset02/evaluation_all/RFC/model.pkl"
model_path_03 = "../../data/outputs/dataset03/evaluation_all/RFC/model.pkl"

# path to samples
samples_path = "../../data/samples_AMPSphere/AMP_all.csv"

# set thresholds
thr01 = 0.49
thr02 = 0.61
thr03 = 0.48

# load the ampsphere samples
ampsphere_samples = pd.read_csv(samples_path, delimiter='\t')

# load models
with open(model_path_01, 'rb') as file:
    loaded_classifier_01: RFCModel = pickle.load(file)
with open(model_path_02, 'rb') as file:
    loaded_classifier_02: RFCModel = pickle.load(file)
with open(model_path_03, 'rb') as file:
    loaded_classifier_03: RFCModel = pickle.load(file)

# print("Main samples:")
# print(ampsphere_samples.shape)
# print(main_samples.columns)
# print(main_samples.head())

# load models


# compute descriptors and predict
descriptors_list_list = []
for i in range(len(ampsphere_samples)):
    sequence = ampsphere_samples.iloc[i, 1]

    # create initial row
    row_dict = {"SEQUENCE": sequence,
                "FAMILY": ampsphere_samples.iloc[i, 2],
                "ANTIFAM": ampsphere_samples.iloc[i, 10],
                "RNACODE": ampsphere_samples.iloc[i, 11],
                "METAPROTEOMES": ampsphere_samples.iloc[i, 12],
                "METATRANSCRIPTOMES": ampsphere_samples.iloc[i, 13],
                "COORDINATES": ampsphere_samples.iloc[i, 14]}

    # compute descriptors
    descriptors = peptides.Peptide(sequence).descriptors()
    descriptors = pd.DataFrame([descriptors])


    # make predictions
    prediction01 = loaded_classifier_01.predict_proba(descriptors)
    prediction02 = loaded_classifier_02.predict_proba(descriptors)
    prediction03 = loaded_classifier_03.predict_proba(descriptors)
    if (prediction01[0,1]>thr01 and prediction02[0,1]>thr02 and prediction03[0,1]>thr03):
        prediction04 = True
    else:
        prediction04 = False

    predictions = {
        "PRED_01": prediction01[0,1],   #[0, 1] - 1 for proba if antimicrobial
        "PRED_02": prediction02[0,1],
        "PRED_03": prediction03[0,1],
        "HIGH_PROBA": prediction04
    }
    row_dict.update(predictions)

    # add row
    descriptors_list_list.append(row_dict)
descriptors_df = pd.DataFrame(descriptors_list_list)

# store into csv
descriptors_df.to_csv(storage_path, index=False)