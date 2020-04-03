# Create a file, explore.py, that contains the following functions for exploring your variables (features & target).

# Write a function, plot_variable_pairs(dataframe) that plots all of the pairwise relationships along with the regression line for each pair.

# Write a function, months_to_years(tenure_months, df) that returns your dataframe with a new feature tenure_years, in complete years as a customer.

# Write a function, plot_categorical_and_continous_vars(categorical_var, continuous_var, df), 
# that outputs 3 different plots for plotting a categorical variable with a continuous variable, e.g. tenure_years with total_charges. 
# For ideas on effective ways to visualize categorical with continuous: https://datavizcatalogue.com/. 
# You can then look into seaborn and matplotlib documentation for ways to create plots.

import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import warnings
warnings.filterwarnings("ignore")

import env
import wrangle
import split_scale

# Functions to create new categorical features
def months_to_years(tenure_months, df):
    df["tenure_years"] = (df[tenure_months] / 12).round() - 1
    customers["tenure_years_bins"]= pd.cut(customers.tenure_years, 3, labels=["1 year or less", "1 to 3 years", "3 to 5 years"])
    return df

def create_bins_monthly_charges(dataframe):
    dataframe["monthly_charges_bins"] = pd.cut(dataframe.monthly_charges, 3, labels=["low", "medium", "high"])

# Functions for visualization

def plot_variable_pairs(dataframe, hue=None, kind="reg"):
    sns.pairplot(dataframe, hue=hue, kind=kind, plot_kws={'line_kws':{'color':'red'}, 'scatter_kws': {'alpha': 0.5}})


def create_jointplot(dataframe, x, y):
    sns.jointplot(dataframe.x,dataframe.y, data=dataframe, kind="reg")


def plot_categorical_and_continous_vars(categorical_var, continuous_var, df):
    figure, axes = plt.subplots(1,4, figsize=(16,8))
    sns.boxplot(categorical_var, continuous_var, data=df, ax=axes[3])
    sns.barplot(x=categorical_var, y=continuous_var, data=df, ax=axes[1])
    sns.swarmplot(x=categorical_var, y=continuous_var, data=df, ax=axes[2])
    sns.countplot(x=categorical_var, data=df, ax=axes[0])
    figure.tight_layout()
    plt.show()


