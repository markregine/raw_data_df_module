## Raw data files

import pandas as pd
import numpy as np

def get_excel_file_object_and_list_containing_worksheet_names_from_excel_file(path):
    """  
        Takes one parameter, the path to the excel file of interest.  
        Returns a tuple, containing a pd.ExcelFile object and a list of the worksheets in that excel file.  
    """
    excel_file = pd.ExcelFile(path)

    sheet_names = excel_file.sheet_names
    print(sheet_names)
    
    return excel_file, sheet_names


def strip_white_space_from_columns_of_dtype_str(df):
    """ Takes one parameter, a dataframe. """
    for i in df.select_dtypes([object]).columns:
        m = df[i].dropna().index
        df.loc[m, i] = df.loc[m, i].astype(str).str.strip()
        del m, i
    return df


def replace_white_space_in_column_names_with_and_underscore(df):
    """ Takes one parameter, the dataframe. """
    with_replacement = [i.replace(' ', '_') for i in df.columns]
    df.columns = with_replacement
    return df

def drop_columns_from_dataframe_if_all_elements_are_nan(df, elements_list=['', '']):
    """ Takes two parameters:  
        df: Dataframe  
        elements_list: By default it will identify np.nan. If you want to add additional elements, as an example, you can do this ['', ' ']  
    """
    m = df.applymap(lambda i: i if i not in elements_list else np.nan).apply(lambda c: c.isnull().all())
    columns_to_drop = df.columns[m]
    df.drop(columns_to_drop, axis=1, inplace=True)
    return df