import pyproj

from app.schemas.services import UTMData

# This function is for convert a coordinate from UTM to WGS84
def utm_to_latlong (utmData:UTMData):
    utm_proj = pyproj.Proj(proj='utm', zone=utmData.zone_number, ellps='WGS84', south = (utmData.zone_letter < 'N'))
    wgs_proj = pyproj.Proj(proj='latlong', datum='WGS84')

    lon, lat = pyproj.transform(utm_proj, wgs_proj, utmData.easting, utmData.northing)

    return {
        "lat": lat,
        "long": lon
    }
