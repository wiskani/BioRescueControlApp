import pyproj

from app.schemas.services import UTMData

def utm_to_latlong (utmData:UTMData):
    utm_proj = pyproj.Proj(proj='utm', zone=utmData.zone_number, ellps='WGS84', south = True)
    wgs_proj = pyproj.Proj(proj='latlong', datum='WGS84')

    wgsData = pyproj.transform(utm_proj, wgs_proj, utmData.easting, utmData.northing)

    return wgsData
