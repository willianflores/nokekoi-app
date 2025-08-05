import os
from urllib.request import urlopen
import pandas as pd
import geopandas as gpd
#import geoparquet as gpq
import os
import glob
from datetime import date, timedelta
import rasterio
from rasterio.features import shapes
from rasterio.mask import mask

## 
def loadRaddRasterData():
   
  # Define url parameters
  url = "https://data-api.globalforestwatch.org/dataset/gfw_integrated_alerts/latest/download/geotiff?grid=10/100000&tile_id=00N_080W&pixel_meaning=date_conf&x-api-key=2d60cd88-8348-4c0f-a6d5-bd9adb585a8c"

  # Get request
  response = urlopen(url).read()
  
  # Delete existing file
  delete_file = "/home/willianflores/localhost/nokekoiApp/datasets/radd/00N_080W.tif"
  
  # If file exists, delete it.
  if os.path.isfile(delete_file) and os.access(delete_file, os.R_OK):
      os.remove(delete_file)

  # Set output file name 
  output_file = "/home/willianflores/localhost/nokekoiApp/datasets/radd/00N_080W.tif"

  # Open a file in binary write mode
  with open(output_file, "wb") as f:
    # Write response content to file
    f.write(response)
  f.close()

loadRaddRasterData()

## Fuction to clip radd image
def imgClip(inShp, inRas, outRas):
  vector = gpd.read_file(inShp)

  with rasterio.open(inRas) as src:
      vector = vector.to_crs(src.crs)
      # print(Vector.crs)
      out_image, out_transform = mask(src,vector.geometry,crop=True)
      out_meta=src.meta.copy() # copy the metadata of the source DEM
      
  out_meta.update({
      "driver":"Gtiff",
      "height":out_image.shape[1], # height starts with shape[1]
      "width":out_image.shape[2], # width starts with shape[2]
      "transform":out_transform
  })
          
  with rasterio.open(outRas,'w',**out_meta) as dst:
      dst.write(out_image)
      
## Run imgClip function  
inshp = '/home/willianflores/localhost/nokekoiApp/datasets/shp/TI_Campinas_Katukina_Buffer10km_All.shp'
inRas = '/home/willianflores/localhost/nokekoiApp/datasets/radd/00N_080W.tif'
outRas = '/home/willianflores/localhost/nokekoiApp/datasets/radd/00N_080W_clip.tif'

imgClip(inshp,inRas,outRas)

## Fuction to process radd clip image
def imgToGeoparquet(radd_path, parquet_path, shp_ti, shp_buffer):
  mask = None
  shp_ti_clip = gpd.read_file(shp_ti)
  shp_buffer_clip = gpd.read_file(shp_buffer)
  with rasterio.Env():
      with rasterio.open(radd_path) as src:
          image = src.read(1) # first band
          results = (
            {'properties': {'raster_val': v}, 'geometry': s}
            for i, (s, v) in enumerate(
              shapes(
                image, 
                mask=mask, 
                transform=src.transform
              )
            )
          )

  geoms = list(results)
  gpd_poly_raster  = gpd.GeoDataFrame.from_features(geoms, crs="EPSG:4326")
  gpd_poly_raster["raster_val"] = gpd_poly_raster["raster_val"].astype(str)
  gpd_poly_raster["v_id"] = gpd_poly_raster["raster_val"].str[:1]
  gpd_poly_raster["date"] = gpd_poly_raster["raster_val"].str[1:5]

  gpd_poly_raster["raster_val"] = gpd_poly_raster["raster_val"].astype(float)
  gpd_poly_raster["raster_val"] = gpd_poly_raster["raster_val"].astype(int)
  gpd_poly_raster["v_id"] = gpd_poly_raster["v_id"].astype(int)
  gpd_poly_raster["date"] = gpd_poly_raster["date"].astype(float)
  gpd_poly_raster["date"] = gpd_poly_raster["date"].astype(int)

  gpd_poly_raster["date"] = pd.to_datetime(
    gpd_poly_raster["date"],
    unit = "D",
    origin = "2014-12-31"  
  )

  gpd_poly_raster = gpd_poly_raster.loc[gpd_poly_raster["date"]>= pd.to_datetime(date.today() - timedelta(days = 366))]
  gpd_poly_raster = gpd_poly_raster.loc[gpd_poly_raster["v_id"]>= 3]
  
  radd_data = gpd_poly_raster.drop(gpd_poly_raster[["raster_val", "v_id"]], axis=1)
  
  radd_ti_data = radd_data.clip(shp_ti_clip.to_crs("EPSG:4326"))
  radd_ti_data.to_parquet(os.path.join(parquet_path, "radd_ti_data.geoparquet"))
  
  radd_buffer_data = radd_data.clip(shp_buffer_clip.to_crs("EPSG:4326"))
  radd_buffer_data.to_parquet(os.path.join(parquet_path, "radd_buffer_data.geoparquet"))
  
  
# Run imgToGeoparquet function
radd_path = "/home/willianflores/localhost/nokekoiApp/datasets/radd/00N_080W_clip.tif"
parquet_path = "/home/willianflores/localhost/nokekoiApp/datasets/radd/geoparquet/"
shp_ti = "/home/willianflores/localhost/nokekoiApp/datasets/shp/TI_Campinas_Katukina.shp"
shp_buffer = "/home/willianflores/localhost/nokekoiApp/datasets/shp/TI_Campinas_Katukina_Buffer10km.shp"

imgToGeoparquet(radd_path, parquet_path, shp_ti, shp_buffer)