import pandas as pd
import numpy as numpy
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

import acquire

def create_month_day_columns(df):
    df["day_of_week"] = df.index.day_name()
    df["month"] = df.index.month_name()
    return df

def add_total_sales_column(df):
    df["sales_total"] = df.sale_amount * df.item_price
    return df

def add_previous_sales_column(df):
    df["previous_sales_diff"] = df.sale_amount.diff(1)
    return df

def prepare_sales_data(df):
    df = create_month_day_columns(df)
    df = add_previous_sales_column(df)
    df = add_total_sales_column(df)

    df = (df.astype({'sale_id': object, 
                    'store': object, 
                    'store_zipcode': object, 
                    'item_id': object, 
                    'item_upc12': object, 
                    'item_upc14': object, 
                    'month': 'category', 
                    'day_of_week': 'category'}))
    
    return df

# ____ Main Prep Function ___ # 
def wrangle_sales_data():
    df = acquire.read_sales_data()
    df = prepare_sales_data(df)
    return df


def split_time_data_ptc(df, ptc):
    # Percentage-Based
    train_size = ptc
    n = df.shape[0]
    test_start_index = round(train_size * n)

    train = df[:test_start_index] # everything up (not including) to the test_start_index
    test = df[test_start_index:] # everything from the test_start_index to the end
    
    return train, test

def plot_splits(train, validate, test, target_variable):
    sns.lineplot(data=train, x=train.index, y= target_variable)
    sns.lineplot(data=validate, x=validate.index, y= target_variable)
    sns.lineplot(data=test, x=test.index, y= target_variable)

# ----------------------- #
#   Prepare Energy Data   #
# ----------------------- #

def prepped_energy():
    """
    Function the acquires and returns 
    a prepared df for the OPS German Energy data
    and displays historgrams for numeric columns
    """
    # Acquire Datetime df
    gdf = acquire.german_energy_csv()
    
    # Create new date part columns as category dtypes
    gdf['month'] = gdf.index.month.astype('category')
    gdf['year'] = gdf.index.year.astype('category')
    
    # Plot numeric column distributions
    numeric_hists(gdf)
    
    return gdf

