#---------------------------------------------------------------------------------------------------#
# File name: helpers_ml.py                                                                          #
# Autor: Chrissi2802                                                                                #
# Created on: 21.12.2022                                                                            #
#---------------------------------------------------------------------------------------------------#
# This file provides auxiliary classes and functions for machine learning.
# Exact description in the functions.


import numpy as np
import pandas as pd
from scipy import stats, signal


def statistical_feature_engineering(df, column):
    """This function adds statistical features to the existing data set.
       Inspired by: https://towardsdatascience.com/feature-engineering-on-time-series-data-transforming-signal-data-of-a-smartphone-accelerometer-for-72cbe34b8a60
    
    Args:
        df (pandas DataFrame): Dataset
        column (string): Name of the column containing the data

    Returns:
        df (pandas DataFrame): Extended dataset
    """

    # Feature engineering for data
    df[column + "_mean"] = df[column].apply(lambda x: np.mean(np.float64(x)))   # mean
    df[column + "_std"] = df[column].apply(lambda x: np.std(np.float64(x)))     # std dev
    df[column + "_mad"] = df[column].apply(lambda x: np.mean(np.absolute(np.float64(x) - np.mean(np.float64(x)))))  # mean absolute difference
    df[column + "_max"] = df[column].apply(lambda x: np.max(np.float64(x)))     # maximum
    df[column + "_min"] = df[column].apply(lambda x: np.min(np.float64(x)))     # minimum
    df[column + "_max_min_diff"] = df[column + "_max"] - df[column + "_min"]    # max-min difference, range
    df[column + "_median"] = df[column].apply(lambda x: np.median(np.float64(x)))   # median
    df[column + "_mad"] = df[column].apply(lambda x: np.median(np.absolute(np.float64(x) - np.median(np.float64(x)))))  # median absolute difference
    df[column + "_iqr"] = df[column].apply(lambda x: np.percentile(np.float64(x), 75) - np.percentile(np.float64(x), 25))   # interquartile range
    df[column + "_pos_count"] = df[column].apply(lambda x: np.sum(np.float64(x) >= 0.0))    # positive count
    df[column + "_neg_count"] = df[column].apply(lambda x: np.sum(np.float64(x) < 0.0))     # negative count
    df[column + "_tot_count"] = df[column + "_pos_count"] + df[column + "_neg_count"]       # total count
    df[column + "_above_mean"] = df[column].apply(lambda x: np.sum(np.float64(x) > np.mean(np.float64(x)))) # values above mean
    df[column + "_peak_count"] = df[column].apply(lambda x: len(signal.find_peaks(np.float64(x))[0]))       # number of peaks
    df[column + "_skewness"] = df[column].apply(lambda x: stats.skew(np.float64(x)))        # skewness
    df[column + "_kurtosis"] = df[column].apply(lambda x: stats.kurtosis(np.float64(x)))    # kurtosis
    df[column + "_energy"] = df[column].apply(lambda x: np.sum(np.float64(x)**2) / 100.0)   # energy
    df[column + "_sma"] = df[column].apply(lambda x: np.sum(np.absolute(np.float64(x)) / 100.0))    # signal magnitude area

    # Feature engineering for indices
    df[column + "_argmax"] = df[column].apply(lambda x: np.argmax(np.float64(x)))   # index of max value
    df[column + "_argmin"] = df[column].apply(lambda x: np.argmin(np.float64(x)))   # index of min value
    df[column + "_arg_diff"] = np.absolute(df[column + "_argmax"] - df[column + "_argmin"]) # absolute difference between above indices
    
    return df


if (__name__ == "__main__"):
    
    # Test data
    df = pd.DataFrame({"Size": [15, 20, 25], 
                       "Measured": [[1, 2, 3], [4, 5, 6, 7], [8, 9]]})

    columns = ["Measured"]
    for column in columns:
        df = statistical_feature_engineering(df, column)
    
