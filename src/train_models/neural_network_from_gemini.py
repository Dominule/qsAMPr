import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def train_and_evaluate_mlp(data, target_column="ACTIVITY", test_size=0.2, random_state=42):
    """
    Trains and evaluates a Multi-layer Perceptron (MLP) classifier on a balanced dataset.

    Args:
        data (pd.DataFrame): The dataset with descriptors and the target variable.
        target_column (str): The name of the target variable column.
        test_size (float): The proportion of the dataset to include in the test split.
        random_state (int): Seed for reproducibility.

    Returns:
        tuple: A tuple containing the trained model, test accuracy, classification report,
               and confusion matrix.
    """

    # Separate features and target
    X = data.drop(target_column, axis=1)
    y = data[target_column]

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Scale the features, MinMaxScaler had worse results
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)


    # Build the MLP classifier model
    model = MLPClassifier(hidden_layer_sizes=(128, 64), activation='relu', solver='adam',
                          alpha=0.0001, batch_size='auto', learning_rate='adaptive',
                          max_iter=500, random_state=random_state) #Increased max_iter

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    confusion = confusion_matrix(y_test, y_pred)

    return model, accuracy, report, confusion, scaler #Return scaler for future predictions

# Example usage (replace 'your_data.csv' with your actual data file)
try:
    data_pos = pd.read_csv('../../data/inputs/clf_descriptors_positive_staphylococcus.csv')
    data_neg = pd.read_csv('../../data/inputs/clf_descriptors_negative_02_dataset.csv')
    data = pd.concat([data_pos, data_neg])
    data = data.drop(columns=['SEQUENCE'])
    model, accuracy, report, confusion, scaler = train_and_evaluate_mlp(data)

    print(f"Test Accuracy: {accuracy}")
    print("Classification Report:\n", report)
    print("Confusion Matrix:\n", confusion)

except FileNotFoundError:
    print("Error: 'your_data.csv' not found. Please provide the correct file path.")

except Exception as e:
    print(f"An error occurred: {e}")
