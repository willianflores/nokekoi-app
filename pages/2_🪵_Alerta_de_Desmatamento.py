import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from streamlit_folium import folium_static
from folium import plugins
from PIL import Image
import base64
import glob
from datetime import date, timedelta

from shapely.geometry import box
import shapely.geometry
import rasterio
from rasterio.features import shapes

from branca.element import Template, MacroElement

import locale
from mobile_responsive_improvements import apply_mobile_first_improvements

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

## Page configuration
st.set_page_config(
  page_title = "Alertas de desmatamento na TI Campinas/Katukina", 
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

# @st.cache_data
# def get_base64_of_bin_file(png_file):
#     with open(png_file, "rb") as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# def build_markup_for_logo(
#   png_file,
#   background_position="50% 0%",
#   margin_top="10%",
#   image_width="",
#   image_height="70%",
# ):
#   binary_string = get_base64_of_bin_file(png_file)
#   return """
#           <style>
#               [data-testid="stSidebarNav"] {
#                   background-image: url("data:image/png;base64,%s");
#                   background-repeat: no-repeat;
#                   background-position: %s;
#                   margin-top: %s;
#                   background-size: %s %s;
#               }
#           </style>
#             """ % (
#         binary_string,
#         background_position,
#         margin_top,
#         image_width,
#         image_height,
#     )


# def add_logo(png_file):
#     logo_markup = build_markup_for_logo(png_file)
#     st.markdown(
#         logo_markup,
#         unsafe_allow_html=True,
#     )

# add_logo('./img/Ufac_logo.png')

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

# Header mobile
st.markdown("""
<div class="mobile-header">
    <div class="app-title">
        <img src="../img/labgama-favicon.png" alt="Logo" class="header-logo">
        <span>Nokekoi - Desmatamento</span>
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

## Sidebar
with st.sidebar:
  #st.image(logo, width=300)
  st.sidebar.header("Alertas de desmatameto")
    
  time = st.radio(
    "Selecione o período de análise:",
    (
      "15 dias",
      "1 mês",
      "2 meses",
      "3 meses",
      "6 meses",
      "1 ano"
    )
  )



@st.cache_data(ttl=600, hash_funcs={gpd.GeoDataFrame: lambda _: None})
def getShpData(parquet_path):
  
  return gpd.read_parquet(parquet_path)
  
ti = getShpData("./datasets/shp/TI_Campinas_Katukina.parquet")
ti_buffer = getShpData("./datasets/shp/TI_Campinas_Katukina_Buffer10km.parquet")

# df_fire.memory_usage(deep=True)
# df_fire.info()
# df_fire["confidence"].value_counts()

def getRaddData(data_type, time):
  """
  Load fire data based on type and time range.

  Parameters:
  data_type (str): The prefix of the dataset ('ti' or 'ti_buffer').
  time (str): The time range ('15 dias', '1 mês', '2 meses', etc.).

  Returns:
  GeoDataFrame: The loaded GeoParquet data as a GeoDataFrame.
  """
  # Define the mapping of time ranges to file suffixes
  time_map = {
    "15 dias": "15d",
    "1 mês": "30d",
    "2 meses": "60d",
    "3 meses": "90d",
    "6 meses": "180d",
    "1 ano": "365d",
  }
  
  # Validate input
  if time not in time_map:
    raise ValueError(f"Invalid time range: {time}. Valid options are: {', '.join(time_map.keys())}")
  if data_type not in ["ti", "ti_buffer"]:
    raise ValueError(f"Invalid data type: {data_type}. Valid options are: 'ti', 'ti_buffer'")
  
  # Construct the file path dynamically
  file_suffix = time_map[time]
  file_path = f"./datasets/radd/geoparquet/{data_type}_radd_{file_suffix}.geoparquet"
  
  # Load and return the dataset
  return gpd.read_parquet(file_path)

with st.spinner("Carregando dados..."):
  ti_radd_data = getRaddData(time=time, data_type="ti")
  buffer_radd_data = getRaddData(time=time, data_type="ti_buffer")
  
ti_radd_data["date"] = ti_radd_data["date"].dt.strftime('%d/%m/%Y')
buffer_radd_data["date"] = buffer_radd_data["date"].dt.strftime("%d/%m/%Y")

porj_area = "+proj=aea +lat_1=10 +lat_2=-40 +lat_0=-25 +lon_0=-50 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs "

ti_radd_data_proj = ti_radd_data.to_crs(porj_area)
ti_radd_data_proj['area_ha'] = ti_radd_data_proj['geometry'].area/10000

buffer_radd_data_proj = buffer_radd_data.to_crs(porj_area)
buffer_radd_data_proj['area_ha'] = buffer_radd_data_proj['geometry'].area/10000

ti_radd_n = f"{round(ti_radd_data_proj['area_ha'].sum()):,}".replace(",", ".")
buffer_radd_n = f"{round(buffer_radd_data_proj['area_ha'].sum()):,}".replace(",", ".")

## Legend
template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="https://code.jquery.com/ui/1.13.3/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-3.7.1.js"></script>
  <script src="https://code.jquery.com/ui/1.13.3/jquery-ui.js"></script>
  
  <script>
    $( function() {
      $( "#maplegend" ).draggable({
                      start: function (event, ui) {
                          $(this).css({
                              right: "auto",
                              top: "auto",
                              bottom: "auto"
                          });
                      }
                  });
    });

  </script>
</head>
<body>


<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
     
  <div class='legend-scale'>
    <ul class='legend-labels'>
      <li><span style='background:red;opacity: 1;'></span>Alertas de desmatamento na TI</li>
      <li><span style='background:#ff6666;opacity: 1;'></span>Alertas de desmatamento na Área de Amortecimento</li>

    </ul>
  </div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    color: #0f0f0f;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    color: #0f0f0f;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

macro = MacroElement()
macro._template = Template(template)

# Deforestation map - Configuração com zoom ajustado
center = [
  -7.79476, 
  -72.18981
]
# Zoom retornado para 11 conforme solicitado
zoom_start = 11

# Add custom base maps to folium
basemaps = {
    'Google Maps': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Maps',
        overlay = True,
        control = True
    ),
    'Google Satellite': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite',
        overlay = True,
        control = True
    ),
    'Google Terrain': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Terrain',
        overlay = True,
        control = True
    ),
    'Google Satellite Hybrid': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite',
        overlay = True,
        control = True
    ),
    'Esri Satellite': folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = True,
        control = True
    )
}

map_type = basemaps["Esri Satellite"]

m = folium.Map(
  location = center,
  zoom_start = zoom_start,
  tiles = map_type
)

tib = folium.FeatureGroup(name = "Limites da área de amortecimento")
buffer = folium.GeoJson(
  data = ti_buffer.to_json(),
  style_function = lambda x: {
    "fillColor": "#ffb38a",
    "color": "#444444",
    "weight": 2
  },
  highlight_function = lambda feat: { "color": "white"},
).add_to(tib)

til = folium.FeatureGroup(name = "Limites da Terra Indígena")
ti = folium.GeoJson(
  data = ti.to_json(),
  style_function = lambda x: {
    "fillColor": "#cbd5c0",
    "color": "#444444",
    "weight": 2
  },
  highlight_function = lambda feat: { "color": "white"},
).add_to(til)

# ti_buffer_fire = ti_buffer_fire.to_json()
# ti_buffer_fire = folium.features.GeoJson(ti_buffer_fire)

tooltip_b=folium.GeoJsonTooltip(
    fields=["date"],
    aliases=["Data:"],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
        font-size: 50px;
    """,
    max_width=800,
)

tooltip_ti=folium.GeoJsonTooltip(
    fields=["date"],
    aliases=["Data:"],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=800,
)

tibp=folium.FeatureGroup(name = "Alertas de desmatamento na área de amortecimento")
buffer_r = folium.GeoJson(
    data=buffer_radd_data.__geo_interface__,
    style_function=lambda x: {
        "fillColor": "#ff6666",
        "color": "#ff6666",
        "fillOpacity": 1,  # Corrigindo "fillopacity" para "fillOpacity"
    },
    tooltip=tooltip_b,
).add_to(tibp)

tilp=folium.FeatureGroup(name = "Alertas de desmatamento na Terra Indígena")
ti_r = folium.GeoJson(
    data=ti_radd_data.__geo_interface__,
    style_function=lambda x: {
        "fillColor": "red",
        "color": "red",
        "fillOpacity": 1,  # Corrigindo "fillopacity" para "fillOpacity"
    },
    tooltip=tooltip_ti,
).add_to(tilp)

# Add a layer control panel to the map
m.add_child(tib)
m.add_child(til)

if (ti_radd_data["date"].count() >= 1):
  m.add_child(tilp)
  
if (buffer_radd_data["date"].count() >= 1):
  m.add_child(tibp)
  
m.get_root().add_child(macro)

m.add_child(folium.LayerControl()) 

#fullscreen
plugins.Fullscreen().add_to(m)

#GPS
plugins.LocateControl().add_to(m)

#mouse position
fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
plugins.MousePosition(
  position='topright', 
  separator=' | ', 
  prefix="Mouse:",
  lat_formatter=fmtr, 
  lng_formatter=fmtr
).add_to(m)

#Add measure tool 
plugins.MeasureControl(
  position='topright', 
  primary_length_unit='meters', 
  secondary_length_unit='miles', 
  primary_area_unit='sqmeters', 
  secondary_area_unit='acres'
).add_to(m)
 

## Layout Otimizado - Cards e Mapa de Desmatamento

# Layout responsivo com distribuição perfeita
st.markdown("""
<div class="main-container">
    <div class="content-wrapper">
        <!-- Cards Section -->
        <div class="metrics-section">
            <div class="metrics-grid">
                <div class="metric-card deforestation">
                    <div class="metric-icon">🪵</div>
                    <div class="metric-content">
                        <div class="metric-title">Alertas de desmatamento na TI</div>
                        <div class="metric-value">""" + str(ti_radd_n) + """ ha</div>
                        <div class="metric-description">Terra Indígena Campinas/Katukina</div>
                    </div>
                </div>
                <div class="metric-card deforestation">
                    <div class="metric-icon">🛡️</div>
                    <div class="metric-content">
                        <div class="metric-title">Alertas na área de amortecimento</div>
                        <div class="metric-value">""" + str(buffer_radd_n) + """ ha</div>
                        <div class="metric-description">Zona de proteção (buffer 10km)</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# CSS otimizado para layout perfeito de desmatamento
st.markdown("""
<style>
/* Container principal simplificado */
.main-container {
    width: 100%;
    margin: 0;
    padding: 0;
}

.content-wrapper {
    width: 100%;
    padding: 5px;
}

/* Seção de métricas otimizada */
.metrics-section {
    margin-bottom: 5px;
}

.metrics-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 10px;
    width: 100%;
    margin: 0;
}

.metric-card.deforestation {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    color: white;
    border-radius: 12px;
    padding: 12px;
    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.2);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    gap: 12px;
    min-height: 70px;
}

.metric-card.deforestation::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(255,255,255,0.1), transparent);
    pointer-events: none;
}

.metric-card.deforestation:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(255, 107, 107, 0.4);
}

.metric-icon {
    font-size: 32px;
    flex-shrink: 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.metric-content {
    flex: 1;
}

.metric-title {
    font-size: 13px;
    opacity: 0.9;
    margin-bottom: 5px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    line-height: 1.2;
}

.metric-value {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 5px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    color: #ffffff;
}

.metric-description {
    font-size: 11px;
    opacity: 0.8;
    font-style: italic;
    line-height: 1.3;
}

/* Tablet e Desktop */
@media (min-width: 768px) {
    .content-wrapper {
        padding: 10px;
    }
    
    .metrics-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
    }
    
    .metric-card.deforestation {
        padding: 15px;
        min-height: 85px;
    }
    
    .metric-icon {
        font-size: 34px;
    }
    
    .metric-title {
        font-size: 14px;
    }
    
    .metric-value {
        font-size: 26px;
    }
    
    .metric-description {
        font-size: 12px;
    }
}

/* Desktop grande */
@media (min-width: 1200px) {
    .content-wrapper {
        max-width: 1200px;
        margin: 0 auto;
        padding: 15px;
    }
    
    .metrics-grid {
        gap: 18px;
    }
    
    .metric-card.deforestation {
        padding: 18px;
        min-height: 95px;
    }
    
    .metric-icon {
        font-size: 36px;
    }
    
    .metric-value {
        font-size: 28px;
    }
}

/* Mobile - ajustes específicos */
@media (max-width: 767px) {
    .content-wrapper {
        padding: 8px;
    }
    
    .metrics-section {
        margin-bottom: 5px;
    }
    
    .metric-card.deforestation {
        min-height: 65px;
        padding: 10px;
    }
    
    .metric-icon {
        font-size: 26px;
    }
    
    .metric-value {
        font-size: 20px;
    }
}
</style>
""", unsafe_allow_html=True)

st.divider()

if time:
  
  # CSS otimizado para o mapa de desmatamento
  st.markdown("""
  <style>
  .map-container {
      width: 100%;
      margin: 0;
      padding: 0;
  }
  
  .map-section {
      margin-bottom: 15px;
  }
  
  .map-title {
      font-size: 20px;
      font-weight: 600;
      color: #333;
      margin: 0 0 15px 0;
      text-align: center;
      padding: 10px;
      background: linear-gradient(135deg, #fff0f0 0%, #ffe6e6 100%);
      border-radius: 10px;
      border-left: 4px solid #ff6b6b;
  }
  
  /* Otimização do iframe do mapa */
  .stIframe {
      width: 100% !important;
      margin: 0 !important;
      padding: 0 !important;
      border-radius: 12px !important;
      overflow: hidden !important;
      box-shadow: 0 8px 32px rgba(255, 107, 107, 0.15) !important;
  }
  
  .stIframe iframe {
      border-radius: 12px !important;
      box-shadow: none !important;
      border: none !important;
  }
  
  /* Altura fixa e responsiva do mapa */
  .stIframe {
      height: 600px !important; /* Desktop padrão */
  }
  
  /* Mobile - altura otimizada */
  @media (max-width: 767px) {
      .map-title {
          font-size: 18px;
          padding: 8px;
      }
      
      .stIframe {
          height: 450px !important; /* Mobile */
          margin: 0 !important;
      }
  }
  
  /* Tablet - altura intermediária */
  @media (min-width: 768px) and (max-width: 1024px) {
      .stIframe {
          height: 550px !important; /* Tablet */
      }
  }
  
  /* Desktop - altura otimizada */
  @media (min-width: 1025px) {
      .stIframe {
          height: 650px !important; /* Desktop */
      }
  }
  </style>
  """, unsafe_allow_html=True)
  
  # Renderizar mapa com configurações otimizadas
  map_data = st_folium(
    m,
    width="100%",
    height=600,  # Valor base, será sobrescrito pelo CSS
    key="optimized_deforestation_map"
  )

# Navegação inferior para mobile
st.markdown("""
<div class="bottom-nav">
    <a href="../" class="nav-item">
        <div class="nav-icon">🔥</div>
        <div class="nav-label">Focos</div>
    </a>
    <a href="#" class="nav-item active">
        <div class="nav-icon">🪵</div>
        <div class="nav-label">Desmate</div>
    </a>
    <a href="3_ℹ️_Informações_do_Projeto" class="nav-item">
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
    color: #ee5a24;
    background: #fff5f5;
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

