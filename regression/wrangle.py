# Throughout the exercises for Regression in Python lessons, you will use the following example scenario: As a customer analyst, I want to know who has spent the most money with us over their lifetime. I have monthly charges and tenure, so I think I will be able to use those two attributes as features to estimate total_charges. I need to do this within an average of $5.00 per customer.

# The first step will be to acquire and prep the data. Do your work for this exercise in a file named wrangle.py.

# Acquire customer_id, monthly_charges, tenure, and total_charges from telco_churn database for all customers with a 2 year contract.
# Walk through the steps above using your new dataframe. You may handle the missing values however you feel is appropriate.
# End with a python file wrangle.py that contains the function, wrangle_telco(), that will acquire the data and return a dataframe cleaned with no missing values.

import pandas as pd 
import numpy as np 
from env import sql_database

sql = '''
SELECT customer_id, `monthly_charges`, tenure, total_charges
FROM customers
WHERE contract_type_id = 3
;
'''

def months_to_years(tenure_months, df):
    df["tenure_years"] = (df[tenure_months] / 12).round() - 1
    customers["tenure_years_bins"]= pd.cut(customers.tenure_years, 3, labels=["1 year or less", "1 to 3 years", "3 to 5 years"])
    return df

def create_bins_monthly_charges(dataframe):
    dataframe["monthly_charges_bins"] = pd.cut(dataframe.monthly_charges, 3, labels=["low", "medium", "high"])

def wrangle_telco():
    '''
    Function use to pull the "telco_churn" dataset from sql and 
    returns a dataframe with clean data, and the columns
    "customer_id", "monthly_charges", "tenure", "total_charges"
    
    '''

    customers = sql_database("telco_churn", sql)
    customers[customers["total_charges"].str.contains(' ')]
    customers = customers.replace(' ', np.nan)
    customers = customers.dropna()
    customers.total_charges = customers["total_charges"].astype(float)
    customers["tenure_years"] = (customers["tenure"] / 12).round() - 1
    customers["tenure_years_bins"]= pd.cut(customers.tenure_years, 3, labels=[">= 1", "1 > x <= 3", "<=5 "])
    customers["monthly_charges_bins"] = pd.cut(customers.monthly_charges, 3, labels=["Low", "Medium", "High"])
    return customers
