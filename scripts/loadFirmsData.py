## Import libraries
import requests
import os
from datetime import datetime, timedelta, date
import pytz
import pandas as pd
import glob
from dotenv import load_dotenv
from path_config import get_path_config

# Carrega variáveis de ambiente e configuração de caminhos
load_dotenv()
PATHS = get_path_config()

## Load FIRMS data function
def loadFirmsData():
    ## Variables
    # Obtém token usando sistema híbrido
    try:
        from token_manager import get_nasa_token
        token_data = get_nasa_token()
        NTR_TOKEN = token_data["access_token"]
    except ImportError:
        # Fallback para variável de ambiente
        NTR_TOKEN = os.getenv('NTR_TOKEN')
        if not NTR_TOKEN or NTR_TOKEN == 'your_nasa_token_here':
            raise ValueError("NTR_TOKEN não encontrado nas variáveis de ambiente. Configure o arquivo .env")
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

