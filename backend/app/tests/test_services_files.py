import pandas as pd
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
    addMarkIdByNumber
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
    resultDF, resulLIST = await addIdSpecieByName(async_session, df, col)


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

    # Test
    assert resultDF.equals(expected)
    assert resulLIST == listExpect




