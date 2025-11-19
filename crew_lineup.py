import pandas as pd


def to_df(file):
    
    return pd.read_excel(file, sheet_name = 'Top', usecols= [0,2,3,4,5], dtype = {'Tour #' : 'Int32'})



