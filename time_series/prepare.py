import pandas as pd
import numpy as numpy
import seaborn as sns
import matplotlib.pyplot as plt

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
    return df

def wrangle_sales_data():
    df = acquire.read_compiled_data()
    df = prepare_sales_data(df)
    return df