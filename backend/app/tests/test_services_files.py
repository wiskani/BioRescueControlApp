import pandas as pd
import numpy as np
from httpx import Response, AsyncClient
import pytest
from app.schemas.services import UTMData
from app.services.files import (
    convert_to_datetime,
    remplace_nan_with_none,
    none_value,
    generateUTMData,
    insertGEOData,
    addIdSpecieByName,
    addIdGenusByName,
    addIdFamilyByName,
    addMarkIdByNumber,
    addAgeGroupIdByName,
    addBooleanByGender,
    addTransectIdByNumber,
    addNumRescueHerpeto,
    addBooleanByCheck,
    addRescueIdByNumber,
    addTransectTranslocationIdByCod,
    addPointTranslocationByCod
)

from app.tests.conftest import *
from app.tests.utils.users import *
from app.tests.utils.species_example import *
from app.tests.utils.towers_example import *
from app.tests.utils.rescue_herpetofauna import *

# Test convert_to_datetime function
def test_convert_to_datetime():
    # Tests dataset
    data = {
        'A': ['08/08/2023 21:30:00', '08/07/2023 22:30:00', '08/06/2023 23:30:00'],
        'B': ['08/08/2023 21:30:00', '08/07/2023 22:30:00', '08/06/2023 23:30:00'],
        'C': ['date_in', 'date_out', 'date_total']
    }
    df = pd.DataFrame(data)
    # Expected result
    expected = pd.DataFrame({
        'A': pd.to_datetime(['08/08/2023 21:30:00', '08/07/2023 22:30:00', '08/06/2023 23:30:00'], utc=True).tz_convert('America/La_Paz') + pd.Timedelta(hours=4),
        'B': pd.to_datetime(['08/08/2023 21:30:00', '08/07/2023 22:30:00', '08/06/2023 23:30:00'], utc=True).tz_convert('America/La_Paz') + pd.Timedelta(hours=4),
        'C': ['date_in', 'date_out', 'date_total']
    })
    # Test
    result = convert_to_datetime(df, ['A', 'B'])
    assert result.equals(expected)


# Test none_value function
def test_none_value():
    # Test
    result = none_value('None')
    assert result == None

# Test generateUTMData function
def test_generateUTMData():
    # Sample data
    data = {
        'x': [50000, 50000],
        'y': [4649776, 4649776],
        'zona': [20, 20],
        'letra': ['K', 'K'],
    }
    df=pd.DataFrame(data)

    # Colums to Test
    columns = { "easting": "x",  "northing": "y", "zone_number": "zona",  "zone_letter": "letra"}

    # Expected result
    expected = [
        UTMData(
            easting=50000,
            northing=4649776,
            zone_number=20,
            zone_letter='K'
        ),
        UTMData(
            easting=50000,
            northing=4649776,
            zone_number=20,
            zone_letter='K'
        )
    ]

    # Test
    result = generateUTMData(df, columns)
    assert result == expected

# Test insertGEOData
def test_insertGEOData():
    # Sample data
    data = {
        'x': [258182, 258175],
        'y': [8062818, 8062839],
        'zona': [20, 20],
        'letra': ['S', 'S'],
        'numer': [1, 2]
    }
    df=pd.DataFrame(data)

    # Colums to Test
    columns = { "easting": "x",  "northing": "y", "zone_number": "zona",  "zone_letter": "letra"}


    # Name columns
    nameLatitude = "latitude1"
    nameLongitude = "longitude1"

    # Expected result
    expected = pd.DataFrame({
        'x': [258182, 258175],
        'y': [8062818, 8062839],
        'zona': [20, 20],
        'letra': ['S', 'S'],
        'numer': [1, 2],
        'latitude1': [-17.50783403355633, -17.50764360693236],
        'longitude1': [-65.27753191052074, -65.27759543591202]
    })

    # Test
    result = insertGEOData(df, columns , nameLatitude, nameLongitude)
    assert result.equals(expected)

# Test for addIdSpecieByName function
@pytest.mark.asyncio
async def test_addIdSpecieByName(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    specie_id, specie_name = await create_specieWithName(async_client)
    col: str = "especie"
    colId: str = "idSpecie"

    #Create DF for Test
    data = {
        'number' : [1, 2],
        'especie': [specie_name, "unknown"],
    }

    df = pd.DataFrame(data)

    # Expected result
    expected = pd.DataFrame({
        'number' : [1, 2],
        'especie': [specie_name, "unknown"],
        'idSpecie': [specie_id, None],
    })

    listExpect: list[tuple[int, str]] =  [(2, "unknown")]

    # Result
    resultDF, resulLIST = await addIdSpecieByName(async_session, df, col, colId)


    # Test
    assert resultDF.equals(expected)
    assert resulLIST == listExpect

# Test for addIdGenusByName function
@pytest.mark.asyncio
async def test_addIdGenusByName(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    genus_id, genus_name = await create_genusWithName(async_client)
    col: str = "genero"
    colId: str = "idGenus"

    #Create DF for Test
    data = {
        'number' : [1, 2],
        'genero': [genus_name, "unknown"],
    }

    df = pd.DataFrame(data)

    # Expected result
    expected = pd.DataFrame({
        'number' : [1, 2],
        'genero': [genus_name, "unknown"],
        'idGenus': [genus_id, None],
    })

    listExpect: list[tuple[int, str]] =  [(2, "unknown")]

    # Result
    resultDF, resulLIST = await addIdGenusByName(async_session, df, col, colId)


    # Test
    assert resultDF.equals(expected)
    assert resulLIST == listExpect

# Test for addIdFamilyByName function
@pytest.mark.asyncio
async def test_addIdFamilyByName(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    family_id, family_name = await create_familyWithName(async_client)
    col: str = "familia"
    colId: str = "idFamily"

    #Create DF for Test
    data = {
        'number' : [1, 2],
        'familia': [family_name, "unknown"],
    }

    df = pd.DataFrame(data)

    # Expected result
    expected = pd.DataFrame({
        'number' : [1, 2],
        'familia': [family_name, "unknown"],
        'idFamily': [family_id, None],
    })

    listExpect: list[tuple[int, str]] =  [(2, "unknown")]

    # Result
    resultDF, resulLIST = await addIdFamilyByName(async_session, df, col, colId)


    # Test
    assert resultDF.equals(expected)
    assert resulLIST == listExpect



#Test for addMarkIdByNumber function
@pytest.mark.asyncio
async def test_addMarkIdByNumber(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    mark_id, mark_number = await create_mark_herpetofaunaWithNumber(async_client)
    col: str = "marck"
    number_mark: int = random.randint(1, 1000)

    #Create DF for Test
    data = {
        'number' : [1, 2],
        'marck': [mark_number, 12 ],
    }

    df = pd.DataFrame(data)

    # Expected result
    expected = pd.DataFrame({
        'number' : [1, 2],
        'marck': [mark_number, 12 ],
        'idMark': [mark_id, None],
    })

    listExpect: list[tuple[int, int]] =  [(2, 12)]

    # Result
    resultDF, resulLIST = await addMarkIdByNumber(async_session, df, col)

    print(resultDF)
    print(expected)

    # Test
    assert resultDF.equals(expected)
    assert resulLIST == listExpect

# Tes for addAgeGroupIdByName function
@pytest.mark.asyncio
async def test_addAgeGroupIdByName(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    age_group_id, age_group_name = await create_age_groupWithName(async_client)
    col: str = "age_group"

    #Create DF for Test
    data = {
        'number' : [1, 2],
        'age_group': [age_group_name, "unknown"],
    }

    df = pd.DataFrame(data)

    # Expected result
    expected = pd.DataFrame({
        'number' : [1, 2],
        'age_group': [age_group_name, "unknown"],
        'idAgeGroup': [age_group_id, None],
    })

    listExpect: list[tuple[int, str]] =  [(2, "unknown")]

    # Result
    resultDF, resulLIST = await addAgeGroupIdByName(async_session, df, col)

    # Test
    assert resultDF.equals(expected)
    assert resulLIST == listExpect

# Test for addBooleanByGender function
def test_addBooleanByGender() -> None:

    col= "sexo"
    genderEqual: tuple[str, str] = ("Macho", "Hembra")

    #Create DF for Test
    data = {
        'number' : [1, 2, 3],
        'sexo': ["Macho", "Hembra", None],
    }

    df = pd.DataFrame(data)

    # Expected result
    expected = pd.DataFrame({
        'number' : [1, 2, 3],
        'sexo': ["Macho", "Hembra", None],
        'booleanGender': [True, False, None],
    })

    listExpect: list[tuple[int, None ]] =  [(3, None)]

    # Result
    resultDF, resulLIST = addBooleanByGender(df, col, genderEqual)


    # Test
    assert resultDF.equals(expected)
    assert resulLIST == listExpect

# Test for addTransectIdByNumber function
@pytest.mark.asyncio
async def test_addTransectIdByNumber(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    transect_id, transect_number = await create_transect_herpetofaunaWithNumber(async_client)
    col: str = "transect"

    #Create DF for Test
    data = {
        'number' : [1 ],
        'transect': [transect_number ],
    }

    df = pd.DataFrame(data)

    # Expected result
    expected = pd.DataFrame({
        'number' : [1],
        'transect': [transect_number],
        'idTransect': [transect_id],
    })


    # Result
    resultDF = await addTransectIdByNumber(async_session, df, col)


    # Test
    assert resultDF.equals(expected)

# Test for addNumRescueHerpeto
def test_addNumRescueHerpeto() -> None:

    #Create DF for Test
    data = {
        'number' : ["101T09","101T13", "101T12","101T13","101T13","101T13", "101T15"],
        'rescue': [1, 2, 3, 4, 5, 6, 7],
    }

    df = pd.DataFrame(data)

    # Expected result
    expected = pd.DataFrame({
        'number' : ["101T09","101T12", "101T13","101T13","101T13","101T13", "101T15"],
        'rescue': [1, 3, 2, 4, 5, 6, 7],
        'numRescue' : ["101T09R1","101T12R1", "101T13R1","101T13R2","101T13R3","101T13R4", "101T15R1"],
    })

    # Result
    resultDF = addNumRescueHerpeto(df, "number")
    resultDF = resultDF.reset_index(drop=True)

    # Test
    assert resultDF.equals(expected)

# Test for addBooleanByCheck function
def test_addBooleanByCheck() -> None:


    #Create DF with NaN values for Test
    data = {
        'number' : [1, 2, 3, 4, 5, 6, 7],
        'check': ["prueba", "bueno", None, np.nan, "bueno", "prueba", None],
    }

    df = pd.DataFrame(data)

    # Expected result
    expected = pd.DataFrame({
        'number' : [1, 2, 3, 4, 5, 6, 7],
        'check': ["prueba", "bueno", "None", "None" , "bueno", "prueba", "None"],
        'boolean_check': [True, True, False, False, True, True, False],
    })

    # Result
    resultDF = addBooleanByCheck(df, "check")

    # Test
    assert resultDF.equals(expected)

# Test for addRescueIdByNumber function
@pytest.mark.asyncio
async def test_addRescueIdByNumber(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    id, number = await create_rescue_herpetofaunaWithNumber(async_client)
    id2, number2 = await create_rescue_herpetofaunaWithNumber(async_client)
    id3, number3 = await create_rescue_herpetofaunaWithNumber(async_client)
    col: str = "rescue"

    #Create DF for Test
    data = {
        'number' : [1, 2, 3],
        'rescue': [number, number2, number3],
    }

    df = pd.DataFrame(data)

    # Expected result
    expected = pd.DataFrame({
        'number' : [1, 2, 3],
        'rescue': [number, number2, number3],
        'idRescue': [id, id2, id3],
    })

    # Result
    resultDF = await addRescueIdByNumber(async_session, df, col)

    # Test
    assert resultDF.equals(expected)

# Test for addTransectTranslocationIdByCode function
@pytest.mark.asyncio
async def test_addTransectTranslocationIdByNumber(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    transect_id, transect_number = await  create_transect_herpetofauna_translocationWithCode(async_client)
    col: str = "transect"

    #Create DF for Test
    data = {
        'number' : [1 ],
        'transect': [transect_number ],
    }

    df = pd.DataFrame(data)

    # Expected result
    expected = pd.DataFrame({
        'number' : [1],
        'transect': [transect_number],
        'idTransectTranslocation': [transect_id],
    })


    # Result
    resultDF = await addTransectTranslocationIdByCod(async_session, df, col)


    # Test
    assert resultDF.equals(expected)

# Test for addPointTranslocationByCod function
@pytest.mark.asyncio
async def test_addPointTranslocationIdByCod(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    point_id, point_cod = await  create_point_herpetofauna_translocation_with_code(async_client)
    col: str = "point"

    #Create DF for Test
    data = {
        'number' : [1 ],
        'point': [point_cod],
    }

    df = pd.DataFrame(data)

    # Expected result
    expected = pd.DataFrame({
        'number' : [1],
        'point': [point_cod],
        'idPointTranslocation': [point_id],
    })


    # Result
    resultDF = await addPointTranslocationByCod(async_session, df, col)


    # Test
    assert resultDF.equals(expected)


