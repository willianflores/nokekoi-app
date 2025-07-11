## Import libraries
import requests

#import json
from datetime import datetime, timedelta, date
import pytz
import pandas as pd
import os
import glob

## Load FIRMS data function
def loadFirmsData():
    ## Variables
    NTR_TOKEN = "eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6IndpbGxpYW5mbG9yZXNhYyIsImV4cCI6MTcyMzg0NTcwMSwiaWF0IjoxNzE4NjYxNzAxLCJpc3MiOiJFYXJ0aGRhdGEgTG9naW4ifQ.2Uikk3W-0E07Oxj9X71Hfa3eJvVzYpCB0wU-Cwuj8CUOs9SBITOxyNPb5wabuw41aVcynfT-UtYmiUqzqL3K3mZAuEkxIGD5-tCjdFEWTt0QrEegdF7Xm-z2dz5oT3IV4zOhaJAjMoC3IMUj5ODG-CRhttf7a45RCXM8iC3GxBmr0MxgKvfAyFwO1rPJK0_0B8tPTWartVBzeOeXrUkgun3w3gS4qllRth5LWdn0W3T0SKxmKxvCu3a_S9jsndIGSXwYqQRqWE2e-RErhGJVCgcoUfydzmlr3g6-Zi4Oo3p3vHTVC2Bj2xPKczea56N0JwI7DOFJIeGbb_VyBfJUog"
    # URL_NOAA_20_VIIRS_C2 = "https://nrt4.modaps.eosdis.nasa.gov/api/v2/content/archives/FIRMS/noaa-20-viirs-c2/South_America/"
    URL_SUOMI_VIIRS_C2 = "https://nrt4.modaps.eosdis.nasa.gov/api/v2/content/archives/FIRMS/suomi-npp-viirs-c2/South_America/"
    # BASE_NOAA_FILE_NAME = "J1_VIIRS_C2_South_America_VJ114IMGTDL_NRT_"
    BASE_SUOMI_FILE_NAME = "SUOMI_VIIRS_C2_South_America_VNP14IMGTDL_NRT_"
    FILE_TYPE = ".txt"

    TODAY_YDAY = F"{(datetime.now() - timedelta(days=1)).timetuple().tm_yday:03}".__str__()
    TODAY_YEAR = (datetime.now() - timedelta(days=1)).year.__str__()

    # NOAA_FILE_NAME = BASE_NOAA_FILE_NAME + TODAY_YEAR + TODAY_YDAY + FILE_TYPE
    SUOMI_FILE_NAME = BASE_SUOMI_FILE_NAME + TODAY_YEAR + TODAY_YDAY + FILE_TYPE

    # NOAA_URL = URL_NOAA_20_VIIRS_C2 + NOAA_FILE_NAME
    SUOMI_URL = URL_SUOMI_VIIRS_C2 + SUOMI_FILE_NAME

    # NOAA_FOLDER = "/home/willianflores/localhost/nokekoi_app/datasets/noaa-20-viirs-c2/" + NOAA_FILE_NAME
    SUOMI_FOLDER = "/home/willianflores/localhost/nokekoi_app/datasets/suomi-npp-viirs-c2/South_America/" + SUOMI_FILE_NAME

    ## Load API fire data
    # Load NOAA VIIRS data
    # payload_noaa = {}
    headers = {
        "Authorization": "Bearer" + " " + NTR_TOKEN
    }

    # response_noaa = requests.request(
    #     "GET", 
    #     NOAA_URL,
    #     headers = headers,
    #     data = payload_noaa
    # )

    # type(response_noaa.content)

    # print(response_noaa.text)

    # Load SUOMI VIIRS data
    payload_suomi = {}

    response_suomi = requests.request(
        "GET", 
        SUOMI_URL,
        headers = headers,
        data = payload_suomi
    )

    print(response_suomi.text)

    ## Write API fire data to txt file
    # White NOAA file
    # if response_noaa.status_code == 200:
    #     # Save the content of the response to a local CSV file
    #     with open(NOAA_FOLDER, "wb") as f:
    #         f.write(response_noaa.content)
    #     print("TXT file downloaded successfully")
    # else:
    #     print("Failed to download TXT file. Status code:", response_noaa.status_code)

    # White SUOMI file
    if response_suomi.status_code == 200:
        # Save the content of the response to a local CSV file
        with open(SUOMI_FOLDER, "wb") as f:
            f.write(response_suomi.content)
        f.close()
        
        print("TXT file downloaded successfully")
        
    else:
        print("Failed to download TXT file. Status code:", response_suomi.status_code)
        
## Load FIRMS SUOMI day file 
loadFirmsData()

## Process FIRMS txt file
def txt_to_parquet(directory_path, parquet_file_path):
    # Lista todos os arquivos .txt no diretório
    txt_files = glob.glob(os.path.join(directory_path, '*.txt'))

    # Initialize an empty DataFrame to store all data
    df_total = pd.DataFrame()

    # Loads each .txt file and concatenates to the total DataFrame
    for file in txt_files:
        df = pd.read_csv(file, sep=',', encoding='utf-8')  # Ajuste o separador se necessário
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
    
    # Export to .parquet
    df_total.to_parquet(parquet_file_path, index=False)

# Apply the function
directory_path = "/home/willianflores/localhost/nokekoiApp/datasets/suomi-npp-viirs-c2/South_America/"
parquet_file_path = "/home/willianflores/localhost/nokekoiApp/datasets/suomi-npp-viirs-c2/parquet/fire_data.parquet"

txt_to_parquet(directory_path, parquet_file_path)

