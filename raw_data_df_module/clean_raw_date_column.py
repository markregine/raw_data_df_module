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


def fill_missing_date_information_with_nat(S, regex ="none", missing_dates=[None, '']):
    """Takes a dataframe and the column names that are dates and replaces 'junk' with pd.NaT """
    m1 = S.isin(missing_dates)
    m2 = S.astype(str).str.strip() == ''
    m3 = S.astype(str).str.strip().str.contains(regex, case=False)

    for i in [m1, m2, m3]:
        t = S.copy()
        t[i] = pd.NaT
        S = t
    return S

def clean_dates(S, replace=[], max_date='2030-01-01'):
    """ Add parameter replace  
        ---------------------------
        S: series of dates.  
        replace: list of values to replace with the max_date.  
        max_date: default value = '2030-01-01'.  
    """
    try:
        s = pd.to_datetime(S).copy()
        return s
    except ValueError:
        try:
            print('All elements could not convert to datetime objects.\n    Filling "missing" elements with NaT and trying again.')
            s = fill_missing_date_information_with_nat(S)
            s = pd.to_datetime(s)
            return s
        except ValueError:
            ## List the records that could not convert
            errors_coerced = pd.to_datetime(s, errors='coerce')
            if replace == []:
                raise NameError('Here is a pd.Series of strings that would not convert to datetime objects.  Use the replace parameter.',  s[errors_coerced.isnull()])
            try:
                ## List the records that could not convert
                m = s.isin(replace)
                s[m] = max_date
                return pd.to_datetime(s)
            except:
                print("    Replaced elements in replace parameter.\n That was the LAST TRY in the program.")