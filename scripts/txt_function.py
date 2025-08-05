import pandas as pd
import os
import glob
from datetime import date, timedelta

def txt_to_parquet(directory_path, parquet_file_path):
    # Lista todos os arquivos .txt no diretório
    txt_files = glob.glob(os.path.join(directory_path, '*.csv'))

    # Inicializa um DataFrame vazio para armazenar todos os dados
    df_total = pd.DataFrame()

    # Carrega cada arquivo .txt e concatena ao DataFrame total
    for file in txt_files:
        df = pd.read_csv(file, sep=',', encoding='utf-8')  # Ajuste o separador se necessário
        df_total = pd.concat([df_total, df], ignore_index=True)
    
    #df_total.info()
    #df_total.memory_usage(deep=True)
    df_total["acq_date"] = pd.to_datetime(df_total["acq_date"])    
    df_total = df_total.filter(["latitude", "longitude", "brightness", "acq_date", "acq_time"])
    df_total = df_total.loc[df_total["acq_date"]>= pd.to_datetime(date.today() - timedelta(days=365))]
    
    # Exportar o DataFrame total para um arquivo .parquet
    df_total.to_parquet(parquet_file_path, index=False)

# Exemplo de uso da função
directory_path = "../datasets/suomi-npp-viirs-c2/csv"
parquet_file_path = "../datasets/suomi-npp-viirs-c2/parquet/fire_data.parquet"
txt_to_parquet(directory_path, parquet_file_path)

