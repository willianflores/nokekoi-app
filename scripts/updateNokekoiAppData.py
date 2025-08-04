from updateNokekoiAppDataFunctions import *
from path_config import get_path_config
import logging
import sys
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/update_nokekoi.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Configuração de caminhos inteligente
PATHS = get_path_config()

def safe_execute(func, *args, **kwargs):
    """Executa função com tratamento de erro seguro"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logging.error(f"Erro ao executar {func.__name__}: {e}")
        return None

def validate_paths():
    """Valida se os caminhos necessários existem"""
    required_paths = ['suomi_data_path', 'shp_path', 'parquet_path', 'radd_path']
    for path_key in required_paths:
        if path_key not in PATHS:
            logging.error(f"Caminho {path_key} não configurado")
            return False
        if not os.path.exists(PATHS[path_key]):
            logging.error(f"Caminho não existe: {PATHS[path_key]}")
            return False
    return True

def validate_files_exist(files_list):
    """Valida se arquivos necessários existem"""
    for file_path in files_list:
        if not os.path.exists(file_path):
            logging.error(f"Arquivo necessário não encontrado: {file_path}")
            return False
    return True

# Início do processamento
logging.info("=== INICIANDO ATUALIZAÇÃO DOS DADOS NOKEKOI ===")

# Validar caminhos antes de começar
if not validate_paths():
    logging.error("Falha na validação de caminhos. Abortando execução.")
    sys.exit(1)

## ETAPA 1: Download and process fire data
logging.info("ETAPA 1: Carregando token e fazendo download dos dados FIRMS...")
try:
    NTR_TOKEN = loadTokenFromFile()
    if not NTR_TOKEN:
        raise Exception("Token não pôde ser carregado")
    
    loadFirmsData(NTR_TOKEN)
    logging.info("✅ Download dos dados FIRMS concluído com sucesso")
except Exception as e:
    logging.error(f"❌ FALHA na ETAPA 1 - Download FIRMS: {e}")
    sys.exit(1)

## ETAPA 2: Load TI and TI Buffer boundaries
logging.info("ETAPA 2: Carregando limites da Terra Indígena...")
try:
    ti_shp_path = os.path.join(PATHS['shp_path'], 'TI_Campinas_Katukina.shp')
    ti_buffer_shp_path = os.path.join(PATHS['shp_path'], 'TI_Campinas_Katukina_Buffer10km.shp')
    
    # Validar se arquivos existem
    required_shp_files = [ti_shp_path, ti_buffer_shp_path]
    if not validate_files_exist(required_shp_files):
        raise Exception("Arquivos shapefile da TI não encontrados")
    
    ti = import_shp(ti_shp_path)
    ti_buffer = import_shp(ti_buffer_shp_path)
    
    if ti is None or ti_buffer is None:
        raise Exception("Falha ao carregar shapefiles da TI")
    
    logging.info("✅ Limites da Terra Indígena carregados com sucesso")
except Exception as e:
    logging.error(f"❌ FALHA na ETAPA 2 - Carregamento TI: {e}")
    sys.exit(1)

## ETAPA 3: Process FIRMS txt file to parquet
logging.info("ETAPA 3: Convertendo arquivos TXT FIRMS para Parquet...")
try:
    directory_path = PATHS['suomi_data_path']
    parquet_file_path = os.path.join(PATHS['parquet_path'], 'fire_data.parquet')
    
    # Verificar se há arquivos txt na pasta
    txt_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
    if not txt_files:
        raise Exception(f"Nenhum arquivo .txt encontrado em {directory_path}")
    
    txtToParquet(directory_path, parquet_file_path)
    
    # Verificar se o arquivo parquet foi criado
    if not os.path.exists(parquet_file_path):
        raise Exception("Arquivo parquet não foi criado")
    
    logging.info(f"✅ Conversão para Parquet concluída: {len(txt_files)} arquivos processados")
except Exception as e:
    logging.error(f"❌ FALHA na ETAPA 3 - Conversão TXT para Parquet: {e}")
    sys.exit(1)

## ETAPA 4: Generate fire data for different time periods
logging.info("ETAPA 4: Gerando dados de fogo para diferentes períodos...")
try:
    # Verificar se o parquet existe antes de processar
    parquet_file_path = os.path.join(PATHS['parquet_path'], 'fire_data.parquet')
    if not os.path.exists(parquet_file_path):
        raise Exception("Arquivo fire_data.parquet não encontrado")
    
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

    # Loop for dynamic calls with error handling
    processed_count = 0
    for bound_name, file_prefix in bounds:
        for start, days_suffix in start_dates:
            try:
                output_filename = f"{file_prefix}_{days_suffix}"
                getFireData(bound_name, start, output_filename)
                processed_count += 1
                logging.info(f"   ✓ Processado: {output_filename}")
            except Exception as e:
                logging.error(f"   ✗ Erro ao processar {file_prefix}_{days_suffix}: {e}")
                raise Exception(f"Falha no processamento de dados de fogo: {e}")
    
    logging.info(f"✅ Processamento de dados de fogo concluído: {processed_count} arquivos gerados")
except Exception as e:
    logging.error(f"❌ FALHA na ETAPA 4 - Processamento dados de fogo: {e}")
    sys.exit(1)

## ETAPA 5: Download and process RADD data
logging.info("ETAPA 5: Fazendo download e processamento dos dados RADD...")
try:
    loadRaddRasterData()
    
    # Verificar se o arquivo RADD foi baixado
    radd_original = os.path.join(PATHS['radd_path'], '00N_080W.tif')
    if not os.path.exists(radd_original):
        raise Exception("Arquivo RADD original não foi baixado")
    
    logging.info("✅ Download dos dados RADD concluído")
except Exception as e:
    logging.error(f"❌ FALHA na ETAPA 5 - Download RADD: {e}")
    sys.exit(1)

## ETAPA 6: Clip RADD image
logging.info("ETAPA 6: Recortando imagem RADD para área de interesse...")
try:
    inshp = os.path.join(PATHS['shp_path'], 'TI_Campinas_Katukina_Buffer10km_All.shp')
    inRas = os.path.join(PATHS['radd_path'], '00N_080W.tif')
    outRas = os.path.join(PATHS['radd_path'], '00N_080W_clip.tif')
    
    # Verificar se arquivo shapefile existe
    if not os.path.exists(inshp):
        raise Exception(f"Arquivo shapefile para recorte não encontrado: {inshp}")
    
    # Verificar se arquivo raster existe
    if not os.path.exists(inRas):
        raise Exception(f"Arquivo raster RADD não encontrado: {inRas}")
    
    imgClip(inshp, inRas, outRas)
    
    # Verificar se o recorte foi criado
    if not os.path.exists(outRas):
        raise Exception("Arquivo RADD recortado não foi criado")
    
    logging.info("✅ Recorte da imagem RADD concluído")
except Exception as e:
    logging.error(f"❌ FALHA na ETAPA 6 - Recorte RADD: {e}")
    sys.exit(1)

## ETAPA 7: Process RADD image to geoparquet
logging.info("ETAPA 7: Processando dados RADD para diferentes períodos...")
try:
    radd_path = os.path.join(PATHS['radd_path'], '00N_080W_clip.tif')
    
    # Verificar se arquivo recortado existe
    if not os.path.exists(radd_path):
        raise Exception("Arquivo RADD recortado não encontrado")

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

    # Loop for dynamic calls with error handling
    processed_radd_count = 0
    for bound_name, file_prefix in bounds_radd:
        for start, days_suffix in start_dates_radd:
            try:
                output_filename = f"{file_prefix}_{days_suffix}"
                processRaddData(radd_path, bound_name, start, output_filename)
                processed_radd_count += 1
                logging.info(f"   ✓ Processado: {output_filename}")
            except Exception as e:
                logging.error(f"   ✗ Erro ao processar {file_prefix}_{days_suffix}: {e}")
                raise Exception(f"Falha no processamento de dados RADD: {e}")
    
    logging.info(f"✅ Processamento de dados RADD concluído: {processed_radd_count} arquivos gerados")
except Exception as e:
    logging.error(f"❌ FALHA na ETAPA 7 - Processamento dados RADD: {e}")
    sys.exit(1)

# FINALIZAÇÃO
logging.info("🎉 === ATUALIZAÇÃO DOS DADOS NOKEKOI CONCLUÍDA COM SUCESSO ===")
logging.info(f"Timestamp de conclusão: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
logging.info("Todas as etapas foram executadas sem erros críticos.")