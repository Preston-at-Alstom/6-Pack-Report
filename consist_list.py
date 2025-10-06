
import pandas as pd


def to_df(file_name):
    

    header_names = [
                    'AM Train Number',
                    ' ',
                    'AM Departure Track',
                    'AM Departure Time',
                    'AM Yarding as',
                    'AM Arrival',
                    'PM Train Number',
                    '  ',
                    'PM Departure Track',
                    'PM Departure Time',
                    'PM Yarding as',
                    '   ',
                    'PM Yarding station',
                    'Consist Number',
                    'Loco',
                    'Coaches',
                    'Cab Car',
                    'Consist Size'
    ]

    sheet = 'CSA TRANSFER'


    return pd.read_excel(file_name, sheet_name = sheet, skiprows = 9, header = None, names = header_names, 
                         dtype={'AM Departure Time' : 'Int32', 'Cab Car': 'Int32', 'Loco' : 'Int32', 'Consist Number': 'Int32'})


def get_consists(df):

    # remove duplicate trains
    AM_consists = list(set(df['AM Train Number'].tolist()))    
    PM_consists = list(set(df['PM Train Number'].tolist())) 

    # Combine consists from AM and PM dispatch
    return AM_consists + PM_consists