#---------------------------------------------------------------------------------------------------#
# File name: classifier_regressor_test.py                                                           #
# Autor: Chrissi2802                                                                                #
# Created on: 19.12.2022                                                                            #
#---------------------------------------------------------------------------------------------------#
# This file provides the all sklearn classifier and regressor.
# Exact description in the functions.


import numpy as np
from lazypredict.Supervised import LazyClassifier, LazyRegressor
from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold, GridSearchCV
from sklearn.preprocessing import RobustScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline


def scale_data(x_train, x_test, scaler = RobustScaler()):
    """This function scales the training data and, based on it, the test data.

    Args:
        x_train (numpy array): Training data
        x_test (numpy array): Test data
        scaler (sklearn scaler, optional): Scaler to be used from sklearn. Defaults to RobustScaler().

    Returns:
        x_train_scaled (numpy array): Scaled training data
        x_test_scaled (numpy array): Scaled test data
        scaler (sklearn scaler): parameterized scaler
    """
    
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)
    
    return x_train_scaled, x_test_scaled, scaler


def sklearn_classification(x, y):
    """This function executes the lazy classifier. This tests all sklearn models for classification and outputs the accuracy on console. 
       An automatic train test split is performed. No hyperparameter optimization is performed.

    Args:
        x (numpy array): Training and test data
        y (numpy array): Training and testing labels
    """
    
    # Train test split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 28)

    # Scale data
    x_train_scaled, x_test_scaled, scaler = scale_data(x_train, x_test)
    
    # Classification
    classifier = LazyClassifier(verbose = 0,ignore_warnings = True, custom_metric = None)
    models, predictions = classifier.fit(x_train_scaled, x_test_scaled, y_train, y_test)

    print(models)
    
    
def sklearn_regression(x, y):
    """This function executes a lazy regressor. This tests all sklearn models for regression and outputs the error on console.
       An automatic train test split is performed. No hyperparameter optimization is performed.

    Args:
        x (numpy array): Training and test data
        y (numpy array): Training and testing labels
    """
    
    # Train test split
    offset = int(x.shape[0] * 0.8)
    x_train, y_train = x[:offset], y[:offset]
    x_test, y_test =x[offset:], y[offset:]

    # Regression
    regressor = LazyRegressor(verbose = 0, ignore_warnings = True, custom_metric = None)
    models, predictions = regressor.fit(x_train, x_test, y_train, y_test)

    print(models)


def grid_search_knc(x, y):
    """This function searches for the best hyperparameters for the KNeighborsClassifier model.

    Args:
        x (numpy array): Training and test data
        y (numpy array): Training and testing labels

    Returns:
        best_params (dictionary): Name of the tested parameter with the best value
    """
    
    scaler = RobustScaler()
    knc = KNeighborsClassifier()

    # Link them together by using sklearn's pipeline
    pipeline = Pipeline(steps = [("scaler", scaler), ("knc", knc)])

    # Because we are using a pipeline we need to prepend the parameters with the name of the
    # class of instance we want to provide the parameters for.
    param_grid = [
        {
            "knc__n_neighbors": [2, 5, 10],
            "knc__weights": ["uniform", "distance"],
            "knc__algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
            "knc__p": [1, 2]
        }
    ]
    
    # Using crossvalidation
    repeated_kfolds = RepeatedStratifiedKFold(n_splits = 5, n_repeats = 5)

    # Search for the best hyperparameters
    search = GridSearchCV(
        pipeline,
        param_grid,
        scoring = "accuracy",
        cv = repeated_kfolds,
        n_jobs = -1,
        return_train_score = False,
        verbose = 1,
        error_score = "raise"
    )

    search.fit(x, y)

    print("CV score: %0.2f" % search.best_score_)
    print("Best parameters:", search.best_params_)

    return search.best_params_


if (__name__ == "__main__"):
    
    from sklearn.datasets import load_breast_cancer, load_boston
    from sklearn.utils import shuffle
    
    # Classification
    dataset_classification = load_breast_cancer()
    x_classification = dataset_classification.data
    y_classification = dataset_classification.target
    
    sklearn_classification(x_classification, y_classification)
    
    # Regression
    dataset_regression = load_boston()
    x_regression, y_regression = shuffle(dataset_regression.data, dataset_regression.target, random_state = 28)
    x_regression = x_regression.astype(np.float32)
    
    sklearn_regression(x_regression, y_regression)
    
    # Hyperparameter optimization for KNeighborsClassifier = knc
    knc_params = grid_search_knc(x_classification, y_classification)
    
    