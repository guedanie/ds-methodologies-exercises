import pandas as pd
from pydataset import data
import split_scale

import sklearn.impute
import sklearn.model_selection
import sklearn.preprocessing


# --------------------- #
#       Iris DF         #
# ----------------------#

def drop_columns_iris(df):
    return df.drop(columns=[
        "species_id",
        "measurement_id"
        
    ])

def rename_columns(df):
    return df.rename(columns = {"species_name" : "species"})

def encode_iris(train, test):
    encoder = sklearn.preprocessing.OneHotEncoder()

    encoder.fit(train[["species"]])

    m = encoder.transform(train[["species"]]).todense()

    train = pd.concat([train, pd.DataFrame(m, columns=encoder.categories_[0], index=train.index)], axis = 1).drop(columns="species")

    m = encoder.transform(test[["species"]]).todense()

    test = pd.concat([test, pd.DataFrame(m, columns=encoder.categories_[0], index=test.index)], axis = 1).drop(columns="species")
    
    return train, test

def prep_iris(df):
    df = drop_columns_iris(df)
    df = rename_columns(df)
    train, test = sklearn.model_selection.train_test_split(df, random_state=123, train_size= .8)
    train, test = encode_iris(train, test)
    return train, test


# --------------------- #
#       Titanic DF      #
# ----------------------#

def fill_na_values(df):
    df.embark_town = df.embark_town.fillna(df.embark_town.value_counts().head(1).index[0])
    df.embarked = df.embarked.fillna(df.embarked.value_counts().head(1).index[0])
    return df 

def drop_columns_titanic(df):
    df = df.drop(columns="deck")
    return df

def encode_titanic(train, test):
    encoder = sklearn.preprocessing.OneHotEncoder()

    encoder.fit(train[["embarked"]])

    m = encoder.transform(train[["embarked"]]).todense()

    train = pd.concat([train, pd.DataFrame(m, columns=encoder.categories_[0], index=train.index)], axis = 1).drop(columns="embarked")

    m = encoder.transform(test[["embarked"]]).todense()

    test = pd.concat([test, pd.DataFrame(m, columns=encoder.categories_[0], index=test.index)], axis = 1).drop(columns="embarked")

    return train, test

def impude_titanic(train, test):
    imputer = sklearn.impute.SimpleImputer(strategy = "mean")
    imputer.fit(train[["age"]])
    train.age = imputer.transform(train[["age"]])
    test.age = imputer.transform(test[["age"]])
    return train, test

def scale_titanic(train, test):
    X_train = train[["age", "fare"]]
    X_test = test[["age", "fare"]]
    scaler, train_scaled, test_scaled = split_scale.min_max_scaler(X_train, X_test)
    return scaler, train_scaled, test_scaled

def prep_titanic(df):
    df = fill_na_values(df)
    df = drop_columns_titanic(df)
    train, test = sklearn.model_selection.train_test_split(df, random_state=123, train_size = .8)
    train, test = encode_titanic(train, test)
    train, test = impude_titanic(train, test)
    scaler, train_scaled, test_scaled = scale_titanic(train, test)
    return scaler, train_scaled, test_scaled