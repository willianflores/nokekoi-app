from updateNokekoiAppDataFunctions import *

## Download and process fire da data
NTR_TOKEN = loadTokenFromFile()
loadFirmsData(NTR_TOKEN)

## Load TI and TI Buffer boundaries
ti = import_shp("/home/srvadmin/nokekoiApp/datasets/shp/TI_Campinas_Katukina.shp")
ti_buffer = import_shp("/home/srvadmin/nokekoiApp/datasets/shp/TI_Campinas_Katukina_Buffer10km.shp")

# Process FIRMS txt file
directory_path = "/home/srvadmin/nokekoiApp/datasets/suomi-npp-viirs-c2/South_America/"
parquet_file_path = "/home/srvadmin/nokekoiApp/datasets/suomi-npp-viirs-c2/parquet/fire_data.parquet"

txtToParquet(directory_path, parquet_file_path)

## get fire data
start_date = setStartDate(15)
start_date_30 = setStartDate(30)
start_date_60 = setStartDate(60)
start_date_90 = setStartDate(90)
start_date_180 = setStartDate(180)
start_date_365 = setStartDate(365)

bounds = [(ti, "ti_fire"), (ti_buffer, "ti_buffer_fire")]
start_dates = [
    (start_date, "15d"),
    (start_date_30, "30d"),
    (start_date_60, "60d"),
    (start_date_90, "90d"),
    (start_date_180, "180d"),
    (start_date_365, "365d")
]

# Loop for dynamic calls
for bound_name, file_prefix in bounds:
    for start, days_suffix in start_dates:
        output_filename = f"{file_prefix}_{days_suffix}"
        getFireData(bound_name, start, output_filename)

## Download and process RADD data
loadRaddRasterData()

# Clip radd image
inshp = '/home/srvadmin/nokekoiApp/datasets/shp/TI_Campinas_Katukina_Buffer10km_All.shp'
inRas = '/home/srvadmin/nokekoiApp/datasets/radd/00N_080W.tif'
outRas = '/home/srvadmin/nokekoiApp/datasets/radd/00N_080W_clip.tif'

imgClip(inshp,inRas,outRas)

# Process radd image to geoparquet
radd_path = "/home/srvadmin/nokekoiApp/datasets/radd/00N_080W_clip.tif"

start_date = setStartDate(15)
start_date_30 = setStartDate(30)
start_date_60 = setStartDate(60)
start_date_90 = setStartDate(90)
start_date_180 = setStartDate(180)
start_date_365 = setStartDate(365)

bounds_radd = [(ti, "ti_radd"), (ti_buffer, "ti_buffer_radd")]
start_dates_radd = [
    (start_date, "15d"),
    (start_date_30, "30d"),
    (start_date_60, "60d"),
    (start_date_90, "90d"),
    (start_date_180, "180d"),
    (start_date_365, "365d")
]

# Loop for dynamic calls
for bound_name, file_prefix in bounds_radd:
    for start, days_suffix in start_dates_radd:
        output_filename = f"{file_prefix}_{days_suffix}"
        processRaddData(radd_path, bound_name, start, output_filename)
