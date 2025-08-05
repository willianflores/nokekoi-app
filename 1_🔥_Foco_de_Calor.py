import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from folium.plugins import FastMarkerCluster
from streamlit_folium import folium_static
from folium import plugins
import base64
import glob
from datetime import date, timedelta
from streamlit_extras.app_logo import add_logo
from branca.element import Template, MacroElement
import locale
from mobile_responsive_improvements import apply_mobile_first_improvements

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

## Page configuration
st.set_page_config(
  page_title = "Focos de calor na TI Campinas/Katukina", 
  page_icon = "./img/labgama-favicon.png",
  layout = "wide",
  initial_sidebar_state = "collapsed"
)

# Aplicar melhorias Mobile-First
apply_mobile_first_improvements()

# Meta tags para SEO e responsividade
st.markdown("""
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="theme-color" content="#0066cc">
    <meta property="og:title" content="Focos de Calor - TI Campinas/Katukina">
    <meta property="og:description" content="Monitoramento de focos de calor na Terra Indígena Campinas/Katukina e sua área de amortecimento.">
    <meta property="og:image" content="./img/labgama-favicon.png">
    <meta property="og:url" content="https://nokekoi.ufac.br">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Focos de Calor - TI Campinas/Katukina">
    <meta name="twitter:description" content="Monitoramento de focos de calor na Terra Indígena Campinas/Katukina e sua área de amortecimento.">
    <meta name="twitter:image" content="./img/labgama-favicon.png">
</head>
""", unsafe_allow_html=True)


# @st.cache_data
# def get_base64_of_bin_file(png_file):
#     with open(png_file, "rb") as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# def build_markup_for_logo(
#     png_file,
#     background_position="50% 0%",
#     margin_top="10%",
#     image_width="",
#     image_height="70%"
#   ):
#     binary_string = get_base64_of_bin_file(png_file)
#     return """
#             <style>
#                 [data-testid="stSidebarNav"] {
#                     background-image: url("data:image/png;base64,%s");
#                     background-repeat: no-repeat;
#                     background-position: %s;
#                     margin-top: %s;
#                     background-size: %s %s;
#                 }
#             </style>
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

# Header mobile com menu
st.markdown("""
<div class="mobile-header">
    <div class="app-title">
        <img src="./img/labgama-favicon.png" alt="Logo" class="header-logo">
        <span>Nokekoi - Focos de Calor</span>
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
 
  st.sidebar.header("Focos de de calor")
    
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
  
## Dataset'
@st.cache_data(ttl=600, hash_funcs={gpd.GeoDataFrame: lambda _: None})
def getFireData(data_type, time):
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
  
  if time not in time_map or data_type not in ["ti", "ti_buffer"]:
      raise ValueError("Parâmetros inválidos.")
  
  file_path = f"./datasets/suomi-npp-viirs-c2/parquet/{data_type}_fire_{time_map[time]}.geoparquet"
  return gpd.read_parquet(file_path)



@st.cache_data(ttl=600, hash_funcs={gpd.GeoDataFrame: lambda _: None})
def import_shp(parquet_path):
    
    return gpd.read_parquet(parquet_path)

ti = import_shp("./datasets/shp/TI_Campinas_Katukina.parquet")
ti_buffer = import_shp("./datasets/shp/TI_Campinas_Katukina_Buffer10km.parquet")

# df_fire.memory_usage(deep=True)
# df_fire.info()
# df_fire["confidence"].value_counts()

ti_fire = getFireData("ti", time=time)

# ti_fire.info()

ti_buffer_fire = getFireData("ti_buffer", time=time)

ti_fire_n = round(len(ti_fire),0)
ti_fire_n = locale.format_string("%d", ti_fire_n, True)
buffer_fire_n = round(len(ti_buffer_fire),0)
buffer_fire_n = locale.format_string("%d", buffer_fire_n, True)

## Legend
template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
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
      <li><span style='background:red;opacity:1;'></span>Focos de calor na TI</li>
      <li><span style='background:#ff6666;opacity:1;'></span>Focos de calor na Área de Amortecimento</li>

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

# Fire map - Configuração com zoom ajustado
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
# Criar FeatureGroup para os focos de calor
tibp = folium.FeatureGroup(name="Focos de calor na área de amortecimento")
tilp = folium.FeatureGroup(name="Focos de calor na Terra Indígena")

# Adicionar todos os pontos da TI ao FeatureGroup
for _, row in ti_fire.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=4,
        color="red",
        fill=True,
        fill_opacity=0.8,
        opacity=1,
        tooltip=f"Data: {row['acq_date']}",  # Tooltip diretamente no marcador
        stroke=False
    ).add_to(tilp)

# Adicionar todos os pontos da área de amortecimento ao FeatureGroup
for _, row in ti_buffer_fire.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=4,
        color="#ff6666",
        fill=True,
        fill_opacity=0.8,
        opacity=1,
        tooltip=f"Data: {row['acq_date']}",  # Tooltip diretamente no marcador
        stroke=False
    ).add_to(tibp)

# Add a layer control panel to the map
m.add_child(tib)
m.add_child(til)
m.add_child(tilp)
m.add_child(tibp)
m.add_child(folium.LayerControl())
m.get_root().add_child(macro)

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
 

## Dashboard Mobile-First

# Cards de métricas responsivos
metrics_html = f"""
<div class="metrics-container">
    <div class="metric-card">
        <div class="metric-title">Focos de calor na TI</div>
        <div class="metric-value">{ti_fire_n} focos</div>
        <div class="metric-description">Terra Indígena Campinas/Katukina</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">Focos na área de amortecimento</div>
        <div class="metric-value">{buffer_fire_n} focos</div>
        <div class="metric-description">Zona de proteção (buffer 10km)</div>
    </div>
</div>
"""

st.markdown(metrics_html, unsafe_allow_html=True)

# CSS separado para evitar problemas de parsing
st.markdown("""
<style>
.metrics-container {
    display: grid;
    grid-template-columns: 1fr;
    gap: 16px;
    margin: 20px 0;
}

.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(255,255,255,0.1), transparent);
    pointer-events: none;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 35px rgba(0,0,0,0.15);
}

.metric-title {
    font-size: 14px;
    opacity: 0.9;
    margin-bottom: 8px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-value {
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 8px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.metric-description {
    font-size: 12px;
    opacity: 0.8;
    font-style: italic;
}

@media (min-width: 768px) {
    .metrics-container {
        grid-template-columns: repeat(2, 1fr);
        gap: 24px;
    }
    
    .metric-card {
        padding: 24px;
    }
    
    .metric-value {
        font-size: 32px;
    }
}

@media (min-width: 1024px) {
    .metrics-container {
        grid-template-columns: repeat(2, 1fr);
        max-width: 800px;
        margin: 20px auto;
    }
}
</style>
""", unsafe_allow_html=True)

st.divider()

if time:
  # Detectar tamanho da tela para altura responsiva
  st.markdown("""
  <script>
  // Detectar largura da tela e definir altura do mapa
  window.mapHeight = window.innerWidth > 768 ? 600 : 400;
  </script>
  """, unsafe_allow_html=True)
  
  # Calcular altura responsiva baseada na largura da viewport  
  import streamlit.components.v1 as components
  
  # Configuração responsiva de altura do mapa
  map_height_desktop = 700  # Altura aumentada para desktop
  map_height_mobile = 450   # Altura aumentada para mobile
  
  # Usar altura maior por padrão (assumindo desktop) com CSS responsivo
  map_height = map_height_desktop
  
  # Mapa otimizado para diferentes tamanhos de tela
  st.markdown("""
  <style>
  .stIframe iframe {
      border-radius: 12px !important;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
  }
  
  /* Altura responsiva do mapa */
  .stIframe {
      height: 700px !important; /* Desktop - aumentado */
  }
  
  @media (max-width: 767px) {
      .stIframe {
          height: 450px !important; /* Mobile - aumentado */
          margin: 10px 0 !important;
      }
  }
  
  @media (min-width: 768px) and (max-width: 1024px) {
      .stIframe {
          height: 550px !important; /* Tablet - aumentado */
      }
  }
  </style>
  """, unsafe_allow_html=True)
  
  # Renderizar mapa com configurações responsivas
  map_data = st_folium(
    m,
    width="100%",
    height=map_height,  # Altura responsiva otimizada
    key="mobile_fire_map"
  )

# Navegação inferior para mobile
st.markdown("""
<div class="bottom-nav">
    <a href="#" class="nav-item active">
        <div class="nav-icon">🔥</div>
        <div class="nav-label">Focos</div>
    </a>
    <a href="pages/2_🪵_Alerta_de_Desmatamento" class="nav-item">
        <div class="nav-icon">🪵</div>
        <div class="nav-label">Desmate</div>
    </a>
    <a href="pages/3_ℹ️_Informações_do_Projeto" class="nav-item">
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

