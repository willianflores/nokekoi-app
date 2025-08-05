# Nokekoi App 🔥

Sistema de Monitoramento de Focos de Calor para a Terra Indígena Campinas/Katukina

## 📋 Descrição

A **Nokekoi App** é uma aplicação web desenvolvida em Streamlit para monitoramento em tempo real de focos de calor na Terra Indígena Campinas/Katukina no Acre. O sistema utiliza dados da NASA FIRMS (Fire Information for Resource Management System) para detectar e analisar eventos de queimadas.

## ✨ Funcionalidades

- 🔥 **Monitoramento em Tempo Real**: Visualização de focos de calor atualizados
- 🗺️ **Mapas Interativos**: Interface geoespacial com Folium e Streamlit
- 📊 **Análise de Dados**: Processamento e análise estatística dos eventos
- 🚨 **Sistema de Alertas**: Notificações automáticas via email
- 📈 **Dashboard**: Visualizações e métricas dos dados de queimadas
- 🔄 **Atualização Automática**: Sincronização periódica com APIs NASA
- 📱 **Interface Responsiva**: Compatível com dispositivos móveis

## 🛠️ Tecnologias

- **Python 3.8+**
- **Streamlit** - Framework web principal
- **GeoPandas** - Processamento de dados geoespaciais
- **Folium** - Mapas interativos
- **Pandas** - Manipulação de dados
- **NASA FIRMS API** - Fonte de dados de focos de calor
- **RADD API** - Dados de desmatamento

## 🚀 Instalação

### Desenvolvimento

1. **Clone o repositório**:
```bash
git clone <repository-url>
cd nokekoi-app
```

2. **Execute o script de instalação**:
```bash
chmod +x install.sh
./install.sh
```

3. **Configure as variáveis de ambiente**:
```bash
cp env.example .env
# Edite o arquivo .env com suas configurações
```

4. **Execute a aplicação**:
```bash
source venv/bin/activate
streamlit run 1_🔥_Foco_de_Calor.py
```

### Produção

```bash
./install.sh production
```

## ⚙️ Configuração

### Variáveis de Ambiente

Copie o arquivo `env.example` para `.env` e configure:

```bash
# NASA FIRMS API Token
NTR_TOKEN=your_nasa_token_here

# Caminhos de dados
DATASET_PATH=/path/to/datasets
SUOMI_DATA_PATH=/path/to/suomi/data
PARQUET_PATH=/path/to/parquet/files

# Configurações de email
EMAIL_SERVER=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Configurações SSL (produção)
SSL_CERT_PATH=/path/to/cert.pem
SSL_KEY_PATH=/path/to/key.pem
```

### Token NASA FIRMS

A aplicação possui **sistema híbrido** de gerenciamento de tokens:

#### **Opção 1: Manual (Recomendada para desenvolvimento)**
1. Acesse: https://firms.modaps.eosdis.nasa.gov/api/
2. Registre-se para obter um token
3. Configure a variável `NTR_TOKEN` no arquivo `.env`

#### **Opção 2: Renovação Automática (Recomendada para produção)**
```bash
# Configure credenciais NASA no .env (opcional)
NASA_USERNAME=seu_usuario_nasa
NASA_PASSWORD=sua_senha_nasa

# Execute renovação automática
python scripts/token_manager.py
```

#### **Opção 3: Agendamento Automático (Produção)**
```bash
# Adicione ao crontab para renovação semanal
0 2 * * 0 cd /caminho/para/nokekoi-app && ./scripts/auto_renew_token.py >> logs/token_renewal.log 2>&1
```

#### **Prioridade de Tokens:**
1. **Variável de ambiente** (.env) - Mais alta prioridade
2. **Arquivo de token** (renovação automática) - Fallback
3. **Erro** - Se nenhum encontrado

## 🏗️ Estrutura do Projeto

```
nokekoi-app/
├── 1_🔥_Foco_de_Calor.py          # Aplicação principal
├── pages/                         # Páginas do Streamlit
├── scripts/                       # Scripts utilitários
│   ├── loadFirmsData.py          # Carregamento dados NASA
│   ├── backup.sh                 # Script de backup
│   ├── test_dependencies.py      # Testes de dependências
│   └── test_nasa_api.py          # Testes API NASA
├── datasets/                      # Dados locais (gitignore)
├── .streamlit/                    # Configurações Streamlit
├── requirements.txt               # Dependências Python
├── env.example                    # Template de variáveis
├── install.sh                     # Script de instalação
└── README.md                      # Documentação
```

## 🧪 Testes

### Teste de Dependências
```bash
python scripts/test_dependencies.py
```

### Teste da API NASA
```bash
python scripts/test_nasa_api.py
```

### Teste Completo
```bash
./install.sh test
```

## 📦 APIs Utilizadas

- **NASA FIRMS**: Fire Information for Resource Management System
- **NASA RADD**: Radar for Detecting Deforestation

## 🔐 Segurança

- Tokens e credenciais via variáveis de ambiente
- Certificados SSL para produção
- Validação de entrada de dados
- Logs de auditoria

## 🔄 Backup

Configure backup automático:

```bash
# Adicione ao crontab
0 2 * * * /path/to/nokekoi-app/scripts/backup.sh
```

## 🐳 Docker (Opcional)

```bash
# Build
docker build -t nokekoi-app .

# Run
docker run -p 8501:8501 --env-file .env nokekoi-app
```

## 📝 Logs

Logs são salvos em:
- `logs/app.log` - Log principal da aplicação
- `logs/error.log` - Logs de erro
- `logs/backup.log` - Logs de backup

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).

## 📞 Suporte

Para suporte e dúvidas:
- Email: support@nokekoi.org
- Issues: [GitHub Issues](https://github.com/user/nokekoi-app/issues)

## 🙏 Agradecimentos

- **NASA FIRMS** - Fornecimento de dados de focos de calor
- **Terra Indígena Campinas/Katukina** - Colaboração e dados locais
- **Comunidade Streamlit** - Framework e suporte técnico
