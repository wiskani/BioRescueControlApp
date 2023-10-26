import pandas as pd
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import List, Any

from app.services.system_coordinate import utm_to_latlong
from app.schemas.services import  UTMData

from app.crud.species import get_specie_by_name
from app.crud.rescue_herpetofauna import get_mark_herpetofauna_by_number


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
    try:
        df = df.astype({cols["easting"]: float, cols["northing"]: float, cols["zone_number"]: int, cols["zone_letter"]: str})
    except Exception as e:
        raise Exception(f"Error changing columns types: {e}")
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
    latitude = []
    longitude = []

    for utmData in utmDataList:
       lat, long = utm_to_latlong(utmData)

       # Apend lat and long to list
       latitude.append(lat)
       longitude.append(long)

    # add  latitude and longitude columns
    df[nameLatitude] = latitude
    df[nameLongitude] = longitude

    return df

async def addIdSpecieByName(
    db: AsyncSession,
    df: pd.DataFrame,
    col: str,
) -> tuple[pd.DataFrame, list[tuple[int, str]]]:
    """
    Adds the id of a specie to a dataframe

    Parameters
    ----------
    df : pandas dataframe
    col : str with name of column with specie name

    Returns
    -------
    df : pandas dataframe with idSpecie column
    """
    listNameSpecieNumberRow: list[tuple[int, str]] = []
    colunmId: list[int | None] = []

    for _, row in df.iterrows():
        specie = await get_specie_by_name(db, row[col])
        if specie is None:
            listNameSpecieNumberRow.append((row[0], row[col]))
            colunmId.append(None)
        else:
            colunmId.append(specie.id)

    df['idSpecie'] = colunmId

    return df, listNameSpecieNumberRow

async def addMarkIdByNumber(
    db: AsyncSession,
    df: pd.DataFrame,
    col: str,
) -> tuple[pd.DataFrame, list[tuple[int, str]]]:
    """
    Adds the id of a mark to a dataframe

    Parameters
    ----------
    db : AsyncSession
    df : pandas dataframe
    col : str with name of column with mark number

    Returns
    -------
    df : pandas dataframe with idMark column
    """
    listMarkNumberRow: list[tuple[int, str]] = []
    colunmId: list[int | None] = []

    for _, row in df.iterrows():
        mark = await get_mark_herpetofauna_by_number(db, row[col])
        if mark is None:
            listMarkNumberRow.append((row[0], row[col]))
            colunmId.append(None)
        else:
            colunmId.append(mark.id)

    df['idMark'] = colunmId

    return df, listMarkNumberRow



