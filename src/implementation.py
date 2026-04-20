"""
Project: Network Intrusion Detection System (NIDS)

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, confusion_matrix, classification_report)

# PHASE 1 & 2: BUSINESS & DATA UNDERSTANDING


def display_project_goals():
    print("PHASE 1: BUSINESS UNDERSTANDING ")
    print("Goal: Build an ML model to solve alert fatigue.")
    print("Success Criteria: Achieve a False Positive Rate < 1%.\n")
def load_dataset(filename):
    """Loads the raw CSV data."""
    if not os.path.exists(filename):
        print(f"Error: {filename} not found in the directory.")
        return None
    df = pd.read_csv(filename)
    print(f" PHASE 2: DATA LOADED ")
    print(f"Records: {df.shape[0]} | Features: {df.shape[1]}")
    return df

# PHASE 3: DATA PREPARATION (CLEANING & ENCODING)


def clean_and_prepare_data(df):
    """
    Cleans the data to make it ready for the Machine Learning models.
    """
    print("\n PHASE 3: DATA PREPARATION ")
    
    # 1. Handling Duplicates: i remove these so the model doesn't overfit to repeated data.
    original_size = len(df)
    df = df.drop_duplicates()
    print(f"Cleaned {original_size - len(df)} duplicate records.")

    # 2. Handling Missing Values: 
    # i use 'median' for numbers because it is robust against outliers.
    num_cols = df.select_dtypes(include=np.number).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    # 3. Categorical Encoding:
    # Models only understand numbers, so i turned words into columns using One-Hot Encoding.
    df = pd.get_dummies(df, drop_first=True)

    # 4. Feature Scaling:
    # i use StandardScaler so features like 'src_bytes' (large numbers) 
    # don't dominate features with small numbers.
    scaler = StandardScaler()
    # i don't want to scale our target 'class_normal', just the features.
    target_col = 'class_normal'
    features = [col for col in df.columns if col != target_col]
    
    df[features] = scaler.fit_transform(df[features])
    
    print("Data cleaning, encoding, and scaling complete.")
    return df


# PHASE 4 & 5: MODELLING & EVALUATION


def train_and_evaluate_model(df):
    """
    Splits the data, trains the Random Forest, and checks performance.
    """
    print("\nPHASE 4 & 5: MODELLING & EVALUATION ")
    
    # Defining features (X) and target (y)
    target = 'class_normal'
    X = df.drop(columns=[target])
    y = df[target]
    
    # i split 80% for training and 20% for testing to see how it handles new data.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # i chose Random Forest because it handles complex network traffic patterns well
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Making predictions on the test set
    y_pred = model.predict(X_test)
    
    # Calculating key metrics
    recall = recall_score(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Results: Accuracy = {accuracy:.2%} | Recall = {recall:.2%}")
    print("\nFull Classification Report:")
    print(classification_report(y_test, y_pred))
    
    return model, X_test, y_test


# PHASE 6: DEPLOYMENT (SAVING THE MODEL)


def deploy_system(model):
    """
    Saves the model as a file so it can be used in a real security dashboard.
    """
    print("\nPHASE 6: DEPLOYMENT ")
    model_filename = 'intrusion_detection_model.pkl'
    joblib.dump(model, model_filename)
    print(f"Model serialized and saved as '{model_filename}' for production use.")
    print("Project successfully completed following CRISP-DM standards.")


# MAIN ENGINE

if __name__ == "__main__":
    # Step 1: Initialize the project
    display_project_goals()
    
    # Step 2: Load the data 
    raw_data = load_dataset("Train_data.csv")
    if raw_data is not None:
        # Step 3: Run the cleaning pipeline
        processed_data = clean_and_prepare_data(raw_data)
        
        # Step 4: Run the modelling engine
        final_model, x_test, y_test = train_and_evaluate_model(processed_data)
        
        # Step 5: Save for deployment
        deploy_system(final_model)