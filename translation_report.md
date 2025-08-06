# 🌎 Relatório de Extração de Textos para Tradução

## Aplicação: Nokekoi - Sistema de Monitoramento TI Campinas/Katukina

### 📊 Resumo da Extração

- **Total de textos extraídos**: 20
- **Page Titles**: 3 textos
- **Headers**: 3 textos
- **Interface Texts**: 6 textos
- **Descriptions**: 3 textos
- **Labels**: 1 textos
- **Messages**: 4 textos

### 📝 Textos por Categoria

#### 🏷️ Títulos das Páginas

1. "Focos de calor na TI Campinas/Katukina"
2. "Informações sobre o projeto"
3. "Alertas de desmatamento na TI Campinas/Katukina"

#### 📋 Cabeçalhos e Títulos

1. "Descrição da Aplicação e dos Dados Disponibilizados"
2. "Alertas de desmatameto"
3. "Focos de de calor"

#### 🏷️ Rótulos de Controles

1. "Selecione o período de análise:"

#### 💬 Textos de Interface

1. "1 ano"
2. "15 dias"
3. "1 mês"
4. "2 meses"
5. "6 meses"
6. "3 meses"

#### 📢 Mensagens e Alertas

1. "**Focos de calor na área de amortecimento:**"
2. "**Alertas de desmatametno na área de amortecimento:**"
3. "**Focos de calor na TI:**"
4. "**Alertas de desmatamento na TI:**"

#### 📖 Descrições Longas

1. "header {visibility: hidden;} div[class^='block-container'] { padding-top: 8rem; } """, unsafe_allow_html=True) # @st.cache_data # def get_base64_of_bin_file(png_file): # with open(png_file, "rb") as f: # data = f.read() # return base64.b64encode(data).decode() # def build_markup_for_logo( # png_file, # background_position="50% 0%", # margin_top="10%", # image_width="", # image_height="70%", # ): # binary_string = get_base64_of_bin_file(png_file) # return """ # # [data-testid="stSidebarNav"] { # background-image: url("data:image/png;base64,%s"); # background-repeat: no-repeat; # background-position: %s; # margin-top: %s; # background-size: %s %s; # } # # """ % ( # binary_string, # background_position, # margin_top, # image_width, # image_height, # ) # def add_logo(png_file): # logo_markup = build_markup_for_logo(png_file) # st.markdown( # logo_markup, # unsafe_allow_html=True, # ) # add_logo('./img/Ufac_logo.png') ## Add logo to sidebar def add_logo(): st.html(""" [alt=Logo] { height: 70%; margin-top: 10%; margin-bottom: 0%; margin-left: 5%; margin-right: 5%; }"
2. "header {visibility: hidden;} div[class^='block-container'] { padding-top: 8rem; } """, unsafe_allow_html=True) st.markdown(""" """, unsafe_allow_html=True) # @st.cache_data # def get_base64_of_bin_file(png_file): # with open(png_file, "rb") as f: # data = f.read() # return base64.b64encode(data).decode() # def build_markup_for_logo( # png_file, # background_position="50% 0%", # margin_top="10%", # image_width="", # image_height="70%" # ): # binary_string = get_base64_of_bin_file(png_file) # return """ # # [data-testid="stSidebarNav"] { # background-image: url("data:image/png;base64,%s"); # background-repeat: no-repeat; # background-position: %s; # margin-top: %s; # background-size: %s %s; # } # # """ % ( # binary_string, # background_position, # margin_top, # image_width, # image_height, # ) # def add_logo(png_file): # logo_markup = build_markup_for_logo(png_file) # st.markdown( # logo_markup, # unsafe_allow_html=True, # ) # add_logo('./img/Ufac_logo.png') st.html(""" [alt=Logo] { height: 70%; margin-top: 10%; margin-bottom: 0%; margin-left: 5%; margin-right: 5%; }"
3. "header {visibility: hidden;} div[class^='block-container'] { padding-top: 8rem; } """, unsafe_allow_html=True) ## Get the current year current_year = datetime.datetime.now().year with st.sidebar: st.markdown( f'Copyright (c) {current_year} &nbsp LabGAMA', unsafe_allow_html=True, ) st.markdown("# Descrição da Aplicação e dos Dados Disponibilizados") st.markdown( """ Essa aplicação web foi desenvolvida com o propósito de produzir informações que permitam detectar de forma precoce a alteração da cobertura vegetal na Terra Indígena Campinas/Katukina, ajudando a comunidade indígena a proteger seu patrimônio natural. Essa atividade foi desenvolvida no âmbito do Projeto **Sistema de Monitoramento Precoce de Invasões da Terra Indígena Campinas/Katukina**, liderando por professores e estudantes da [Universidade Federal do Acre](https://www.ufac.br/) com apoio financeiro da [Transmissora Acre SPE S.A.](https://www.zenergiabr.com.br/subestacao/transmissora-acre), no âmbito do Plano Básico Ambiental do Componente Indígena – CI-PBA da Terra Indígena Campinas Katukina/AC, referente ao Licenciamento Ambiental da Linha de Transmissão (LT) 230 kV, no trecho Feijó-Cruzeiro do Sul. Para tanto utilizamos dados de focos de calor provenientes do **Sensor VIIRS**, [produto fogo ativo](https://www.earthdata.nasa.gov/learn/find-data/near-real-time/firms/viirs-i-band-375-m-active-fire-data), resolução espacial de 375 m e atualização diária. Além disso utilizamos dados de alertas de desmatamento do [RADD Forest Disturbance Alerts](https://data.globalforestwatch.org/datasets/gfw::deforestation-alerts-radd/about) que usa dados de radar da missão Sentinel-1 para mapear alterações da cobertura florestal com resolução espacial de 10 m e resolução de temporal 6 a 12 dias. Fonte dos dados: Focos de calor disponiblilizados pela **NASA** [Fire Information for Resource Management System](https://firms.modaps.eosdis.nasa.gov/active_fire/) (FIRMS). Alertas de desmatamento conforme, Reiche J, Mullissa A, Slagter B, Gou Y, Tsendbazar N, Odongo-Braun C, Vollrath A, Weisse M, Stolle F, Pickens A, Donchyts G, Clinton N, Gorelick N & Herold M, (2021), Forest disturbance alerts for the Congo Basin using Sentinel-1, Environmental Research Letters, [https://doi.org/10.1088/1748-9326/abd0a8](https://doi.org/10.1088/1748-9326/abd0a8). Desenvolvido por: [Laboratório de Geoprocessamento Aplicado ao Meio Ambiente](https://www.ufac.br/labgama), [UFAC Campus Floresta](https://www.ufac.br/floresta). Equipe: [Dr. A. Willian Flores de Melo](https://lattes.cnpq.br/9339997282776018), [Dra. Sonaira Silva](http://lattes.cnpq.br/7877159779121386), [Dr. Igor Oliveira](http://lattes.cnpq.br/2419895860496067) e [Henrique Melo](http://lattes.cnpq.br/4776096577200930)."

### 📁 Arquivos Gerados

1. `texts_extraction_complete.json` - Extração completa com detalhes por arquivo
2. `translation_template.json` - Template estruturado para tradução
3. `translation_report.md` - Este relatório

### 🎯 Próximos Passos

1. Revisar os textos extraídos
2. Preencher o campo `translation` no arquivo `translation_template.json`
3. Adicionar contexto quando necessário
4. Definir prioridades de tradução
5. Implementar as traduções na aplicação
