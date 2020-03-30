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

sql_database("telco_churn", sql)

def wrangle_telco():
    customers = pd.read_sql(sql, url)
    customers[customers["total_charges"].str.contains(' ')]
    customers = customers.replace(' ', np.nan)
    customers = customers.dropna()
    customers.total_charges = customers["total_charges"].astype(float)
    return customers

# def wrangle_telco():
#     customers = pd.read_sql(sql, url)
#     customers[customers["total_charges"].str.contains(' ')]
#     customers = customers.replace(' ', np.nan)
#     customers = customers.dropna()
#     customers.total_charges = customers["total_charges"].astype(float)
#     # The commented lines below will only be needed if we want to munally calcualte total_chrages
#     # customers["total_charges_2"] = customers.tenure * customers.monthly_charges
#     # customers.drop(columns = ["total_charges"], inplace = True)
#     # customers = customers.rename(columns = {"total_charges_2": "total_charges"})
#     return customers