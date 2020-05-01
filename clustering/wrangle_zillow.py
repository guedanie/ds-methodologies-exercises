
from env import sql_database
import pandas as pd

# ~~~~~~~~~ Acquire ~~~~~~~~~~ #

# ----------------- #
#     Read SQL      #
# ----------------- #

query = '''

SELECT *
FROM properties_2017
JOIN (
	SELECT parcelid, `logerror`, max(transactiondate)
	FROM predictions_2017
	GROUP BY parcelid, logerror) predictions_2017 USING (parcelid)
LEFT JOIN `typeconstructiontype` USING (typeconstructiontypeid)
LEFT JOIN propertylandusetype USING (propertylandusetypeid)
LEFT JOIN airconditioningtype USING (airconditioningtypeid)
LEFT JOIN architecturalstyletype USING (architecturalstyletypeid)
LEFT JOIN buildingclasstype USING (buildingclasstypeid)
LEFT JOIN `heatingorsystemtype` USING (`heatingorsystemtypeid`)
LEFT JOIN storytype USING (`storytypeid`)
WHERE latitude IS NOT NULL AND longitude IS NOT NULL
;

'''

data_base_name = "zillow"

def run_query_to_csv():
    df = sql_database(data_base_name, query)
    df.to_csv("zillow_data.csv")

def read_zillow():
    df = pd.read_csv("zillow_data.csv")
    df.drop(columns= "Unnamed: 0", inplace=True)
    return df


# ~~~~~~~~~ Prep ~~~~~~~~~ #


# ------------------------- #
#    Find Missing Values    # 
# ------------------------- #

def find_missing_values_rows(df):
    num_rows_missing = df.isnull().sum()
    ptc_rows_missing = df.isnull().sum() / df.shape[0]
    new_df = pd.DataFrame({"num_rows_missing": num_rows_missing, "pct_rows_missing": ptc_rows_missing})
    return new_df

def find_missing_rows(df):
    num_cols_missing = df.isnull().sum(axis=1)
    pct_cols_missing = df.isnull().sum(axis=1) / df.shape[0] 
    num_rows = df.isnull().sum()

    n_columns = pd.DataFrame({"num_cols_missing": num_cols_missing, "ptc_cols_missing": pct_cols_missing, "num_rows": num_rows})
    return n_columns

# ----------------------- #
#       Imputting         #
# ----------------------- #

def remove_columns(df, cols_to_remove):  
    df = df.drop(columns=cols_to_remove)
    return df

def impude_unit_cnt(df):
    if df.propertylandusedesc == "Condominium" or df.propertylandusedesc == "Single Family Residential":
        return 1
    else:
        return 0

def handle_missing_values(df, prop_required_column = .5, prop_required_row = .75):
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df

def data_prep(df, cols_to_remove = [], prop_required_column=.5, prop_required_row=.75):
    # Remove any columns
    df = remove_columns(df, cols_to_remove)

    # df.heating 
    df.heatingorsystemdesc = df.heatingorsystemdesc.fillna(value="None")

    df = df.drop(columns="calculatedbathnbr")
    
    # Drop any rows with no bedroom or bathroom columns
    bath = df.bathroomcnt != 0
    bedroom = df.bedroomcnt != 0
    df = df[bedroom & bath]

    # Drop that aren't single units
    df.unitcnt = df.unitcnt.fillna(df.apply(lambda col: impude_unit_cnt(col), axis = 1))
    df = df[df.unitcnt == 1]

    df = handle_missing_values(df)
    
    # Drop duplicate `parcelid`
    df = df.drop_duplicates(subset="parcelid", keep="first")

    # Drop missing values for `calculatedfinishedsquarefeet`
    df.calculatedfinishedsquarefeet = df.calculatedfinishedsquarefeet.dropna()

    # Fill nan values for `lotsizesquarefeet` with mean
    df.lotsizesquarefeet = df.lotsizesquarefeet.fillna(df.lotsizesquarefeet.mean())

    # Fill nan values for `regionidcity` with mode
    df.regionidcity = df.regionidcity.fillna(value=df.regionidcity.mode()[0])

    # Fill nan values for `censustractandblock` with mode
    df.censustractandblock = df.censustractandblock.fillna(value=df.censustractandblock.mode()[0])

    # Drop remaining nan values
    df = df.dropna()

    return df