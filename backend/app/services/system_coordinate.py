import pyproj
from typing import Tuple

from app.schemas.services import UTMData

def utm_to_latlong (utmData:UTMData) -> Tuple [float, float]:
    try:
        utm_proj = pyproj.Proj(proj='utm', zone=utmData.zone_number, ellps='WGS84', south = True)
        wgs_proj = pyproj.Proj(proj='latlong', datum='WGS84')

        wgsData = pyproj.transform(utm_proj, wgs_proj, utmData.easting, utmData.northing)

        lat, lon  = float(wgsData[1]), float(wgsData[0])
        return lat, lon

    except Exception as e:
        raise Exception(f"Error converting UTM to LatLong: {e}")
