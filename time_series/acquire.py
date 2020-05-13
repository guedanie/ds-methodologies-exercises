import pandas as pd
import requests
import os

# ----------------------- #
#   Acquire Sales Data    #
# ----------------------- #

def get_store_data():
    response = requests.get('https://python.zach.lol/api/v1/stores')
    data = response.json()
    df_stores = pd.DataFrame(data["payload"]["stores"])
    return df_stores

def get_item_data():
    base_url = 'https://python.zach.lol'
    response = requests.get('https://python.zach.lol/api/v1/items')

    data = response.json()
    df = pd.DataFrame(data["payload"]["items"])
    
    for i in range(data["payload"]["max_page"] -1):
        response = requests.get(base_url + data['payload']['next_page'])
        data = response.json()
        df = pd.concat([df, pd.DataFrame(data['payload']['items'])]).reset_index()

    return df

def get_sales_data():
    
    base_url = 'https://python.zach.lol'
    # Create the first response 
    response = requests.get('https://python.zach.lol/api/v1/sales')
    # Parse the data as a json
    data = response.json()
    # Turn the first page into a df
    df_sales = pd.DataFrame(data["payload"]["sales"])

    for i in range(data['payload']['max_page']-1):
        response = requests.get(base_url + data['payload']['next_page'])
        data = response.json()
        df_sales = pd.concat([df_sales, pd.DataFrame(data['payload']['sales'])]).reset_index(drop=True)
    
    
    return df_sales

# __ Main Acquire Function __ #

def create_merged_report():
    # Create the individual df
    df_items = get_item_data()
    df_store = get_store_data()
    df_sales = get_sales_data()

    # Combine the df using merge
    df_sales_store = df_sales.merge(df_store, how="left", left_on="store", right_on="store_id")
    df_sales_store = df_sales_store.merge(df_items, how="left", left_on="item", right_on="item_id")

    # Drop duplicated columns
    df = df_sales_store.drop(columns=["level_0", "index","store_id"])

    # Change date dtype to DateTime
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    
    return df

# Read from csv
def read_sales_data():
    df = pd.read_csv("store_sales.csv", index_col="sale_date", parse_dates=True)
    df.drop(columns="Unnamed: 0", inplace=True)
    return df

# ----------------------- #
#   Acquire Energy Data   #
# ----------------------- #

def german_energy_csv():
    """
    This function returns a df with a datetime index
    using the opsd_germany url/csv.
    """
    if os.path.isfile('german_energy.csv'):
        df = pd.read_csv('german_energy.csv', parse_dates=True, index_col='Date').sort_index()
    else:
        url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
        df = pd.read_csv(url, parse_dates=True, index_col="Date").sort_index()
        df.to_csv('german_energy.csv')
    return df