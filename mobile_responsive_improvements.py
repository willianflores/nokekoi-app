# 📱 Melhorias de Responsividade Mobile para Nokekoi App
# Seguindo o princípio Mobile-First

import streamlit as st

def apply_mobile_first_css():
    """
    Aplica CSS responsivo seguindo o princípio Mobile-First
    """
    mobile_css = """
    <style>
    /* ===== MOBILE-FIRST CSS ===== */
    /* Base styles (mobile) */
    
    /* Container principal */
    .main .block-container {
        padding-top: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    
    /* Sidebar responsiva */
    .css-1d391kg {
        width: 100% !important;
        min-width: 100% !important;
    }
    
    /* Headers mais compactos no mobile */
    h1 {
        font-size: 1.5rem !important;
        line-height: 1.3 !important;
        margin-bottom: 1rem !important;
    }
    
    h2 {
        font-size: 1.3rem !important;
        line-height: 1.3 !important;
        margin-bottom: 0.8rem !important;
    }
    
    h3 {
        font-size: 1.1rem !important;
        line-height: 1.3 !important;
        margin-bottom: 0.6rem !important;
    }
    
    /* Cards de métricas mais compactos */
    .metric-card {
        padding: 0.8rem !important;
        margin-bottom: 0.8rem !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    /* Controles de filtro empilhados */
    .stRadio > div {
        flex-direction: column !important;
        gap: 0.5rem !important;
    }
    
    .stRadio > div > label {
        font-size: 0.9rem !important;
        padding: 0.5rem !important;
        margin-bottom: 0.2rem !important;
    }
    
    /* Mapas responsivos */
    .folium-map {
        width: 100% !important;
        height: 60vh !important;
        min-height: 400px !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    /* Legenda do mapa adaptada para mobile */
    .maplegend {
        position: fixed !important;
        bottom: 10px !important;
        left: 10px !important;
        right: 10px !important;
        max-width: none !important;
        font-size: 12px !important;
        padding: 8px !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        z-index: 1000 !important;
    }
    
    .maplegend ul.legend-labels li {
        font-size: 11px !important;
        line-height: 16px !important;
        margin-bottom: 3px !important;
    }
    
    .maplegend ul.legend-labels li span {
        width: 20px !important;
        height: 12px !important;
        margin-right: 8px !important;
    }
    
    /* Controles do mapa otimizados para touch */
    .leaflet-control-container .leaflet-top .leaflet-control {
        margin-top: 60px !important;
        margin-right: 10px !important;
    }
    
    .leaflet-control-zoom a {
        width: 40px !important;
        height: 40px !important;
        line-height: 40px !important;
        font-size: 18px !important;
    }
    
    /* Colunas responsivas */
    .row-widget.stHorizontal {
        flex-direction: column !important;
        gap: 1rem !important;
    }
    
    /* Imagens responsivas */
    img {
        max-width: 100% !important;
        height: auto !important;
    }
    
    /* Logo adaptado para mobile */
    [alt=Logo] {
        height: 40px !important;
        margin: 10px auto !important;
        display: block !important;
    }
    
    /* Botões touch-friendly */
    .stButton > button {
        width: 100% !important;
        min-height: 44px !important;
        font-size: 16px !important;
        padding: 12px 16px !important;
        border-radius: 8px !important;
        margin-bottom: 8px !important;
    }
    
    /* Select boxes mais touch-friendly */
    .stSelectbox > div > div {
        min-height: 44px !important;
    }
    
    /* Texto mais legível */
    .stMarkdown {
        font-size: 14px !important;
        line-height: 1.5 !important;
    }
    
    /* ===== TABLET (768px+) ===== */
    @media (min-width: 768px) {
        .main .block-container {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            max-width: 1200px !important;
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        h2 {
            font-size: 1.6rem !important;
        }
        
        .folium-map {
            height: 70vh !important;
            min-height: 500px !important;
        }
        
        .maplegend {
            position: absolute !important;
            bottom: 20px !important;
            right: 20px !important;
            left: auto !important;
            max-width: 300px !important;
            font-size: 13px !important;
        }
        
        .row-widget.stHorizontal {
            flex-direction: row !important;
        }
        
        .stButton > button {
            width: auto !important;
            min-width: 120px !important;
        }
    }
    
    /* ===== DESKTOP (1024px+) ===== */
    @media (min-width: 1024px) {
        .main .block-container {
            padding-top: 3rem !important;
            padding-left: 3rem !important;
            padding-right: 3rem !important;
        }
        
        h1 {
            font-size: 2.5rem !important;
        }
        
        h2 {
            font-size: 2rem !important;
        }
        
        .folium-map {
            height: 80vh !important;
            min-height: 600px !important;
        }
        
        .maplegend {
            font-size: 14px !important;
            padding: 10px !important;
        }
        
        .leaflet-control-zoom a {
            width: 30px !important;
            height: 30px !important;
            line-height: 30px !important;
            font-size: 14px !important;
        }
        
        .stMarkdown {
            font-size: 16px !important;
        }
    }
    
    /* ===== ACESSIBILIDADE E UX ===== */
    
    /* Focus visível para navegação por teclado */
    *:focus {
        outline: 2px solid #0066cc !important;
        outline-offset: 2px !important;
    }
    
    /* Melhor contraste para texto */
    .stMarkdown, .stText {
        color: #2c3e50 !important;
    }
    
    /* Loading states mais visíveis */
    .stSpinner {
        border-width: 3px !important;
        width: 40px !important;
        height: 40px !important;
    }
    
    /* Tooltips touch-friendly */
    .tooltip {
        pointer-events: auto !important;
        font-size: 14px !important;
        padding: 8px 12px !important;
        max-width: 200px !important;
        word-wrap: break-word !important;
    }
    
    /* Sidebar collapsible no mobile */
    @media (max-width: 767px) {
        .css-1d391kg {
            transform: translateX(-100%) !important;
            transition: transform 0.3s ease !important;
        }
        
        .css-1d391kg.expanded {
            transform: translateX(0) !important;
        }
        
        /* Botão para expandir sidebar */
        .sidebar-toggle {
            position: fixed !important;
            top: 10px !important;
            left: 10px !important;
            z-index: 1001 !important;
            background: #ffffff !important;
            border: 1px solid #ddd !important;
            border-radius: 4px !important;
            padding: 8px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }
    }
    
    /* Otimizações para PWA */
    @media (display-mode: standalone) {
        .main .block-container {
            padding-top: calc(env(safe-area-inset-top) + 1rem) !important;
            padding-bottom: calc(env(safe-area-inset-bottom) + 1rem) !important;
        }
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background-color: #1e1e1e !important;
            color: #ffffff !important;
        }
        
        .maplegend {
            background-color: rgba(30, 30, 30, 0.9) !important;
            color: #ffffff !important;
            border-color: #555 !important;
        }
        
        .stButton > button {
            background-color: #333 !important;
            color: #fff !important;
            border-color: #555 !important;
        }
    }
    
    /* Prevenção de zoom inadvertido */
    input, textarea, select {
        font-size: 16px !important;
    }
    
    /* Scrollbar customizada para melhor UX */
    ::-webkit-scrollbar {
        width: 8px !important;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1 !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1 !important;
        border-radius: 4px !important;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8 !important;
    }
    
    </style>
    """
    
    st.markdown(mobile_css, unsafe_allow_html=True)

def configure_mobile_viewport():
    """
    Configura viewport para dispositivos móveis
    """
    viewport_meta = """
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="theme-color" content="#0066cc">
    """
    st.markdown(viewport_meta, unsafe_allow_html=True)

def create_mobile_optimized_columns(num_cols=2, gap="medium"):
    """
    Cria colunas otimizadas para mobile que se empilham automaticamente
    """
    if st.session_state.get('mobile_view', False):
        # No mobile, usar uma coluna só
        return [st.container() for _ in range(num_cols)]
    else:
        # Em telas maiores, usar colunas normais
        return st.columns(num_cols, gap=gap)

def mobile_friendly_map_config():
    """
    Configurações de mapa otimizadas para mobile
    """
    return {
        'width': '100%',
        'height': 400,  # Altura fixa menor para mobile
        'key': 'mobile_map'
    }

def detect_mobile_device():
    """
    Detecta se o usuário está em um dispositivo móvel
    """
    # JavaScript para detectar dispositivo móvel
    mobile_detection_js = """
    <script>
    function isMobileDevice() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }
    
    if (isMobileDevice()) {
        document.body.classList.add('mobile-device');
        parent.postMessage({type: 'mobile_detected'}, '*');
    }
    </script>
    """
    st.markdown(mobile_detection_js, unsafe_allow_html=True)

# Função principal para aplicar todas as melhorias mobile
def apply_mobile_first_improvements():
    """
    Aplica todas as melhorias de responsividade mobile
    """
    configure_mobile_viewport()
    apply_mobile_first_css()
    detect_mobile_device()

if __name__ == "__main__":
    # Exemplo de uso
    st.set_page_config(
        page_title="Nokekoi Mobile-First",
        page_icon="📱",
        layout="wide",
        initial_sidebar_state="collapsed"  # Sidebar colapsada por padrão no mobile
    )
    
    apply_mobile_first_improvements()
    
    st.title("📱 Nokekoi App - Mobile Optimized")
    st.write("Esta versão foi otimizada seguindo o princípio Mobile-First")