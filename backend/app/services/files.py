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

def generateUTMData(df:pd.DataFrame, cols:dict) -> list[UTMData]:
    """
    Generates a list of UTMData objects

    Parameters
    ----------
    df : pandas dataframe
    cols : dict of columns with UTM coordinates

    Returns
    -------
    utmData : list of UTMData objects
    """
    #Change columns types
    df = df.astype({cols["easting"]: float, cols["northing"]: float, cols["zone_number"]: int, cols["zone_letter"]: str})
    utmData = []
    for _, row in df.iterrows():
        try:
            utmData.append(UTMData(
                easting=row[cols["easting"]],
                northing=row[cols["northing"]],
                zone_number=row[cols["zone_number"]],
                zone_letter=row[cols["zone_letter"]]
            ))
        except Exception as e:
            raise Exception(f"Error of data on number row:  {row[0]} to UTM {e}")
    return utmData


def insertGEOData(
    df: pd.DataFrame,
    cols: dict,
    nameLatitude: str,
    nameLongitude: str
) -> pd.DataFrame:
    """
    Inserts GEO data into a dataframe that
    receives a list of UTMData objects and
    converts them to latitude and longitude

    Parameters
    ----------
    df : pandas dataframe
    utmData : list of UTMData objects
    nameLatitude : str
    nameLongitude : str

    Returns
    -------
    df : pandas dataframe with latitude and longitude columns
    """
    utmDataList = generateUTMData(df, cols)
    for column, utmData in zip(df.columns, utmDataList):
        lat, lon = utm_to_latlong(utmData)
        df.at[0, column][nameLatitude] = lat
        df.at[0, column][nameLongitude] = lon
    return df


