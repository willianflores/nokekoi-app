"""
Configuração inteligente de caminhos para desenvolvimento e produção
"""
import os
import sys
from pathlib import Path

# Tenta carregar dotenv se disponível
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv não instalado. Usando apenas variáveis de ambiente do sistema.")

def detect_environment():
    """
    Detecta se estamos em ambiente de desenvolvimento ou produção
    """
    # Verifica indicadores de produção
    if os.getenv('ENVIRONMENT') == 'production':
        return 'production'
    
    # Verifica se está rodando como srvadmin (produção)
    if os.getenv('USER') == 'srvadmin':
        return 'production'
    
    # Verifica se o diretório de produção existe
    prod_path = Path('/home/srvadmin/nokekoiApp')
    if prod_path.exists():
        return 'production'
    
    # Por padrão, assume desenvolvimento
    return 'development'

def get_base_path():
    """
    Retorna o caminho base da aplicação baseado no ambiente
    """
    env = detect_environment()
    
    if env == 'production':
        # Produção: caminho do servidor
        return Path('/home/srvadmin/nokekoiApp')
    else:
        # Desenvolvimento: caminho relativo ou do usuário atual
        # Primeiro tenta encontrar a pasta nokekoi-app
        current_dir = Path(__file__).parent.parent  # sai de scripts/ para nokekoi-app/
        if current_dir.name == 'nokekoi-app':
            return current_dir
        
        # Se não encontrar, usa o caminho do usuário atual
        user = os.getenv('USER', 'willianflores')
        return Path(f'/home/{user}/localhost/nokekoi-app')

def get_datasets_path():
    """
    Retorna o caminho para a pasta datasets
    """
    # Primeiro verifica variável de ambiente
    env_path = os.getenv('DATASET_PATH')
    if env_path:
        return Path(env_path)
    
    # Senão, usa detecção automática
    base_path = get_base_path()
    return base_path / 'datasets'

def get_path_config():
    """
    Retorna configuração completa de caminhos
    """
    datasets_path = get_datasets_path()
    
    config = {
        'environment': detect_environment(),
        'base_path': get_base_path(),
        'datasets_path': datasets_path,
        'suomi_data_path': os.getenv('SUOMI_DATA_PATH', str(datasets_path / 'suomi-npp-viirs-c2' / 'South_America')),
        'parquet_path': os.getenv('PARQUET_PATH', str(datasets_path / 'suomi-npp-viirs-c2' / 'parquet')),
        'radd_path': os.getenv('RADD_PATH', str(datasets_path / 'radd')),
        'shp_path': os.getenv('SHP_PATH', str(datasets_path / 'shp')),
        'token_file': str(datasets_path / 'suomi-npp-viirs-c2' / 'token' / 'token.txt'),
        'logs_path': str(get_base_path() / 'logs'),
    }
    
    return config

def ensure_directories():
    """
    Cria os diretórios necessários se não existirem
    """
    config = get_path_config()
    
    directories = [
        config['datasets_path'],
        Path(config['suomi_data_path']),
        Path(config['parquet_path']),
        Path(config['radd_path']),
        Path(config['shp_path']),
        Path(config['token_file']).parent,
        Path(config['logs_path']),
        Path(config['radd_path']) / 'geoparquet',
    ]
    
    for directory in directories:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✅ Diretório verificado/criado: {directory}")
        except Exception as e:
            print(f"⚠️  Erro ao criar diretório {directory}: {e}")

def print_config():
    """
    Imprime a configuração atual de caminhos para debug
    """
    config = get_path_config()
    
    print("\n" + "="*50)
    print(f"🔧 CONFIGURAÇÃO DE CAMINHOS - AMBIENTE: {config['environment'].upper()}")
    print("="*50)
    
    for key, value in config.items():
        if key != 'environment':
            status = "✅" if Path(value).exists() else "❌"
            print(f"{status} {key.replace('_', ' ').title()}: {value}")
    
    print("="*50 + "\n")

if __name__ == "__main__":
    # Testa a configuração
    print_config()
    
    # Pergunta se deve criar diretórios faltantes
    config = get_path_config()
    missing_dirs = [k for k, v in config.items() if k != 'environment' and not Path(v).exists()]
    
    if missing_dirs:
        print(f"⚠️  Encontrados {len(missing_dirs)} diretórios faltantes.")
        response = input("Deseja criar os diretórios faltantes? (s/n): ")
        if response.lower() in ['s', 'sim', 'y', 'yes']:
            ensure_directories()
            print("✅ Diretórios criados com sucesso!")
    else:
        print("✅ Todos os diretórios existem!") 