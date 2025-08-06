#!/bin/bash

# Nokekoi App Installation Script
# Autor: Configuração automática
# Data: 2024

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d " " -f 2)
        log_info "Python $PYTHON_VERSION encontrado"
        
        # Check if version is 3.8+
        MIN_VERSION="3.8"
        if python3 -c "import sys; exit(0 if sys.version_info >= (3,8) else 1)"; then
            log_info "Versão do Python é compatível (>= 3.8)"
        else
            log_error "Python 3.8+ é necessário. Versão atual: $PYTHON_VERSION"
            exit 1
        fi
    else
        log_error "Python3 não encontrado. Por favor, instale Python 3.8+"
        exit 1
    fi
}

check_pip() {
    if command -v pip3 &> /dev/null; then
        log_info "pip3 encontrado"
    elif command -v pip &> /dev/null; then
        log_info "pip encontrado"
        alias pip3=pip
    else
        log_error "pip não encontrado. Instalando..."
        python3 -m ensurepip --upgrade
    fi
}

create_directories() {
    log_info "Criando diretórios necessários..."
    
    directories=(
        "datasets"
        "datasets/suomi-npp-viirs-c2"
        "datasets/suomi-npp-viirs-c2/South_America"
        "datasets/suomi-npp-viirs-c2/parquet"
        "datasets/shp"
        "datasets/radd"
        "logs"
    )
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            log_info "Diretório criado: $dir"
        fi
    done
}

setup_virtual_environment() {
    log_info "Configurando ambiente virtual..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        log_info "Ambiente virtual criado"
    else
        log_warn "Ambiente virtual já existe"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    log_info "Ambiente virtual ativado"
    
    # Upgrade pip
    pip install --upgrade pip
}

install_dependencies() {
    log_info "Instalando dependências Python..."
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        log_info "Dependências instaladas com sucesso"
    else
        log_error "Arquivo requirements.txt não encontrado"
        exit 1
    fi
}

setup_environment() {
    log_info "Configurando variáveis de ambiente..."
    
    if [ ! -f ".env" ]; then
        if [ -f "env.example" ]; then
            cp env.example .env
            log_info "Arquivo .env criado a partir do exemplo"
            log_warn "IMPORTANTE: Edite o arquivo .env com suas configurações!"
            log_warn "Especialmente o token NTR_TOKEN da NASA FIRMS"
        else
            log_error "Arquivo env.example não encontrado"
            exit 1
        fi
    else
        log_warn "Arquivo .env já existe - não sobrescrevendo"
    fi
}

setup_systemd_service() {
    if [ "$1" = "production" ]; then
        log_info "Configurando serviço systemd para produção..."
        
        SERVICE_FILE="/etc/systemd/system/nokekoi.service"
        CURRENT_DIR=$(pwd)
        USER=$(whoami)
        
        cat > nokekoi.service << EOF
[Unit]
Description=Nokekoi App - Fire Monitoring
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$CURRENT_DIR
Environment=PATH=$CURRENT_DIR/venv/bin
ExecStart=$CURRENT_DIR/venv/bin/streamlit run 1_🔥_Foco_de_Calor.py --server.port=8501 --server.address=0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

        log_info "Arquivo de serviço criado: nokekoi.service"
        log_warn "Para instalar o serviço, execute:"
        log_warn "sudo cp nokekoi.service /etc/systemd/system/"
        log_warn "sudo systemctl enable nokekoi"
        log_warn "sudo systemctl start nokekoi"
    fi
}

run_tests() {
    log_info "Executando testes básicos..."
    
    # Test Python imports
    python3 -c "
import sys
print('Python version:', sys.version)

try:
    import streamlit
    print('✓ Streamlit OK')
except ImportError as e:
    print('✗ Streamlit Error:', e)
    sys.exit(1)

try:
    import pandas
    print('✓ Pandas OK')
except ImportError as e:
    print('✗ Pandas Error:', e)
    sys.exit(1)

try:
    import geopandas
    print('✓ GeoPandas OK')
except ImportError as e:
    print('✗ GeoPandas Error:', e)
    sys.exit(1)

try:
    import folium
    print('✓ Folium OK')
except ImportError as e:
    print('✗ Folium Error:', e)
    sys.exit(1)

print('Todos os testes básicos passaram!')
"
}

main() {
    log_info "🔥 Iniciando instalação do Nokekoi App..."
    
    # Parse arguments
    MODE="development"
    if [ "$1" = "production" ]; then
        MODE="production"
        log_info "Modo de produção selecionado"
    else
        log_info "Modo de desenvolvimento selecionado"
    fi
    
    # Run installation steps
    check_python
    check_pip
    create_directories
    setup_virtual_environment
    install_dependencies
    setup_environment
    
    if [ "$MODE" = "production" ]; then
        setup_systemd_service production
    fi
    
    run_tests
    
    log_info "✅ Instalação concluída com sucesso!"
    
    echo ""
    log_info "Próximos passos:"
    log_warn "1. Edite o arquivo .env com suas configurações"
    log_warn "2. Configure seu token NASA no NTR_TOKEN"
    
    if [ "$MODE" = "development" ]; then
        log_warn "3. Execute: source venv/bin/activate"
        log_warn "4. Execute: streamlit run 1_🔥_Foco_de_Calor.py"
    else
        log_warn "3. Configure o serviço systemd (veja instruções acima)"
        log_warn "4. Configure SSL se necessário"
    fi
    
    echo ""
    log_info "Para mais informações, consulte o README.md"
}

# Run main function
main "$@" 