import pandas as pd
import numpy as np
import datetime as datetime
from dateutil.parser import parse
import re as re


def get_date_columns_from_df(df, strings_indicating_dates='date|dt', case=False):
    column_names = pd.Series(df.columns)
    m = column_names.str.contains(strings_indicating_dates, case=case)
    date_columns = column_names[m]
    date_columns.index.name = 'position'
    date_columns.name = 'column_name'
    return date_columns


def fill_missing_date_information_with_nat(S, regex ="\s+|none", isin=[None, ''], max_date=('2030', '01', '01')):
    """Takes a dataframe and the column names that are dates and replaces 'junk' with pd.NaT """
    m1 = S.isin(isin)
    m2 = S.astype(str) == ''
    m3 = S.astype(str).str.strip().str.contains(regex, case=False)

    for i in [m1, m2, m3]:
        t = S.copy()
        t[i] = pd.NaT
        S = t
    return S


def get_date_format(S):
    """ """
    list_of_date_formats = S.astype(str).str.split('-').map(lambda l: ''.join([str(len(i)) for i in l])).tolist()
    date_formats = list(set(list_of_date_formats)) ## There should only be one date format 
    try:
        date_format = pd.Series(date_formats)[pd.Series(['Test if only one item returned, if not, raise error']).notnull()][0]
        if date_format == '422':
            return "Ymd"
        elif date_format == '224':
            return "mdY"
        else:
            return "Unknown date format found."
    except:
        print("More then one date format for a single column was found.")
        print(date_formats)

    
def get_date_format_from_samples(S):
    """ Returns the format code for this date column.  
        If you take the date 9, 9, 1999 and sum the numbers, this should be the largest we would expect any to be: 48 """
    if S.isnull().all():
        return S
    else:
        sum_of_individaul_numbers_in_date = S.dropna().map(lambda x: re.findall(r"\d", x)).map(lambda l: sum([int(n) for n in l]))

    m = sum_of_individaul_numbers_in_date < 48
    dates_to_test_format = S.dropna()[m].map(lambda i: parse(i))
    date_format = get_date_format(S=dates_to_test_format)
    return date_format


def change_bad_date_if_its_9999999(S, current_formated_as, max_year='2030', max_month='01', max_date='01'):
    """"""
    m = (S == '99999999')
    if current_formated_as == 'Ymd':
        S[m] = ''.join([max_year, max_month, max_date])
        return S
    elif current_formated_as == 'mdY':
        S[m] = ''.join([max_month, max_date, max_year]) 
        return 
    else:
        print('WARNING!')
   

def try_to_format_date(date_text):
    """ """
    try:
        return datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        try:
            return datetime.datetime.strptime(date_text, '%Y%m%d')
        except ValueError:
            try:
                return datetime.datetime.strptime(date_text, '%m-%d-%Y')
            except ValueError:
                try:
                    return datetime.datetime.strptime(date_text, '%m/%d/%Y')
                except ValueError:
                    print("Time to add more code to function!") 
   
                    
def string_date_to_datetime(S):
    s = fill_missing_date_information_with_nat(S)  
    s = change_bad_date_if_its_9999999(s, get_date_format_from_samples(s))
    return pd.to_datetime(s)