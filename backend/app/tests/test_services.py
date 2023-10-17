import pandas as pd
import pytest
from app.services.files import  convert_to_datetime

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


