import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.request import urlopen
from datetime import datetime, timedelta, date
import requests
import pytz
import pandas as pd
import geopandas as gpd
import os
import glob
from urllib.request import urlopen
import rasterio
from rasterio.features import shapes
from rasterio.mask import mask
import pyarrow

## Load TI and TI Buffer boundaries
def import_shp(shp_path):
    
    gdf = gpd.read_file(shp_path)
    
    return gdf

## Download and process fire da data

def send_email_notification(subject, body):
    sender_email = "willian.flores@ufac.br"  # Substitua com seu e-mail
    receiver_email = "willianflores@gmail.com"
    password = "U$4ep6My"  # Substitua com sua senha
    smtp_server = "smtp.gmail.com"  # Substitua com o servidor SMTP correto
    port = 587  # Ou o número da porta SMTP correta

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("E-mail de notificação enviado com sucesso.")
    except Exception as e:
        print(f"Falha ao enviar e-mail: {e}")

def loadTokenFromFile():
    """Carrega o token salvo do arquivo."""
    try:
        with open("/home/srvadmin/nokekoiApp/datasets/suomi-npp-viirs-c2/token/token.txt", "r") as file:
            token = file.read().strip()
            print("Token carregado do arquivo:", token)
            return {"access_token": token}
    except FileNotFoundError:
        print("Arquivo de token não encontrado. Crie um novo token.")
        return None

def loadFirmsData(NTR_TOKEN):
    """Carrega dados da API FIRMS usando o token fornecido."""
    if not NTR_TOKEN or "access_token" not in NTR_TOKEN:
        print("Token inválido. Não foi possível carregar os dados.")
        return

    NTR_TOKEN = NTR_TOKEN["access_token"]
    
    ## Variáveis
    URL_NOAA_20_VIIRS_C2 = "https://nrt4.modaps.eosdis.nasa.gov/archive/FIRMS/noaa-20-viirs-c2/South_America/"
    BASE_NOAA_FILE_NAME = "J1_VIIRS_C2_South_America_VJ114IMGTDL_NRT_"
    FILE_TYPE = ".txt"

    TODAY_YDAY = F"{(datetime.now() - timedelta(days=1)).timetuple().tm_yday:03}".__str__()
    TODAY_YEAR = (datetime.now() - timedelta(days=1)).year.__str__()

    NOAA_FILE_NAME = BASE_NOAA_FILE_NAME + TODAY_YEAR + TODAY_YDAY + FILE_TYPE
    NOAA_URL = URL_NOAA_20_VIIRS_C2 + NOAA_FILE_NAME
    NOAA_FOLDER = "/home/srvadmin/nokekoiApp/datasets/suomi-npp-viirs-c2/South_America/" + NOAA_FILE_NAME

    ## Carregar dados da API
    payload_noaa = {}
    headers = {
        "Authorization": "Bearer " + NTR_TOKEN
    }

    response_noaa = requests.request(
        "GET",
        NOAA_URL,
        headers=headers,
        data=payload_noaa
    )

    if response_noaa.status_code == 200:
        # Salvar o conteúdo da resposta em um arquivo local TXT
        with open(NOAA_FOLDER, "wb") as f:
            f.write(response_noaa.content)
        print("TXT file downloaded successfully")
    else:
        print("Failed to download TXT file. Status code:", response_noaa.status_code)
        # Enviar e-mail em caso de falha
        subject = "Falha no download do arquivo NOAA VIIRS..."
        body = f"Não foi possível baixar o arquivo NOAA VIIRS. Status code: {response_noaa.status_code}."
        send_email_notification(subject, body)

        
# Process FIRMS txt file
def txtToParquet(directory_path, parquet_file_path):
    # Lista todos os arquivos .txt no diretório
    txt_files = glob.glob(os.path.join(directory_path, '*.txt'))

    # Initialize an empty DataFrame to store all data
    df_total = pd.DataFrame()

    # Loads each .txt file and concatenates to the total DataFrame
    for file in txt_files:
        df = pd.read_csv(file, sep=',', encoding='utf-8', on_bad_lines='skip')  # Ajuste o separador se necessário
        df_total = pd.concat([df_total, df], ignore_index=True)
    
    #df_total.info()
    #df_total.memory_usage(deep=True)
    # df_total["acq_date_time"] = df_total['acq_date'].astype(str) + " " + df['acq_time'].astype(str)
    df_total["acq_date"] = pd.to_datetime(df_total["acq_date"]) 
    # local_timezone = pytz.timezone('Brazil/Acre')
    # df_total["acq_date_time"] = df_total["acq_date_time"].dt.tz_localize('UTC').dt.tz_convert(local_timezone)
    df_total = df_total.filter(["latitude", "longitude", "brightness", "acq_date"])
    df_total = df_total.loc[df_total["acq_date"]>= pd.to_datetime(date.today() - timedelta(days=365))]
    
    # Clip to TI and TI Buffer
    ## Fazer o clip...
    
    # Export to .parquet
    df_total.to_parquet(parquet_file_path, index=False)


## Set fire data to App

# Function to set start date
def setStartDate(time_filter):
    start_date = date.today() - timedelta(days = time_filter)
    start_date.strftime('%m/%d/%Y')
    
    return start_date

# Function to get fire data
def getFireData(bound, start_date, output_filename):
    
    """
        Loads hotspot data and exports it to a GeoParquet file based on a bounding polygon and a start date.

        Parameters:
        bound (shapely.geometry.Polygon): The bounding polygon used to clip the data.
        start_date (datetime.date or str): The start date for filtering the data.
        output_filename (str): The name of the GeoParquet file to be generated.
        
        Returns:
        None
    """

    path ="/home/srvadmin/nokekoiApp/datasets/suomi-npp-viirs-c2/parquet/fire_data.parquet"
    output_path = f"/home/srvadmin/nokekoiApp/datasets/suomi-npp-viirs-c2/parquet/{output_filename}.geoparquet"

    try:
        # Read data as GeoDataFrame
        df_fire = pd.read_parquet(path)
    
        gdf_fire = gpd.GeoDataFrame(
            df_fire, 
            geometry = gpd.points_from_xy(
            df_fire.longitude, 
            df_fire.latitude
            ), 
            crs="EPSG:4326"
        )

        # Clip data using bound
        gdf_fire = gdf_fire.clip(bound)

        # Filter data based on start_date
        gdf_fire = gdf_fire.loc[gdf_fire["acq_date"]>= pd.to_datetime(start_date)]

        # Format acquisition date
        gdf_fire["acq_date"] = gdf_fire["acq_date"].dt.strftime('%d/%m/%Y')

        # Export to GeoParquet using to_parquet method (recommended)
        gdf_fire.to_parquet(output_path)
        
        print(f"GeoDataFrame exportado com sucesso para {output_path}")

    except Exception as e:
        print(f"Erro ao exportar para GeoParquet: {e}")

## Download and process RADD data
def loadRaddRasterData():
    try:
        # Define url parameters
        url = "https://data-api.globalforestwatch.org/dataset/gfw_integrated_alerts/latest/download/geotiff?grid=10/100000&tile_id=00N_080W&pixel_meaning=date_conf&x-api-key=2d60cd88-8348-4c0f-a6d5-bd9adb585a8c"

        # Get request
        response = urlopen(url).read()
      
        # Delete existing file
        delete_file = "/home/srvadmin/nokekoiApp/datasets/radd/00N_080W.tif"
      
        # If file exists, delete it.
        if os.path.isfile(delete_file) and os.access(delete_file, os.R_OK):
            os.remove(delete_file)

        # Set output file name 
        output_file = "/home/srvadmin/nokekoiApp/datasets/radd/00N_080W.tif"

        # Open a file in binary write mode
        with open(output_file, "wb") as f:
            # Write response content to file
            f.write(response)
        print("Arquivo TIFF baixado e salvo com sucesso.")
    
    except Exception as e:
        print(f"Erro ao carregar os dados RADD: {e}")
        # Enviar e-mail em caso de erro
        subject = "Falha no download do arquivo RADD Raster..."
        body = f"Não foi possível baixar o arquivo RADD Raster. Erro: {e}."
        send_email_notification(subject, body)
        
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
      
## Fuction to process radd clip image
def processRaddData(raster_path, bound, start_date, output_filename):
    """
    Processes raster data and exports it to a GeoParquet file based on a bounding polygon and a start date.

    Parameters:
    raster_path (str): Path to the raster file.
    bound (shapely.geometry.Polygon): The bounding polygon used to clip the data.
    start_date (datetime.date or str): The start date for filtering the data.
    output_filename (str): The name of the GeoParquet file to be generated.

    Returns:
    None
    """

    try:
        # Read bounding polygon as GeoDataFrame
        bound_gdf = bound

        # Load raster and extract shapes
        mask = None              
        with rasterio.Env():
            with rasterio.open(raster_path) as src:
                image = src.read(1)  # First band
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

        # Convert to GeoDataFrame
        gdf = gpd.GeoDataFrame.from_features(geoms, crs="EPSG:4326")

        # Process raster attributes
        gdf["raster_val"] = gdf["raster_val"].astype(str)
        gdf["v_id"] = gdf["raster_val"].str[:1]
        gdf["date"] = gdf["raster_val"].str[1:5]

        gdf["raster_val"] = gdf["raster_val"].astype(float)
        gdf["raster_val"] = gdf["raster_val"].astype(int)
        gdf["v_id"] = gdf["v_id"].astype(int)
        gdf["date"] = gdf["date"].astype(float)
        gdf["date"] = gdf["date"].astype(int)

        gdf["date"] = pd.to_datetime(
            gdf["date"],
            unit="D",
            origin="2014-12-31"  
        )

        # Filter based on date and value
        gdf = gdf[
            (gdf["date"] >= pd.to_datetime(start_date))
            & (gdf["v_id"] >= 3)
        ]

        # Drop unnecessary columns
        gdf = gdf.drop(columns=["raster_val", "v_id"])

        # Clip data with bounding polygon
        gdf_clipped = gdf.clip(bound_gdf)

        # Ensure CRS is projected for area calculation
        projected_crs = "+proj=aea +lat_1=10 +lat_2=-40 +lat_0=-25 +lon_0=-50 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs "
        gdf_clipped = gdf_clipped.to_crs(projected_crs)

        # Calculate area and filter polygons >= 0.05 hectares
        gdf_clipped['area_ha'] = gdf_clipped['geometry'].area / 10_000  # Convert m² to hectares
        gdf_clipped = gdf_clipped[gdf_clipped['area_ha'] >= 0.15]

        # Drop the area column (optional)
        gdf_clipped = gdf_clipped.drop(columns=["area_ha"])

        # Return to geographic CRS (EPSG:4326)
        gdf_clipped = gdf_clipped.to_crs("EPSG:4326")

        # Export to GeoParquet
        output_path = f"/home/srvadmin/nokekoiApp/datasets/radd/geoparquet/{output_filename}.geoparquet"
        gdf_clipped.to_parquet(output_path)

        print(f"GeoDataFrame successfully exported to {output_path}")

    except Exception as e:
        print(f"Error processing raster data: {e}")



