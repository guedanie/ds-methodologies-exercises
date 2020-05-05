#Create split_scale.py that will contain the functions that follow.
#Each scaler function should create the object, fit and transform both train and test.
#They should return the scaler, train dataframe scaled, test dataframe scaled.
# Be sure your indices represent the original indices from train/test, as those represent the indices from the original dataframe.
# Be sure to set a random state where applicable for reproducibility!

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, QuantileTransformer, PowerTransformer, RobustScaler, MinMaxScaler


# We isolate our X and y variables for
train_pct = .8

def pull_X_y(train, test, y):
    X_train = train.drop(columns=y)
    y_train = train[[y]]
    X_test = test.drop(columns=y)
    y_test = test[[y]]
    return X_train, y_train, X_test, y_test
    

# Function used to split the data. Although we do produce 4 new datasets (X["train", "test"] and y["train","test"])
def split_my_data(X, y, train_pct):
    X_train, X_test, y_train, y_test = train_test_split(X, y,train_size=train_pct, random_state = 123)
    return X_train, X_test, y_train, y_test

def split_my_df(df):
    train, test = train_test_split(df, train_size=.8, random_state=123)
    return train, test

# Helper function used to updated the scaled arrays and transform them into usable dataframes
def return_values(scaler, train, test):
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, test_scaled

# Linear Scaler
def standard_scaler(train, test):
    scaler = StandardScaler().fit(train)
    scaler, train_scaled, test_scaled = return_values(scaler, train , test)
    return scaler, train_scaled, test_scaled

# Key function used to reverse scaling
def scale_inverse(scaler, train_scaled, test_scaled):
    train_unscaled = pd.DataFrame(scaler.inverse_transform(train_scaled), columns=train_scaled.columns.values).set_index([train_scaled.index.values])
    test_unscaled = pd.DataFrame(scaler.inverse_transform(test_scaled), columns=test_scaled.columns.values).set_index([test_scaled.index.values])
    return train_unscaled, test_unscaled

# Non-linear
def uniform_scaler(train, test, uniform=True):
    if uniform:
        scaler = QuantileTransformer(output_distribution="uniform").fit(train)
        scaler, train_scaled, test_scaled = return_values(scaler, train , test)
        return scaler, train_scaled, test_scaled
    else:
        scaler = QuantileTransformer(output_distribution="normal").fit(train)
        scaler, train_scaled, test_scaled = return_values(scaler, train , test)
        return scaler, train_scaled, test_scaled

# Non-linear
def gaussian_scaler(train, test, positive_negative=True):
    if positive_negative:
        scaler = PowerTransformer(method="yeo-johnson").fit(train)
        scaler, train_scaled, test_scaled = return_values(scaler, train , test)
        return scaler, train_scaled, test_scaled
    else: 
        scaler = PowerTransformer(method="box-cox").fit(test)
        scaler, train_scaled, test_scaled = return_values(scaler, train , test)
        return scaler, train_scaled, test_scaled

# Linear scaler
def min_max_scaler(train, test):
    scaler = MinMaxScaler().fit(train)
    scaler, train_scaled, test_scaled = return_values(scaler, train , test)
    return scaler, train_scaled, test_scaled

# Linear scaler
def iqr_robust_scaler(train, test):
    scaler = RobustScaler().fit(train)
    scaler, train_scaled, test_scaled = return_values(scaler, train , test)
    return scaler, train_scaled, test_scaled
