import pandas as pd
import pytest
from app.schemas.services import UTMData
from app.services.files import  convert_to_datetime, remplace_nan_with_none, none_value, generateUTMData, insertGEOData

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







