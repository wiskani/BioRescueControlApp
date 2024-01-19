import pytz
import pandas as pd
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import List, Any

from app.services.system_coordinate import utm_to_latlong
from app.schemas.services import  UTMData

from app.crud.species import (
    get_specie_by_name,
    get_genus_by_name,
    get_family_by_name
    )
from app.crud.rescue_herpetofauna import (
    get_mark_herpetofauna_by_number,
    get_age_group_name,
    get_all_age_groups,
    get_transect_herpetofauna_by_number,
    get_rescue_herpetofauna_by_number,
    get_transect_herpetofauna_translocation_by_cod,
    get_point_herpetofauna_translocation_by_cod,
    )

from app.crud.rescue_flora import (
    get_flora_rescue_zone,
    get_flora_rescue,
    get_flora_relocation_zone
)

from app.crud.rescue_mammals import (	
    get_habitat_name,
    get_site_release_mammal_name,
    get_rescue_mammal_cod
)


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
        print(df[col])
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
    # print dataframe columns: easting, northing, zone_number, zone_letter
    try:
        df = df.astype({
        cols["easting"]: 'float64',
        cols["northing"]: 'float64',
        cols["zone_number"]: 'Int64',  
        cols["zone_letter"]: 'str'
    })
    except Exception as e:
        raise Exception(f"Error changing columns types: {e}")
    utmData = []
    for _, row in df.iterrows():
        if pd.isna(row[cols["easting"]]) or pd.isna(row[cols["northing"]]) or pd.isna(row[cols["zone_number"]]) or pd.isna(row[cols["zone_letter"]]):
            utmData.append(None)
        else:
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
        if utmData is None:
            latitude.append(None)
            longitude.append(None)
        else:
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
    colId: str
) -> tuple[pd.DataFrame, list[tuple[int, str]]]:
    """
    Adds the id of a specie to a dataframe

    Parameters
    ----------
    df : pandas dataframe
    col : str with name of column with specie name
    colId : str with name of column to add id

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

    df[colId] = colunmId

    return df, listNameSpecieNumberRow

async def addIdGenusByName(
    db: AsyncSession,
    df: pd.DataFrame,
    col: str,
    colId: str
) -> tuple[pd.DataFrame, list[tuple[int, str]]]:
    """
    Adds the id of a genus to a dataframe

    Parameters
    ----------
    df : pandas dataframe
    col : str with name of column with genus name
    colId : str with name of column to add id

    Returns
    -------
    df : pandas dataframe with idGenus column
    """
    listNameGenusNumberRow: list[tuple[int, str]] = []
    colunmId: list[int | None] = []

    for _, row in df.iterrows():
        genus = await get_genus_by_name(db, row[col])
        if genus is None:
            listNameGenusNumberRow.append((row[0], row[col]))
            colunmId.append(None)
        else:
            colunmId.append(genus.id)

    df[colId] = colunmId

    return df, listNameGenusNumberRow

async def addIdFamilyByName(
    db: AsyncSession,
    df: pd.DataFrame,
    col: str,
    colId: str
) -> tuple[pd.DataFrame, list[tuple[int, str]]]:
    """
    Adds the id of a family to a dataframe

    Parameters
    ----------
    df : pandas dataframe
    col : str with name of column with family name
    colId : str with name of column to add id

    Returns
    -------
    df : pandas dataframe with idFamily column
    """
    listNameFamilyNumberRow: list[tuple[int, str]] = []
    colunmId: list[int | None] = []

    for _, row in df.iterrows():
        family = await get_family_by_name(db, row[col])
        if family is None:
            listNameFamilyNumberRow.append((row[0], row[col]))
            colunmId.append(None)
        else:
            colunmId.append(family.id)

    df[colId] = colunmId

    return df, listNameFamilyNumberRow

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
        if row[col] == "None":
            listMarkNumberRow.append((row[0], row[col]))
            colunmId.append(None)
        else:
            mark = await get_mark_herpetofauna_by_number(db, row[col])
            if mark is None:
                listMarkNumberRow.append((row[0], row[col]))
                colunmId.append(None)
            else:
                colunmId.append(mark.id)

    df['idMark'] = colunmId

    return df, listMarkNumberRow

async def addAgeGroupIdByName(
        db: AsyncSession,
        df: pd.DataFrame,
        col: str,
) -> tuple[pd.DataFrame, list[tuple[int, str]]]:
    """
    Adds the id of a age group to a dataframe

    Parameters
    ----------
    db : AsyncSession
    df : pandas dataframe
    col : str with name of column with age group name

    Returns
    -------
    df : pandas dataframe with idAgeGroup column
    """
    listAgeGroupNameRow: list[tuple[int, str]] = []
    colunmId: list[int | None] = []

    ageGroups = await get_all_age_groups(db)

    for index, row in df.iterrows():
        for agegroup in ageGroups:
            data_age = row[col]
            age_name = agegroup.name

            if data_age.lower() == age_name.lower():
                colunmId.append(agegroup.id)
                break
        if len(colunmId) <= index:
            listAgeGroupNameRow.append((row[0], row[col]))
            colunmId.append(None)
    df['idAgeGroup'] = colunmId

    return df, listAgeGroupNameRow

async def addFloraRescueZoneIdByName(
        db: AsyncSession,
        df: pd.DataFrame,
        col: str,
) -> tuple[pd.DataFrame, list[tuple[int, str]]]:
    """
    Adds the id of a flora rescue zone to a dataframe

    Parameters
    ----------
    db : AsyncSession
    df : pandas dataframe
    col : str with name of column with flora rescue zone name

    Returns
    -------
    df : pandas dataframe with idFloraRescueZone column
    """
    listFloraRescueZoneNameRow: list[tuple[int, str]] = []
    colunmId: list[int | None] = []

    for _, row in df.iterrows():
        floraRescueZone = await get_flora_rescue_zone(db, row[col])
        if floraRescueZone is None:
            listFloraRescueZoneNameRow.append((row[0], row[col]))
            colunmId.append(None)
        else:
            colunmId.append(floraRescueZone.id)

    df['idFloraRescueZone'] = colunmId

    return df, listFloraRescueZoneNameRow


def addBooleanByGender(
    df: pd.DataFrame,
    col: str,
    genderEqual: tuple[str, str]
) -> tuple[pd.DataFrame, list[tuple[int, str|None]]]:
    """
    Adds the id of with a boolean column to a dataframe
    male = True
    female = False

    Parameters
    ----------
    df: pandas dataframe
    col: str with name of column with gender
    genderEqual:  tuple for a name of  male an female
    """
    listGenderNameRow: list[tuple[int, str|None]] = []
    colunmId: list[bool | None] = []
    male, female = genderEqual


    for _, row in df.iterrows():
        gender:str|None = row[col]
        gender_lower: str|None = gender.lower() if gender is not None else None
        if gender_lower == male.lower():
            colunmId.append(True)
        elif gender_lower == female.lower():
            colunmId.append(False)
        else:
            listGenderNameRow.append((row[0], row[col]))
            colunmId.append(None)

    df['booleanGender'] = colunmId

    return df, listGenderNameRow

async def addTransectIdByNumber(
        db: AsyncSession,
        df: pd.DataFrame,
        col: str,
) -> pd.DataFrame:
    """
    Adds the id of a transect to a dataframe

    Parameters
    ----------
    db : AsyncSession
    df : pandas dataframe
    col : str with name of column with transect number
    """
    listTransectNumberRow: list[tuple[int, str]] = []
    colunmId: list[int | None] = []

    for _, row in df.iterrows():
        #conver row[col] to int
        transect = await get_transect_herpetofauna_by_number(db, row[col])
        if transect is None:
            raise Exception(f"Error converting transect number not exist  in row {row[0]}")
        else:
            colunmId.append(transect.id)

    df['idTransect'] = colunmId

    return df

def addNumRescueHerpeto(
        df: pd.DataFrame,
        col: str,
) -> pd.DataFrame:
    """
    Create a new column with the number of rescue herpetofauna

    Parameters
    ----------
    df : pandas dataframe
    col : str with name of column with rescue herpetofauna number
    """
    # sort col 
    df = df.sort_values(by=[col])

    newCol = []

    rowNumber: int = 0

    while rowNumber < len(df)-1:
        if df[col].iloc[rowNumber] == df[col].iloc[rowNumber+1]:
            j = rowNumber
            listNum = []
            while j < len(df)-1 and df[col].iloc[j] == df[col].iloc[j+1]:
                listNum.append(df[col].iloc[j])
                j += 1
                if j == len(df)-1:
                    listNum.append(df[col].iloc[j])
                    j += 1
            k=1
            if j < len(df)-1:
                listNum.append(df[col].iloc[j])
                j += 1
            for row in listNum:
                newCol.append(row+"R"+str(k))
                k += 1
            rowNumber = j

        else:
            newCol.append(df[col].iloc[rowNumber]+"R1")
            rowNumber += 1
    if rowNumber < len(df):
        newCol.append(df[col].iloc[rowNumber]+"R1")

    df["numRescue"] = newCol
    return df

def addBooleanByCheck(
        df: pd.DataFrame,
        col: str,
) -> pd.DataFrame:
    """
    Add a column with boolean values if the column is empty or not
    the new column is named boolean_{col}
    empty = False
    not empty = True

    Parameters
    ----------
    df: pandas dataframe
    col: str with name of column with check
    """
    df = remplace_nan_with_none(df)
    newCol = []

    for _, row in df.iterrows():
        if row[col] == "None":
            newCol.append(False)
        else:
            newCol.append(True)
    df[f"boolean_{col}"] = newCol
    return df

async def addRescueIdByNumber(
        db: AsyncSession,
        df: pd.DataFrame,
        col: str,
) -> pd.DataFrame:
    """
    Adds the id of a rescue to a dataframe

    Parameters
    ----------
    db : AsyncSession
    df : pandas dataframe
    col : str with name of column with rescue number
    """
    colunmId: list[int | None] = []

    for _, row in df.iterrows():
        #conver row[col] to int
        rescue = await get_rescue_herpetofauna_by_number(db, row[col])
        if rescue is None:
            raise Exception(f"Error get rescue id in row {row[0]}")
        else:
            colunmId.append(rescue.id)

    df['idRescue'] = colunmId

    return df

async def addTransectTranslocationIdByCod(
        db: AsyncSession,
        df: pd.DataFrame,
        col: str,
) -> pd.DataFrame:
    """
    Adds the id of a transect to a dataframe

    Parameters
    ----------
    db : AsyncSession
    df : pandas dataframe
    col : str with name of column with transect translocation cod
    """
    listTransectNumberRow: list[tuple[int, str]] = []
    colunmId: list[int | None] = []

    for _, row in df.iterrows():
        #conver row[col] to int
        transect = await get_transect_herpetofauna_translocation_by_cod(db, row[col])
        if transect is None:
            colunmId.append(None)
        else:
            colunmId.append(transect.id)

    df['idTransect'] = colunmId

    return df




async def addPointTranslocationByCod(
        db: AsyncSession,
        df: pd.DataFrame,
        col: str,
) -> pd.DataFrame:
    """
    Adds the id of a transect to a dataframe

    Parameters
    ----------
    db : AsyncSession
    df : pandas dataframe
    col : str with name of column with point translocation number
    """
    listTransectNumberRow: list[tuple[int, str]] = []
    colunmId: list[int | None] = []

    for _, row in df.iterrows():
        #conver row[col] to int
        point = await get_point_herpetofauna_translocation_by_cod(db, row[col])
        if point is None:
            colunmId.append(None)
        else:
            colunmId.append(point.id)

    df['idPoint'] = colunmId

    return df

async def addRescueFloraIdByNumber(
        db: AsyncSession,
        df: pd.DataFrame,
        col: str,
        )-> pd.DataFrame:
    """
    Adds the id of a rescue to a dataframe

    Parameters
    ----------
    db : AsyncSession
    df : pandas dataframe
    col : str with name of column with rescue number
    """
    listRescueNumberRow: list[tuple[int, str]] = []
    colunmId: list[int | None] = []

    for _, row in df.iterrows():
        rescue = await get_flora_rescue(db, row[col])
        if rescue is None:
            colunmId.append(None)
            listRescueNumberRow.append((row[0], row[col]))
        else:
            colunmId.append(rescue.id)

    df['idRescue'] = colunmId

    return df, listRescueNumberRow

async def addRelocationZoneIdByNumber(
        db: AsyncSession,
        df: pd.DataFrame,
        col: str,
        )-> pd.DataFrame:
    """
    Adds the id of a relozation zone to a dataframe

    Parameters
    ----------
    db : AsyncSession
    df : pandas dataframe
    col : str with name of column with relocation zone number
    """
    listRelocationZoneNumberRow: list[tuple[int, str]] = []
    colunmId: list[int | None] = []

    for _, row in df.iterrows():
        relocationZone = await get_flora_relocation_zone(db, row[col])
        if relocationZone is None:
            colunmId.append(None)
            listRelocationZoneNumberRow.append((row[0], row[col]))
        else:
            colunmId.append(relocationZone.id)

    df['idRelocationZone'] = colunmId

    return df, listRelocationZoneNumberRow

async def addHabitatIdByName(
        db: AsyncSession,
        df: pd.DataFrame,
        col: str,
        )-> pd.DataFrame:
    """
    Adds the id of a habitat to a dataframe

    Parameters
    ----------
    db : AsyncSession
    df : pandas dataframe
    col : str with name of column with habitat name
    """
    listHabitatNameRow: list[tuple[int, str]] = []
    colunmId: list[int | None] = []

    for _, row in df.iterrows():
        habitat = await get_habitat_name(db, row[col])
        if habitat is None:
            colunmId.append(None)
            listHabitatNameRow.append((row[0], row[col]))
        else:
            colunmId.append(habitat.id)

    df['idHabitat'] = colunmId

    return df, listHabitatNameRow

async def addSiteReleaseMammalIdByName(
        db: AsyncSession,
        df: pd.DataFrame,
        col: str,
        )-> pd.DataFrame:
    """
    Adds the id of a site release mammal to a dataframe

    Parameters
    ----------
    db : AsyncSession
    df : pandas dataframe
    col : str with name of column with site release mammal name
    """
    listSiteReleaseMammalNameRow: list[tuple[int, str]] = []
    colunmId: list[int | None] = []

    for _, row in df.iterrows():
        siteReleaseMammal = await get_site_release_mammal_name(db, row[col])
        if siteReleaseMammal is None:
            colunmId.append(None)
            listSiteReleaseMammalNameRow.append((row[0], row[col]))
        else:
            colunmId.append(siteReleaseMammal.id)

    df['idSiteReleaseMammal'] = colunmId

    return df, listSiteReleaseMammalNameRow

async def addRescueMammalIdByCode(
        db: AsyncSession,
        df: pd.DataFrame,
        col: str,
        )-> tuple[pd.DataFrame, list[tuple[int, str]]]:
    """
    Adds the id of a rescue mammal to a dataframe

    Parameters
    ----------
    db : AsyncSession
    df : pandas dataframe
    col : str with name of column with rescue mammal code
    """
    listRescueMammalCodeRow: list[tuple[int, str]] = []
    colunmId: list[int | None] = []

    for _, row in df.iterrows():
        rescueMammal = await get_rescue_mammal_cod(db, row[col])
        if rescueMammal is None:
            colunmId.append(None)
            listRescueMammalCodeRow.append((row[0], row[col]))
        else:
            colunmId.append(rescueMammal.id)

    df['idRescueMammal'] = colunmId

    return df, listRescueMammalCodeRow





