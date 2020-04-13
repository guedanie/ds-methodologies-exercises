# get_titanic_data: returns the titanic data from the 
# codeup data science database as a pandas data frame.

from env import sql_database
import pandas as pd
import numpy as np

def get_titanic_data():
    query = '''
    SELECT * 
    FROM passengers
    ;
    '''
    database = "titanic_db"

    titanic = sql_database(database, query)

    return titanic




# get_iris_data: returns the data from the iris_db on the codeup data science database as a pandas data frame. 
# The returned data frame should include the actual name of the species in addition to the species_ids.

def get_iris_data():
    query = '''
    SELECT * 
    FROM measurements
    JOIN species USING (species_id)
    ;
    '''
    database = "iris_db"

    iris = sql_database(database, query)

    return iris