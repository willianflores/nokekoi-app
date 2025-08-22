from updateNokekoiAppDataFunctions import *
from path_config import get_path_config
import logging
import sys
import os
from datetime import datetime

# Criar diretório de logs automaticamente
def ensure_logs_directory():
    """Cria o diretório de logs se não existir"""
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        print(f"📁 Diretório de logs criado: {logs_dir}")

# Garantir que o diretório de logs existe
ensure_logs_directory()

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

# Variáveis globais para controle de execução
execution_status = {
    'etapa_1_firms': False,
    'etapa_2_ti_boundaries': False,
    'etapa_3_txt_to_parquet': False,
    'etapa_4_fire_data': False,
    'etapa_5_radd_download': False,
    'etapa_6_radd_clip': False,
    'etapa_7_radd_process': False
}

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

def check_prerequisites(etapa_name, required_conditions):
    """Verifica pré-condições antes de executar uma etapa"""
    logging.info(f"🔍 Verificando pré-condições para {etapa_name}...")
    
    for condition_name, condition_func in required_conditions.items():
        if not condition_func():
            logging.error(f"❌ Pré-condição não atendida: {condition_name}")
            return False
    
    logging.info(f"✅ Todas as pré-condições atendidas para {etapa_name}")
    return True

def mark_etapa_completed(etapa_key):
    """Marca uma etapa como concluída"""
    execution_status[etapa_key] = True
    logging.info(f"✅ {etapa_key} marcada como concluída")

def can_execute_etapa(etapa_key, required_etapas):
    """Verifica se uma etapa pode ser executada baseada nas etapas anteriores"""
    for required_etapa in required_etapas:
        if not execution_status.get(required_etapa, False):
            logging.error(f"❌ Etapa {etapa_key} não pode ser executada. Etapa {required_etapa} não foi concluída.")
            return False
    return True

def execute_etapa_with_validation(etapa_name, etapa_key, required_etapas, required_conditions, etapa_func):
    """Executa uma etapa com validações completas"""
    logging.info(f"🚀 Iniciando {etapa_name}...")
    
    # Verificar se etapas anteriores foram concluídas
    if not can_execute_etapa(etapa_key, required_etapas):
        logging.error(f"❌ {etapa_name} não pode ser executada devido a falhas em etapas anteriores")
        return False
    
    # Verificar pré-condições
    if not check_prerequisites(etapa_name, required_conditions):
        logging.error(f"❌ {etapa_name} não pode ser executada devido a pré-condições não atendidas")
        return False
    
    # Executar etapa
    try:
        resultado = etapa_func()
        if resultado is not False:  # Considera None como sucesso
            mark_etapa_completed(etapa_key)
            logging.info(f"✅ {etapa_name} concluída com sucesso")
            return True
        else:
            logging.error(f"❌ {etapa_name} falhou durante execução")
            return False
    except Exception as e:
        logging.error(f"❌ {etapa_name} falhou com exceção: {e}")
        return False

# Início do processamento
logging.info("=== INICIANDO ATUALIZAÇÃO DOS DADOS NOKEKOI ===")

# Validar caminhos antes de começar
if not validate_paths():
    logging.error("Falha na validação de caminhos. Abortando execução.")
    sys.exit(1)

# Funções de validação para cada etapa
def validate_token():
    """Valida se o token pode ser carregado"""
    try:
        token = loadTokenFromFile()
        return token is not None and "access_token" in token
    except:
        return False

def validate_firms_files():
    """Valida se arquivos FIRMS foram baixados"""
    directory_path = PATHS['suomi_data_path']
    txt_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
    return len(txt_files) > 0

def validate_shp_files():
    """Valida se arquivos shapefile existem"""
    ti_shp_path = os.path.join(PATHS['shp_path'], 'TI_Campinas_Katukina.shp')
    ti_buffer_shp_path = os.path.join(PATHS['shp_path'], 'TI_Campinas_Katukina_Buffer10km.shp')
    return os.path.exists(ti_shp_path) and os.path.exists(ti_buffer_shp_path)

def validate_parquet_file():
    """Valida se arquivo parquet foi criado"""
    parquet_file_path = os.path.join(PATHS['parquet_path'], 'fire_data.parquet')
    return os.path.exists(parquet_file_path)

def validate_radd_download():
    """Valida se dados RADD foram baixados"""
    radd_original = os.path.join(PATHS['radd_path'], '00N_080W.tif')
    return os.path.exists(radd_original)

def validate_radd_clip():
    """Valida se arquivo RADD foi recortado"""
    radd_clip = os.path.join(PATHS['radd_path'], '00N_080W_clip.tif')
    return os.path.exists(radd_clip)

# Variáveis globais para armazenar dados entre etapas
ti = None
ti_buffer = None

## ETAPA 1: Download and process fire data
def etapa_1_firms():
    """ETAPA 1: Download dos dados FIRMS"""
    global execution_status
    
    NTR_TOKEN = loadTokenFromFile()
    if not NTR_TOKEN:
        raise Exception("Token não pôde ser carregado")
    
    loadFirmsData(NTR_TOKEN)
    return True

execute_etapa_with_validation(
    "ETAPA 1: Download dos dados FIRMS",
    "etapa_1_firms",
    [],  # Não depende de etapas anteriores
    {"Token válido": validate_token},
    etapa_1_firms
)

## ETAPA 2: Load TI and TI Buffer boundaries
def etapa_2_ti_boundaries():
    """ETAPA 2: Carregamento dos limites da Terra Indígena"""
    global ti, ti_buffer
    
    ti_shp_path = os.path.join(PATHS['shp_path'], 'TI_Campinas_Katukina.shp')
    ti_buffer_shp_path = os.path.join(PATHS['shp_path'], 'TI_Campinas_Katukina_Buffer10km.shp')
    
    ti = import_shp(ti_shp_path)
    ti_buffer = import_shp(ti_buffer_shp_path)
    
    if ti is None or ti_buffer is None:
        raise Exception("Falha ao carregar shapefiles da TI")
    
    return True

execute_etapa_with_validation(
    "ETAPA 2: Carregamento dos limites da Terra Indígena",
    "etapa_2_ti_boundaries",
    [],  # Não depende de etapas anteriores
    {"Arquivos shapefile": validate_shp_files},
    etapa_2_ti_boundaries
)

## ETAPA 3: Process FIRMS txt file to parquet
def etapa_3_txt_to_parquet():
    """ETAPA 3: Conversão de arquivos TXT FIRMS para Parquet"""
    directory_path = PATHS['suomi_data_path']
    parquet_file_path = os.path.join(PATHS['parquet_path'], 'fire_data.parquet')
    
    txtToParquet(directory_path, parquet_file_path)
    return True

execute_etapa_with_validation(
    "ETAPA 3: Conversão de arquivos TXT FIRMS para Parquet",
    "etapa_3_txt_to_parquet",
    ["etapa_1_firms"],  # Depende dos dados FIRMS
    {"Arquivos FIRMS": validate_firms_files},
    etapa_3_txt_to_parquet
)

## ETAPA 4: Generate fire data for different time periods
def etapa_4_fire_data():
    """ETAPA 4: Geração de dados de fogo para diferentes períodos"""
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
    
    return True

execute_etapa_with_validation(
    "ETAPA 4: Geração de dados de fogo para diferentes períodos",
    "etapa_4_fire_data",
    ["etapa_2_ti_boundaries", "etapa_3_txt_to_parquet"],  # Depende dos limites e dados parquet
    {"Arquivo parquet": validate_parquet_file},
    etapa_4_fire_data
)

## ETAPA 5: Download and process RADD data
def etapa_5_radd_download():
    """ETAPA 5: Download dos dados RADD"""
    loadRaddRasterData()
    return True

execute_etapa_with_validation(
    "ETAPA 5: Download dos dados RADD",
    "etapa_5_radd_download",
    [],  # Não depende de etapas anteriores
    {},  # Sem pré-condições específicas
    etapa_5_radd_download
)

## ETAPA 6: Clip RADD image
def etapa_6_radd_clip():
    """ETAPA 6: Recorte da imagem RADD"""
    inshp = os.path.join(PATHS['shp_path'], 'TI_Campinas_Katukina_Buffer10km_All.shp')
    inRas = os.path.join(PATHS['radd_path'], '00N_080W.tif')
    outRas = os.path.join(PATHS['radd_path'], '00N_080W_clip.tif')
    
    imgClip(inshp, inRas, outRas)
    return True

execute_etapa_with_validation(
    "ETAPA 6: Recorte da imagem RADD",
    "etapa_6_radd_clip",
    ["etapa_2_ti_boundaries", "etapa_5_radd_download"],  # Depende dos limites e download RADD
    {"Download RADD": validate_radd_download},
    etapa_6_radd_clip
)

## ETAPA 7: Process RADD image to geoparquet
def etapa_7_radd_process():
    """ETAPA 7: Processamento de dados RADD para diferentes períodos"""
    radd_path = os.path.join(PATHS['radd_path'], '00N_080W_clip.tif')

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
    
    return True

execute_etapa_with_validation(
    "ETAPA 7: Processamento de dados RADD para diferentes períodos",
    "etapa_7_radd_process",
    ["etapa_2_ti_boundaries", "etapa_6_radd_clip"],  # Depende dos limites e recorte RADD
    {"Recorte RADD": validate_radd_clip},
    etapa_7_radd_process
)

# FINALIZAÇÃO COM VALIDAÇÃO COMPLETA
logging.info("🎉 === ATUALIZAÇÃO DOS DADOS NOKEKOI CONCLUÍDA COM SUCESSO ===")
logging.info(f"Timestamp de conclusão: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Verificar se todas as etapas foram concluídas
etapas_concluidas = sum(execution_status.values())
total_etapas = len(execution_status)
logging.info(f"📊 Status final: {etapas_concluidas}/{total_etapas} etapas concluídas")

if etapas_concluidas == total_etapas:
    logging.info("✅ Todas as etapas foram executadas sem erros críticos.")
else:
    logging.warning(f"⚠️ {total_etapas - etapas_concluidas} etapa(s) não foram concluídas devido a erros.")
    for etapa, status in execution_status.items():
        if not status:
            logging.warning(f"   ❌ {etapa} não foi concluída")