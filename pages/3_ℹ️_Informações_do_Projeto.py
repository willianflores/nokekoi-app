import datetime
import streamlit as st
from PIL import Image
from mobile_responsive_improvements import apply_mobile_first_improvements

## Page configuration
st.set_page_config(
  page_title = "Informações sobre o projeto", 
  page_icon = "./img/labgama-favicon.png",
  layout = "wide",
  initial_sidebar_state = "collapsed"
)

# Aplicar melhorias Mobile-First
apply_mobile_first_improvements()

# Meta tags para responsividade
st.markdown("""
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="theme-color" content="#0066cc">
</head>
""", unsafe_allow_html=True)

# Header mobile
st.markdown("""
<div class="mobile-header">
    <div class="app-title">
        <img src="./img/labgama-favicon.png" alt="Logo" class="header-logo">
        <span>Nokekoi - Informações</span>
    </div>
</div>

<style>
.mobile-header {
    display: none;
    align-items: center;
    justify-content: center;
    padding: 10px 15px;
    background: #ffffff;
    border-bottom: 1px solid #e0e0e0;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    height: 60px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.app-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: bold;
    font-size: 16px;
    color: #333;
}

.header-logo {
    width: 32px;
    height: 32px;
    border-radius: 50%;
}

@media (max-width: 767px) {
    .mobile-header {
        display: flex;
    }
}
</style>
""", unsafe_allow_html=True)

## Get the current year
current_year = datetime.datetime.now().year

with st.sidebar:
  st.markdown(
    f'<h5>Copyright (c) {current_year} &nbsp <a href="https://www.ufac.br/labgama">LabGAMA</a></h5>',
    unsafe_allow_html=True,
  )

st.markdown("# Descrição da Aplicação e dos Dados Disponibilizados")

st.markdown(
  """
    Essa aplicação web foi desenvolvida com o propósito de produzir informações 
    que permitam detectar de forma precoce a alteração da cobertura vegetal na Terra 
    Indígena Campinas/Katukina, ajudando a comunidade indígena a proteger seu patrimônio 
    natural. 
    
    Essa atividade foi desenvolvida no âmbito do Projeto **Sistema de Monitoramento 
    Precoce de Invasões da Terra Indígena Campinas/Katukina**, liderando por professores 
    e estudantes da [Universidade Federal do Acre](https://www.ufac.br/) com apoio 
    financeiro da [Transmissora Acre SPE S.A.](https://www.zenergiabr.com.br/subestacao/transmissora-acre), 
    no âmbito do Plano Básico Ambiental do Componente Indígena – CI-PBA da Terra Indígena Campinas Katukina/AC, 
    referente ao Licenciamento Ambiental da Linha de Transmissão (LT) 230 kV, no trecho Feijó-Cruzeiro do Sul.

    Para tanto utilizamos dados de focos de calor  provenientes 
    do **Sensor VIIRS**, [produto fogo ativo](https://www.earthdata.nasa.gov/learn/find-data/near-real-time/firms/viirs-i-band-375-m-active-fire-data), 
    resolução espacial de 375 m e atualização diária. Além disso utilizamos dados de 
    alertas de desmatamento do [RADD Forest Disturbance Alerts](https://data.globalforestwatch.org/datasets/gfw::deforestation-alerts-radd/about) 
    que usa dados de radar da missão Sentinel-1 para mapear alterações da cobertura 
    florestal com resolução espacial de 10 m e resolução de temporal 6 a 12 dias.

     Fonte dos dados: Focos de calor disponiblilizados pela 
    **NASA** [Fire Information for Resource Management System](https://firms.modaps.eosdis.nasa.gov/active_fire/) 
    (FIRMS). Alertas de desmatamento conforme, Reiche J, Mullissa A, 
    Slagter B, Gou Y, Tsendbazar N, Odongo-Braun C, Vollrath A, 
    Weisse M, Stolle F, Pickens A, Donchyts G, Clinton N, 
    Gorelick N & Herold M, (2021), Forest disturbance alerts for the 
    Congo Basin using Sentinel-1, Environmental Research Letters, 
    [https://doi.org/10.1088/1748-9326/abd0a8](https://doi.org/10.1088/1748-9326/abd0a8).


    Desenvolvido por: [Laboratório de Geoprocessamento Aplicado ao Meio 
    Ambiente](https://www.ufac.br/labgama), 
    [UFAC Campus Floresta](https://www.ufac.br/floresta).

    Equipe: [Dr. A. Willian Flores de Melo](https://lattes.cnpq.br/9339997282776018), 
    [Dra. Sonaira Silva](http://lattes.cnpq.br/7877159779121386), 
    [Dr. Igor Oliveira](http://lattes.cnpq.br/2419895860496067) e 
    [Henrique Melo](http://lattes.cnpq.br/4776096577200930).    
  """
)

st.markdown('---')

# Grid de logos responsivo
st.markdown("""
<div class="logos-section">
    <h3>Parceiros do Projeto</h3>
    <div class="logos-grid">
        <div class="logo-item">
            <img src="./img/Ufac_logo.png" alt="UFAC" class="partner-logo">
            <p>Universidade Federal do Acre</p>
        </div>
        <div class="logo-item">
            <img src="./img/Logo_agpn.png" alt="AGPN" class="partner-logo">
            <p>Associação dos Geógrafos Profissionais do Norte</p>
        </div>
        <div class="logo-item">
            <img src="./img/Logo_Acre_Transmissora.png" alt="Acre Transmissora" class="partner-logo">
            <p>Transmissora Acre SPE S.A.</p>
        </div>
    </div>
</div>

<style>
.logos-section {
    margin: 40px 0;
    text-align: center;
}

.logos-section h3 {
    color: #2c3e50;
    margin-bottom: 30px;
    font-size: 24px;
    font-weight: 600;
}

.logos-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 30px;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.logo-item {
    background: #ffffff;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    text-align: center;
}

.logo-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}

.partner-logo {
    max-width: 100%;
    height: auto;
    max-height: 120px;
    object-fit: contain;
    margin-bottom: 16px;
    filter: grayscale(20%);
    transition: filter 0.3s ease;
}

.logo-item:hover .partner-logo {
    filter: grayscale(0%);
}

.logo-item p {
    color: #666;
    font-size: 14px;
    font-weight: 500;
    margin: 0;
    line-height: 1.4;
}

/* Responsividade */
@media (min-width: 768px) {
    .logos-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 40px;
    }
    
    .partner-logo {
        max-height: 140px;
    }
    
    .logo-item p {
        font-size: 15px;
    }
}

@media (min-width: 1024px) {
    .logos-grid {
        grid-template-columns: repeat(3, 1fr);
    }
    
    .partner-logo {
        max-height: 160px;
    }
    
    .logo-item p {
        font-size: 16px;
    }
}

@media (min-width: 1200px) {
    .logos-section {
        padding: 0 20px;
    }
}
</style>
""", unsafe_allow_html=True)

# Navegação inferior para mobile
st.markdown("""
<div class="bottom-nav">
    <a href="../" class="nav-item">
        <div class="nav-icon">🔥</div>
        <div class="nav-label">Focos</div>
    </a>
    <a href="2_🪵_Alerta_de_Desmatamento" class="nav-item">
        <div class="nav-icon">🪵</div>
        <div class="nav-label">Desmate</div>
    </a>
    <a href="#" class="nav-item active">
        <div class="nav-icon">ℹ️</div>
        <div class="nav-label">Info</div>
    </a>
</div>

<style>
.bottom-nav {
    display: none;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #ffffff;
    border-top: 1px solid #e0e0e0;
    padding: 8px 0;
    justify-content: space-around;
    align-items: center;
    z-index: 1000;
    box-shadow: 0 -2px 8px rgba(0,0,0,0.1);
}

.nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-decoration: none;
    color: #666;
    padding: 8px 12px;
    border-radius: 8px;
    transition: all 0.3s ease;
    min-width: 60px;
}

.nav-item:hover,
.nav-item.active {
    color: #0066cc;
    background: #f0f8ff;
}

.nav-icon {
    font-size: 20px;
    margin-bottom: 4px;
}

.nav-label {
    font-size: 11px;
    font-weight: 500;
}

@media (max-width: 767px) {
    .bottom-nav {
        display: flex;
    }
    
    /* Adicionar espaço no rodapé para compensar navbar */
    .main .block-container {
        padding-bottom: 80px !important;
    }
}
</style>
""", unsafe_allow_html=True)

