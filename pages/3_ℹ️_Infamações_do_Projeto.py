import streamlit as st
from PIL import Image

## Page configuration
st.set_page_config(
  page_title = "Informações sobre o projeto", 
  page_icon = "./img/labgama-favicon.png",
 
)

with st.sidebar:
  st.markdown(
    '<h5>Copyright (c) 2024 &nbsp <a href="https://www.ufac.br/labgama">LabGAMA</a></h5>',
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
    financeiro da [Transmissora Acre SPE S.A.](https://www.zenergiabr.com.br/subestacao/transmissora-acre).

    Para tanto utilizamos dados de focos de calor dados de focos de calor provenientes 
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

col1, col2, col3 = st.columns(3)

with col1:
  ufac = Image.open("./img/Ufac_logo.png")
  st.image(
    ufac,
    
  )
  
with col3:
  acre_transmissora = Image.open("./img/Logo_Acre_Transmissora.png")
  st.image(
    acre_transmissora,
    
    
  )

