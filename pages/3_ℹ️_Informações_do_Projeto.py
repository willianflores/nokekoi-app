import datetime
import streamlit as st
from PIL import Image
from mobile_responsive_improvements import apply_mobile_first_improvements

## Page configuration
st.set_page_config(
  page_title = "Informações sobre o projeto", 
  page_icon = "./img/labgama-favicon.png",
  layout = "centered",
  initial_sidebar_state = "expanded"
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

<style>
/* Controle do sidebar responsivo */
@media (max-width: 767px) {
    /* Mobile - sidebar otimizado */
    [data-testid="stSidebar"] {
        top: 0 !important;
        height: 100vh !important;
        z-index: 999 !important;
        background-color: #262730 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Corrigir faixa branca no mobile */
    [data-testid="stSidebar"] > div {
        background-color: #262730 !important;
        height: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Corrigir todos os elementos internos */
    [data-testid="stSidebar"] * {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Corrigir espaçamento superior específico */
    [data-testid="stSidebar"] .css-1d391kg,
    [data-testid="stSidebar"] .css-1d391kg > div,
    [data-testid="stSidebar"] header,
    [data-testid="stSidebar"] header > div {
        margin: 0 !important;
        padding: 0 !important;
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Forçar cor de fundo em todos os elementos */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] * {
        background-color: #262730 !important;
    }
}

@media (min-width: 768px) {
    /* Desktop - sidebar expandido por padrão */
    [data-testid="stSidebar"] {
        transform: translateX(0) !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Header mobile
st.markdown("""
<div class="mobile-header">
    <div class="app-title">
        <img src="../img/labgama-favicon.png" alt="Logo" class="header-logo">
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

## Add logo to sidebar
def add_logo():
  st.html("""
    <style>
      [alt=Logo] {
        height: 70%;
        margin-top: 10%;
        margin-bottom: 0%;
        margin-left: 5%;
        margin-right: 5%;
      }
    </style>
          """
  )

  st.logo('./img/Ufac_logo.png')
  
add_logo()

## Get the current year
current_year = datetime.datetime.now().year

with st.sidebar:
  st.markdown(
    f'<h5>Copyright (c) {current_year} &nbsp <a href="https://www.ufac.br/labgama">LabGAMA</a></h5>',
    unsafe_allow_html=True,
  )

st.markdown("""
<h1 style="color: #999999; text-align: center; margin: 30px 0; font-size: 28px;">Descrição da Aplicação e dos Dados Disponibilizados</h1>
""", unsafe_allow_html=True)

st.markdown(
  """
  <div style="color: #999999; line-height: 1.8; font-size: 18px;">
    Essa aplicação web foi desenvolvida com o propósito de produzir informações 
    que permitam detectar de forma precoce a alteração da cobertura vegetal na Terra 
    Indígena Campinas/Katukina, ajudando a comunidade indígena a proteger seu patrimônio 
    natural. 
    
    Essa atividade foi desenvolvida no âmbito do Projeto <strong>Sistema de Monitoramento 
    Precoce de Invasões da Terra Indígena Campinas/Katukina</strong>, liderando por professores 
    e estudantes da <a href="https://www.ufac.br/" style="color: #87CEEB;">Universidade Federal do Acre</a> com apoio 
    financeiro da <a href="https://www.zenergiabr.com.br/subestacao/transmissora-acre" style="color: #87CEEB;">Transmissora Acre SPE S.A.</a>, 
    no âmbito do Plano Básico Ambiental do Componente Indígena – CI-PBA da Terra Indígena Campinas Katukina/AC, 
    referente ao Licenciamento Ambiental da Linha de Transmissão (LT) 230 kV, no trecho Feijó-Cruzeiro do Sul.

    Para tanto utilizamos dados de focos de calor provenientes 
    do <strong>Sensor VIIRS</strong>, <a href="https://www.earthdata.nasa.gov/learn/find-data/near-real-time/firms/viirs-i-band-375-m-active-fire-data" style="color: #87CEEB;">produto fogo ativo</a>, 
    resolução espacial de 375 m e atualização diária. Além disso utilizamos dados de 
    alertas de desmatamento do <a href="https://data.globalforestwatch.org/datasets/gfw::deforestation-alerts-radd/about" style="color: #87CEEB;">RADD Forest Disturbance Alerts</a> 
    que usa dados de radar da missão Sentinel-1 para mapear alterações da cobertura 
    florestal com resolução espacial de 10 m e resolução de temporal 6 a 12 dias.

    Fonte dos dados: Focos de calor disponiblilizados pela 
    <strong>NASA</strong> <a href="https://firms.modaps.eosdis.nasa.gov/active_fire/" style="color: #87CEEB;">Fire Information for Resource Management System</a> 
    (FIRMS). Alertas de desmatamento conforme, Reiche J, Mullissa A, 
    Slagter B, Gou Y, Tsendbazar N, Odongo-Braun C, Vollrath A, 
    Weisse M, Stolle F, Pickens A, Donchyts G, Clinton N, 
    Gorelick N & Herold M, (2021), Forest disturbance alerts for the 
    Congo Basin using Sentinel-1, Environmental Research Letters, 
    <a href="https://doi.org/10.1088/1748-9326/abd0a8" style="color: #87CEEB;">https://doi.org/10.1088/1748-9326/abd0a8</a>.

    Desenvolvido por: <a href="https://www.ufac.br/labgama" style="color: #87CEEB;">Laboratório de Geoprocessamento Aplicado ao Meio 
    Ambiente</a>, 
    <a href="https://www.ufac.br/floresta" style="color: #87CEEB;">UFAC Campus Floresta</a>.

    Equipe: <a href="https://lattes.cnpq.br/9339997282776018" style="color: #87CEEB;">Dr. A. Willian Flores de Melo</a>, 
    <a href="http://lattes.cnpq.br/7877159779121386" style="color: #87CEEB;">Dra. Sonaira Silva</a>, 
    <a href="http://lattes.cnpq.br/2419895860496067" style="color: #87CEEB;">Dr. Igor Oliveira</a> e 
    <a href="http://lattes.cnpq.br/4776096577200930" style="color: #87CEEB;">Henrique Melo</a>.
  </div>
  """,
  unsafe_allow_html=True
)

st.markdown('---')

st.markdown("""
<h3 style="color: white; text-align: center; margin: 20px 0; font-size: 24px;">Parceiros do Projeto</h3>

<style>
/* Responsividade para os logos */
@media (max-width: 767px) {
    /* Mobile - logos médios */
    .stImage img {
        max-width: 130px !important;
        height: auto !important;
    }
    
    /* Centralizar containers dos logos */
    [data-testid="column"] {
        text-align: center !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
}

@media (min-width: 768px) and (max-width: 1024px) {
    /* Tablet - logos médios */
    .stImage img {
        max-width: 150px !important;
        height: auto !important;
    }
    
    /* Centralizar containers dos logos */
    [data-testid="column"] {
        text-align: center !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
}

@media (min-width: 1025px) {
    /* Desktop - logos normais */
    .stImage img {
        max-width: 180px !important;
        height: auto !important;
    }
    
    /* Centralizar containers dos logos */
    [data-testid="column"] {
        text-align: center !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large", vertical_alignment="center")

with col1:
    ufac = Image.open("img/Ufac_logo.png")
    st.image(ufac, width=180)

with col2:
    agpn = Image.open("img/Logo_agpn.png")
    st.image(agpn, width=180)
  
with col3:
    acre_transmissora = Image.open("img/Logo_Acre_Transmissora.png")
    st.image(acre_transmissora, width=180)

# Adicionar espaçamento depois dos logos
st.markdown("---")



