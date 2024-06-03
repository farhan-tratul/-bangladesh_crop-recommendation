# -*- coding: utf-8 -*-
"""Cse366Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1d1CbPG6LMdwTqvjMWmgnNqgGudl6IoLG
"""



23569

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from pyswarm import pso
import random
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv('/content/Crop_recommendation.csv')
df.head()

x = df.drop('label', axis = 1)
y = df['label']

df['label'].value_counts()

x.info()

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y, random_state = 1,test_size=0.2)

y_train.info()

x_train.info()

from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
from sklearn.metrics import accuracy_score
logistic_acc = accuracy_score(y_test, y_pred)
print("Accuracy of logistic regression is " + str(logistic_acc))

from sklearn.tree import DecisionTreeClassifier
model_2 = DecisionTreeClassifier(criterion='entropy',max_depth = 6, random_state = 2)
model_2.fit(x_train, y_train)
y_pred_2 = model_2.predict(x_test)
decision_acc = accuracy_score(y_test, y_pred_2)
print("Accuracy of decision  tree is " + str(decision_acc))

from sklearn.ensemble import RandomForestClassifier
model_4 = RandomForestClassifier(n_estimators = 25, random_state=2)
model_4.fit(x_train.values, y_train.values)
y_pred_4 = model_4.predict(x_test)
random_fore_acc = accuracy_score(y_test, y_pred_4)
print("Accuracy of Random Forest is " + str(random_fore_acc))

from sklearn.naive_bayes import GaussianNB
model_3 = GaussianNB()
model_3.fit(x_train, y_train)
y_pred_3 = model_3.predict(x_test)
naive_bayes_acc = accuracy_score(y_test, y_pred_3)
print("Accuracy of naive_bayes is " + str(naive_bayes_acc))

"""------------------Cross over Validation--------------------"""

# list of models
models = [LogisticRegression(max_iter=1000), SVC(kernel='linear'), KNeighborsClassifier(), RandomForestClassifier()]

#Objective Function

from sklearn.model_selection import cross_val_score

# Number of folds for cross-validation
k = 15

# Dictionary to store the cross-validation scores of each model
cv_scores = {}

# Loop through the models
for model in models:
    model_name = model.__class__.__name__
    scores = cross_val_score(model, x, y, cv=k, scoring='accuracy')
    cv_scores[model_name] = scores
    print(f'{model_name}: {scores}')
    print(f'Mean Accuracy: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})\n')

# Print all cross-validation scores
print("\nCross-Validation Scores:")
for model_name, scores in cv_scores.items():
    print(f'{model_name}: Mean Accuracy = {scores.mean():.4f} (+/- {scores.std() * 2:.4f})')

"""----------------particle sorm----------------------------"""

#dataframe with features

df = pd.DataFrame({
    'feature1': np.random.rand(100),
    'feature2': np.random.rand(100),
    'label': np.random.randint(2, size=100)
})

# Define the objective function
def objective_function(params):
    n_estimators, max_depth = params
    n_estimators = int(n_estimators)
    if max_depth < 1:
        max_depth = None
    else:
        max_depth = int(max_depth)

    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    score = cross_val_score(model, x, y, cv=5, scoring='accuracy').mean()
    return -score  # We want to maximize accuracy, so we minimize the negative accuracy

# (min, max) for n_estimators and max_depth
bounds = [(10, 200), (1, 20)]

# Run PSO
optimal_params, optimal_score = pso(objective_function, lb=[bound[0] for bound in bounds], ub=[bound[1] for bound in bounds], swarmsize=30, maxiter=50)

# Print the optimal parameters and the best score
print("Optimal Parameters:", optimal_params)
print("Best Cross-Validation Score:", -optimal_score)

# Optimal hyperparameters from PSO
optimal_n_estimators = int(optimal_params[0])
optimal_max_depth = int(optimal_params[1])

# Train the final model
final_model = RandomForestClassifier(n_estimators=optimal_n_estimators, max_depth=optimal_max_depth, random_state=42)
final_model.fit(x, y)

# Evaluate on the same data (or ideally on a separate test set)
final_accuracy = final_model.score(x, y)
print("Final Model Accuracy:", final_accuracy)

import joblib

file_name = 'crop_app'
joblib.dump(model_4,'crop_app')
app = joblib.load('crop_app')
arr = [[90,42,43,20.879744,82.002744,6.502985,202.935536]]
acc = app.predict(arr)
acc

# Split features and target variable
X = df.drop('label', axis=1)  # Features
y = df['label']  # Target variable

# Split the data into training and test sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train a RandomForestClassifier
clf = RandomForestClassifier().fit(X_train, y_train)

train_accuracy = clf.score(X_train, y_train)
test_accuracy = clf.score(X_test, y_test)

print("Training Accuracy:", train_accuracy)
print("Test Accuracy:", test_accuracy)

"""Apply cross validation for training"""

# Split the data into features and target
X = data.drop('label', axis=1)
y = data['label']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize the model
model = RandomForestClassifier(random_state=42)

# Perform cross-validation
cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
print(f'Cross-Validation Accuracy: {cv_scores.mean()}')

# Hyperparameter tuning with GridSearchCV
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(model, param_grid, cv=5, n_jobs=-1, verbose=1)
grid_search.fit(X_train_scaled, y_train)

# Best parameters
best_params = grid_search.best_params_
print(f'Best Parameters: {best_params}')

# Train the best model
best_model = grid_search.best_estimator_
best_model.fit(X_train_scaled, y_train)

# Make predictions
y_train_pred = best_model.predict(X_train_scaled)
y_test_pred = best_model.predict(X_test_scaled)

# Calculate accuracy
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

print(f'Train Accuracy: {train_accuracy}')
print(f'Test Accuracy: {test_accuracy}')