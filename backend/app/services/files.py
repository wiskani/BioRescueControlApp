import pandas as pd
from fastapi import HTTPException, status
from typing import List, Any

from app.services.system_coordinate import utm_to_latlong
from app.schemas.services import  UTMData

def convert_to_datetime(df:pd.DataFrame, cols:List[str]) -> pd.DataFrame:
    """
    Converts a column in a dataframe to datetime format

    Parameters
    ----------
    df : pandas dataframe
    cols : list of columns to convert to datetime

    Returns
    -------
    df : pandas dataframe with datetime columns on tz La_Paz
    """
    for col in cols:
        try:
            df[col] = pd.to_datetime(df[col])
            df[col] = df[col].dt.tz_localize('America/La_Paz')
        except:
            raise Exception(f"Error converting column {col} to datetime")
    return df

def remplace_nan_with_none(df:pd.DataFrame) -> pd.DataFrame:
    """
    Replaces NaN values with None

    Parameters
    ----------
    df : pandas dataframe

    Returns
    -------
    df : pandas dataframe with None values instead of NaN
    """
    # Replace NaN with None
    df = df.fillna('None')

    # chek if NaN is in df 
    if df.isnull().values.any():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must not contain NaN",
        )
    return df

def none_value(value) -> Any | None:
    """
    Replaces 'None' string with None

    Parameters
    ----------
    value : str

    Returns
    -------
    value : None or str
    """
    if value == 'None':
        return None
    else:
        return value

def convert_utm_to_latlong(df:pd.DataFrame, cols:List[str]) -> pd.DataFrame:
    """
    Converts UTM coordinates to latlong

    Parameters
    ----------
    df : pandas dataframe
    cols : list of columns to convert to latlong

    Returns
    -------
    df : pandas dataframe with latlong columns
    """
    for col in cols:
        try:
            df[col] = df.apply(lambda row: utm_to_latlong(row[col]), axis=1)
        except:
            raise Exception(f"Error converting column {col} to latlong")
    return df





