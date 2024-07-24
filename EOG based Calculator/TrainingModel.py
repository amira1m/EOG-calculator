from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.linear_model import LogisticRegression
import joblib
import numpy as np

# =====================================
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

from ExtractFeatures import feature_extraction
from Preprocessing import preprocessing
from SingalPreprocessing import process_signals


# import matplotlib.pyplot as plt


def SVM_classification(X_train, y_train, X_test, y_test):
    # Define the parameter grid for grid search
    param_grid = {
        'C': [0.1, 1, 10, 100],
        'gamma': [0.1, 0.01, 0.001, 0.0001],
        'kernel': ['rbf', 'linear', 'poly']
    }

    # Initialize the SVM classifier
    svm_model = SVC(random_state=4)

    # Perform grid search
    grid_search = GridSearchCV(estimator=svm_model, param_grid=param_grid, cv=3, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    # Get the best model from grid search
    best_svm_model = grid_search.best_estimator_

    # Fit the best model to the training data
    best_svm_model.fit(X_train, y_train)

    # Predict on the test data using the best model
    y_pred = best_svm_model.predict(X_test)

    # Predict on the training data for evaluation
    Y_train_pred = best_svm_model.predict(X_train)
    train_accuracy = accuracy_score(y_train, Y_train_pred)
    print("Training Accuracy:", train_accuracy)

    # Calculate accuracy on the test data
    test_accuracy = accuracy_score(y_test, y_pred)
    print("Test Accuracy:", test_accuracy)

    # Print the best parameters found by grid search
    print("Best Parameters:", grid_search.best_params_)

    model_filename = "Saved Models/SVM.pkl"
    joblib.dump(best_svm_model, model_filename)
    return train_accuracy, test_accuracy


def Random_Forest_classification(x_train, y_train, X_test, y_test):
    # Define the parameter grid for grid search
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }

    # Initialize the Random Forest classifier
    rf_model = RandomForestClassifier(random_state=4)

    # Perform grid search
    grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=3, n_jobs=-1)
    grid_search.fit(x_train, y_train)

    # Get the best model from grid search
    best_rf_model = grid_search.best_estimator_

    # Fit the best model to the training data
    best_rf_model.fit(x_train, y_train)

    # Predict on the test data using the best model
    y_pred = best_rf_model.predict(X_test)

    # Predict on the training data for evaluation
    Y_train_pred = best_rf_model.predict(x_train)
    train_accuracy = accuracy_score(y_train, Y_train_pred)
    print("Training Accuracy:", train_accuracy)

    # Calculate accuracy on the test data
    test_accuracy = accuracy_score(y_test, y_pred)
    print("Test Accuracy:", test_accuracy)

    # Print the best parameters found by grid search
    print("Best Parameters:", grid_search.best_params_)

    model_filename = "Saved Models/random_forest.pkl"
    joblib.dump(best_rf_model, model_filename)
    return train_accuracy, test_accuracy


def Logistic_classification(X_train, Y_train, X_test, Y_test):
    # Define the parameter grid for logistic regression
    param_grid = {
        'C': [.001, .01, 0.1, 1],  # Regularization parameter
        'penalty': ['l1', 'l2'],  # Type of regularization
        'solver': ['saga']
        # Increase the maximum number of iterations
        # 'saga' supports both l1 and l2 regularization
    }

    # GridSearchCV with 5-fold cross-validation
    grid_search = GridSearchCV(
        LogisticRegression(),
        param_grid,
        cv=5,  # 5-fold cross-validation
        scoring='accuracy',  # Optimize for accuracy
        n_jobs=-1,  # Use all available CPU cores
    )
    # Fit the grid search to the training data
    grid_search.fit(X_train, Y_train)
    # # Best estimator and its hyperparameters
    best_model = grid_search.best_estimator_

    # Calculate test accuracy
    Y_test_pred = best_model.predict(X_test)
    test_accuracy = accuracy_score(Y_test, Y_test_pred) * 100
    print("Logistic Regression Test Accuracy:", test_accuracy)

    # Calculate training accuracy
    Y_train_pred = best_model.predict(X_train)
    train_accuracy = accuracy_score(Y_train, Y_train_pred) * 100
    print("Logistic Regression Training Accuracy:", train_accuracy)

    model_filename = "logistic_regression.pkl"
    joblib.dump(best_model, model_filename)
    return train_accuracy, test_accuracy


data = preprocessing("3-class")
data['Horizontal_Signal'], data['Vertical_Signal'] = process_signals(data)
features = feature_extraction(data)
# print(f"wavelet horizontal:\n{features["wavelet"][0]}\nhorizontal PSD:\n{features["PSD"][0]}")

x_horizontal_wavelet_array = features["wavelet"][0]
x_vertical_wavelet_array = features["wavelet"][1]
x_horizontal_PSD = features["PSD"][0]
X_vertical_PSD = features["PSD"][1]

# combine wavelet and split
X_combined_wavelet = np.concatenate((x_vertical_wavelet_array, x_horizontal_wavelet_array), axis=1)
x_train_wavelet, x_test_wavelet, y_train_wavelet, y_test_wavelet = train_test_split(X_combined_wavelet,
                                                                                    data['Eye_Movement'],
                                                                                    test_size=0.2,
                                                                                    random_state=4)  # training and test data division

# combine PSD and split
X_combined_PSD = np.concatenate((x_horizontal_PSD[:, 1], X_vertical_PSD[:, 1]), axis=1)
x_train_PSD, x_test_PSD, y_train_PSD, y_test_PSD = train_test_split(X_combined_PSD, data['Eye_Movement'],
                                                                    test_size=0.2,
                                                                    random_state=4)  # training and test data division

# combine Wavelet and PSD features
X_combined_wavelet_PSD = np.concatenate((X_combined_wavelet, X_combined_PSD), axis=1)
x_train_combined_wavelet_PSD, x_test_combined_wavelet_PSD, y_train_combined_wavelet_PSD, y_test_combined_wavelet_PSD = train_test_split(
    X_combined_wavelet_PSD, data['Eye_Movement'], test_size=0.2,
    random_state=4)  # training and test data division

# classify wavelet features only
print("SVM classification using wavelet features")
SVM_classification(x_train_wavelet, y_train_wavelet, x_test_wavelet, y_test_wavelet)
print("SVM classification using PSD features")
SVM_classification(x_train_PSD, y_train_PSD, x_test_PSD, y_test_PSD)
print("SVM classification using PSD+Wavelet features")
SVM_classification(x_train_combined_wavelet_PSD, y_train_combined_wavelet_PSD, x_test_combined_wavelet_PSD,
                   y_test_combined_wavelet_PSD)

print("--------------------------------------------------------------------")
print("Random Forest classification using wavelet features")
Random_Forest_classification(x_train_wavelet, y_train_wavelet, x_test_wavelet, y_test_wavelet)
print("Random Forest classification PSD features")
Random_Forest_classification(x_train_PSD, y_train_PSD, x_test_PSD, y_test_PSD)
print("Random Forest classification using PSD+Wavelet features")
Random_Forest_classification(x_train_combined_wavelet_PSD, y_train_combined_wavelet_PSD, x_test_combined_wavelet_PSD,
                             y_test_combined_wavelet_PSD)
print("--------------------------------------------------------------------")

