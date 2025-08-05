import requests
import json
import pandas as pd
import geopandas as gpd
from shapely.geometry import box
import shapely.geometry
import io

## Load datasets
gdf_val_buffer = gpd.read_file('../data/shp/valparaiso_buffer.shp')
gdf_val_buffer_box = gdf_val_buffer.bounds
gdf_val_buffer_box.to_json(orient = 'columns')

geom = box(*gdf_val_buffer.total_bounds)
json = shapely.geometry.mapping(geom)
coord = str(json['coordinates']).replace('(','[').replace(')',']')
print(json.dumps(coord))

def loadRaddDataApi(bounding_box, startdate, enddate):
  url = "https://data-api.globalforestwatch.org/dataset/wur_radd_alerts/latest/query/csv"

  payload = json.dumps({
    "geometry": {    
      "type": "Polygon",
      "coordinates": bounding_box
    },
    "sql": "SELECT longitude, latitude, wur_radd_alerts__date, wur_radd_alerts__confidence FROM results WHERE wur_radd_alerts__date >= '2023-01-01' AND wur_radd_alerts__date <= '2023-12-31'"
  })

  headers = {
    'Connection':'close',
    'accept': 'application/json',
    'x-api-key': 'ea7f3949-a15a-4c1b-90cb-e9ada0b25f0b'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  df = pd.read_csv(io.StringIO(response.text))
  
  return df

gdf = gpd.GeoDataFrame(
    df, 
    geometry = gpd.points_from_xy(
      df.longitude, 
      df.latitude
    ),
    crs="EPSG:4326"
)

gdf.plot(color='red')
