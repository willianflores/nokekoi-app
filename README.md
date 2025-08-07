# Nokekoi App 🔥

Real-time Fire Monitoring System for the Campinas/Katukina Indigenous Territory

## 📋 Description

The **Nokekoi App** is a web application developed in Streamlit for real-time monitoring of fire hotspots in the Campinas/Katukina Indigenous Territory in Acre, Brazil. The system uses NASA FIRMS (Fire Information for Resource Management System) data to detect and analyze fire events.

## ✨ Features

- 🔥 **Real-time Monitoring**: Visualization of updated fire hotspots
- 🗺️ **Interactive Maps**: Geospatial interface with Folium and Streamlit
- 📊 **Data Analysis**: Processing and statistical analysis of events
- 🚨 **Alert System**: Automatic email notifications
- 📈 **Dashboard**: Visualizations and metrics of fire data
- 🔄 **Automatic Updates**: Periodic synchronization with NASA APIs
- 📱 **Responsive Interface**: Compatible with mobile devices

## 🛠️ Technologies

- **Python 3.8+**
- **Streamlit** - Main web framework
- **GeoPandas** - Geospatial data processing
- **Folium** - Interactive maps
- **Pandas** - Data manipulation
- **NASA FIRMS API** - Fire hotspot data source
- **RADD API** - Deforestation data

## 🚀 Installation

### Development

1. **Clone the repository**:
```bash
git clone <repository-url>
cd nokekoi-app
```

2. **Run the installation script**:
```bash
chmod +x install.sh
./install.sh
```

3. **Configure environment variables**:
```bash
cp env.example .env
# Edit the .env file with your configurations
```

4. **Run the application**:
```bash
source venv/bin/activate
streamlit run 1_🔥_Foco_de_Calor.py
```

### Production

```bash
./install.sh production
```

## ⚙️ Configuration

### Environment Variables

Copy the `env.example` file to `.env` and configure:

```bash
# NASA FIRMS API Token
NTR_TOKEN=your_nasa_token_here

# Data paths
DATASET_PATH=/path/to/datasets
SUOMI_DATA_PATH=/path/to/suomi/data
PARQUET_PATH=/path/to/parquet/files

# Email settings
EMAIL_SERVER=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# SSL settings (production)
SSL_CERT_PATH=/path/to/cert.pem
SSL_KEY_PATH=/path/to/key.pem
```

### NASA FIRMS Token

The application has a **hybrid token management system**:

#### **Option 1: Manual (Recommended for development)**
1. Access: https://firms.modaps.eosdis.nasa.gov/api/
2. Register to obtain a token
3. Configure the `NTR_TOKEN` variable in the `.env` file

#### **Option 2: Automatic Renewal (Recommended for production)**
```bash
# Configure NASA credentials in .env (optional)
NASA_USERNAME=your_nasa_username
NASA_PASSWORD=your_nasa_password

# Run automatic renewal
python scripts/token_manager.py
```

#### **Option 3: Scheduled Automation (Production)**
```bash
# Add to crontab for weekly renewal
0 2 * * 0 cd /path/to/nokekoi-app && ./scripts/auto_renew_token.py >> logs/token_renewal.log 2>&1
```

#### **Token Priority:**
1. **Environment variable** (.env) - Highest priority
2. **Token file** (automatic renewal) - Fallback
3. **Error** - If none found

## 🏗️ Project Structure

```
nokekoi-app/
├── 1_🔥_Foco_de_Calor.py          # Main application
├── pages/                         # Streamlit pages
├── scripts/                       # Utility scripts
│   ├── loadFirmsData.py          # NASA data loading
│   ├── backup.sh                 # Backup script
│   ├── test_dependencies.py      # Dependency tests
│   └── test_nasa_api.py          # NASA API tests
├── datasets/                      # Local data (gitignore)
├── .streamlit/                    # Streamlit configurations
├── requirements.txt               # Python dependencies
├── env.example                    # Environment template
├── install.sh                     # Installation script
└── README.md                      # Documentation
```

## 🧪 Testing

### Dependency Test
```bash
python scripts/test_dependencies.py
```

### NASA API Test
```bash
python scripts/test_nasa_api.py
```

### Complete Test
```bash
./install.sh test
```

## 📦 APIs Used

- **NASA FIRMS**: Fire Information for Resource Management System
- **NASA RADD**: Radar for Detecting Deforestation

## 🔐 Security

- Tokens and credentials via environment variables
- SSL certificates for production
- Input data validation
- Audit logs

## 🔄 Backup

Configure automatic backup:

```bash
# Add to crontab
0 2 * * * /path/to/nokekoi-app/scripts/backup.sh
```

## 🐳 Docker (Optional)

```bash
# Build
docker build -t nokekoi-app .

# Run
docker run -p 8501:8501 --env-file .env nokekoi-app
```

## 📝 Logs

Logs are saved in:
- `logs/app.log` - Main application log
- `logs/error.log` - Error logs
- `logs/backup.log` - Backup logs

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the [MIT](LICENSE) license.

## 📞 Support

For support and questions:
- Email: support@nokekoi.org
- Issues: [GitHub Issues](https://github.com/user/nokekoi-app/issues)

## 🙏 Acknowledgments

- **NASA FIRMS** - Provision of fire hotspot data
- **Campinas/Katukina Indigenous Territory** - Collaboration and local data
- **Streamlit Community** - Framework and technical support
