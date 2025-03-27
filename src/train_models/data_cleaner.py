"""
Clean the data for training
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import VarianceThreshold

def preprocess_features(df):
    """
    Preprocesses a pandas DataFrame by:
    1.  Scaling features using MinMaxScaler.
    2.  Removing features with zero variance.
    3.  Removing features with high correlation (> 0.92).
    4.  Removing features containing "BLOSUM" in their name.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The preprocessed DataFrame.
    """

    # Normalizing the data using MinMaxScaler
    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(df)
    df_feat = pd.DataFrame(scaled_features, columns=df.columns)

    # Variance threshold - remove features with zero variance
    selector = VarianceThreshold()
    selector.fit(df_feat)
    dropped_variance = df.columns[~selector.get_support()]
    df_feat = df_feat[df_feat.columns[selector.get_support(indices=True)]]
    print("-----Variance treshold-----")
    print(f"Features dropped: {dropped_variance}")
    print(f"New shape: {df_feat.shape}\n")

    # Trash randomly one of the features with correlation > 0.92
    corr_matrix = df_feat.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
    to_drop_corr = [column for column in upper.columns if any(upper[column] > 0.92)]
    df_feat = df_feat.drop(columns=to_drop_corr)
    print("-----Correlation filter-----")
    print(f"Features dropped: {to_drop_corr}")
    print(f"New shape: {df_feat.shape}\n")

    # Trash all features with "BLOSUM" in the name
    # to_drop_name = [col for col in df_feat.columns if "BLOSUM" in col]
    # df_feat = df_feat.drop(columns=to_drop_name)
    # print("-----Filter by name-----")
    # print(f"Features dropped: {to_drop_name}")
    # print(f"New shape: {df_feat.shape}\n")

    return df_feat