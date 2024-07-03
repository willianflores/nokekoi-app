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

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

## Page configuration
st.set_page_config(
  page_title = "Alertas de desmatamento na TI Campinas/Katukina", 
  page_icon = "./img/labgama-favicon.png",
  layout = "wide",  
)

st.markdown(" <style> div[class^='block-container'] { padding-top: 8rem; } </style> ", unsafe_allow_html=True)

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

## Sidebar
with st.sidebar:
  #st.image(logo, width=300)
  st.sidebar.header("Alertas de desmatameto")
    
  time = st.selectbox(
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

## Dataset
if time == "15 dias":
  time_filter = 15
elif time == "1 mês":
  time_filter = 30  
elif time == "2 meses":
  time_filter = 60
elif time == "3 meses":
  time_filter = 90
elif time == "6 meses":
  time_filter = 180
elif time == "1 ano":
  time_filter = 365

start_date = date.today() - timedelta(days = time_filter)

#logo = Image.open("./img/logo_300.png")

@st.cache_data
def getShpData(shp_path):
  shp = gpd.read_file(shp_path)
  
  return shp

ti = getShpData("./datasets/shp/TI_Campinas_Katukina.shp")
ti_buffer = getShpData("./datasets/shp/TI_Campinas_Katukina_Buffer10km.shp")

# df_fire.memory_usage(deep=True)
# df_fire.info()
# df_fire["confidence"].value_counts()

@st.cache_data
def getGeoParquetData(parquet_path):
  geoparquet = gpd.read_parquet(parquet_path)
  
  return geoparquet

ti_parquet_path = "./datasets/radd/geoparquet/radd_ti_data.geoparquet"
ti_radd_data = getGeoParquetData(ti_parquet_path)


ti_radd_data = ti_radd_data.loc[ti_radd_data["date"]>= pd.to_datetime(start_date)]
ti_radd_data["date"] = ti_radd_data["date"].dt.strftime('%d/%m/%Y')

# ti_fire.info()

buffer_parquet_path = "./datasets/radd/geoparquet/radd_buffer_data.geoparquet"
buffer_radd_data = getGeoParquetData(buffer_parquet_path)

buffer_radd_data = buffer_radd_data.loc[buffer_radd_data["date"]>= pd.to_datetime(start_date)]
buffer_radd_data["date"] = buffer_radd_data["date"].dt.strftime("%d/%m/%Y")

porj_area = "+proj=aea +lat_1=10 +lat_2=-40 +lat_0=-25 +lon_0=-50 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs "

ti_radd_data_proj = ti_radd_data.to_crs(porj_area)
ti_radd_data_proj['area_ha'] = ti_radd_data_proj['geometry'].area/10000

buffer_radd_data_proj = buffer_radd_data.to_crs(porj_area)
buffer_radd_data_proj['area_ha'] = buffer_radd_data_proj['geometry'].area/10000

ti_radd_n = round(ti_radd_data_proj["area_ha"].sum())
ti_radd_n = locale.format_string("%d", ti_radd_n, True)
buffer_radd_n = round(buffer_radd_data_proj["area_ha"].sum())
buffer_radd_n = locale.format_string("%d", buffer_radd_n, True)

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
buffer_r=folium.GeoJson(
  data = buffer_radd_data.to_json(),
  style_function=lambda x: {
    "fillColor": "#ff6666",
    "color": "#ff6666",
    "fillopacity": 1,
  },
  tooltip=tooltip_b,
).add_to(tibp)

tilp=folium.FeatureGroup(name = "Alertas de desmatamento na Terra Indígena")
ti_r=folium.GeoJson(
  data=ti_radd_data.to_json(),
  style_function=lambda x: {
    "fillColor": "red",
    "color": "red",
    "fillopacity": 1,
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
 

## Dashboard

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.write('**Alertas de desmatamento na TI:**')
    st.info(f"{ti_radd_n} ha")

with row1_col2:
    st.write('**Alertas de desmatametno na área de amortecimento:**')
    st.info(f"{buffer_radd_n} ha")

st.divider()

st_folium(
  m,
  width = "100%",
)

