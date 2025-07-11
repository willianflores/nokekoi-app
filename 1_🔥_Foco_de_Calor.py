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

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

## Page configuration
st.set_page_config(
  page_title = "Focos de calor na TI Campinas/Katukina", 
  page_icon = "./img/labgama-favicon.png",
  layout = "wide",  
)

st.markdown("""
    <style>
        header {visibility: hidden;}
        div[class^='block-container'] { padding-top: 8rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<head>
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
  
  def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url('./img/Ufac_logo.png');
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "My Company Name";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    add_logo()
  
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

# Fire map
center = [
  -7.79476, 
  -72.18981
]
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
 

## Dashboard
# st.divider()
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.write('**Focos de calor na TI:**')
    st.info(f"{ti_fire_n} focos")

with row1_col2:
    st.write('**Focos de calor na área de amortecimento:**')
    st.info(f"{buffer_fire_n} focos")

st.divider()

if time:
  st_folium(
    m,
    width = "100%",
  )

