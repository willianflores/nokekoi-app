# 📱 Componentes de Layout Mobile-First para Nokekoi App

import streamlit as st
import folium
from streamlit_folium import st_folium

def mobile_header_with_menu():
    """
    Cria um cabeçalho mobile com menu hambúrguer
    """
    header_html = """
    <div class="mobile-header">
        <button class="menu-toggle" onclick="toggleSidebar()">
            <span></span>
            <span></span>
            <span></span>
        </button>
        <div class="app-title">
            <img src="./img/labgama-favicon.png" alt="Logo" class="header-logo">
            <span>Nokekoi</span>
        </div>
    </div>
    
    <style>
    .mobile-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
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
    
    .menu-toggle {
        background: none;
        border: none;
        cursor: pointer;
        padding: 5px;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        width: 24px;
        height: 24px;
    }
    
    .menu-toggle span {
        width: 100%;
        height: 2px;
        background: #333;
        transition: 0.3s;
    }
    
    .menu-toggle.active span:nth-child(1) {
        transform: rotate(45deg) translate(5px, 5px);
    }
    
    .menu-toggle.active span:nth-child(2) {
        opacity: 0;
    }
    
    .menu-toggle.active span:nth-child(3) {
        transform: rotate(-45deg) translate(7px, -6px);
    }
    
    .app-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: bold;
        font-size: 18px;
        color: #333;
    }
    
    .header-logo {
        width: 32px;
        height: 32px;
        border-radius: 50%;
    }
    
    /* Ajustar conteúdo principal para compensar header fixo */
    .main .block-container {
        padding-top: 80px !important;
    }
    
    @media (min-width: 768px) {
        .mobile-header {
            display: none;
        }
        
        .main .block-container {
            padding-top: 2rem !important;
        }
    }
    </style>
    
    <script>
    function toggleSidebar() {
        const sidebar = document.querySelector('.css-1d391kg');
        const toggle = document.querySelector('.menu-toggle');
        
        if (sidebar) {
            sidebar.classList.toggle('expanded');
            toggle.classList.toggle('active');
        }
    }
    </script>
    """
    
    st.markdown(header_html, unsafe_allow_html=True)

def mobile_metrics_cards(metrics_data):
    """
    Cria cards de métricas otimizados para mobile
    
    Args:
        metrics_data: Lista de dicionários com 'title', 'value', 'delta' (opcional)
    """
    cards_html = """
    <div class="metrics-container">
    """
    
    for metric in metrics_data:
        delta_html = ""
        if metric.get('delta'):
            delta_class = "positive" if metric['delta'] > 0 else "negative" if metric['delta'] < 0 else "neutral"
            delta_html = f'<div class="metric-delta {delta_class}">{metric["delta"]:+}</div>'
        
        cards_html += f"""
        <div class="metric-card">
            <div class="metric-title">{metric['title']}</div>
            <div class="metric-value">{metric['value']}</div>
            {delta_html}
        </div>
        """
    
    cards_html += """
    </div>
    
    <style>
    .metrics-container {
        display: grid;
        grid-template-columns: 1fr;
        gap: 12px;
        margin: 16px 0;
    }
    
    .metric-card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .metric-title {
        font-size: 14px;
        color: #666;
        margin-bottom: 8px;
        font-weight: 500;
    }
    
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 4px;
    }
    
    .metric-delta {
        font-size: 12px;
        font-weight: 600;
        padding: 2px 6px;
        border-radius: 4px;
        display: inline-block;
    }
    
    .metric-delta.positive {
        color: #27ae60;
        background: #e8f5e8;
    }
    
    .metric-delta.negative {
        color: #e74c3c;
        background: #fdf2f2;
    }
    
    .metric-delta.neutral {
        color: #7f8c8d;
        background: #f8f9fa;
    }
    
    @media (min-width: 480px) {
        .metrics-container {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    @media (min-width: 768px) {
        .metrics-container {
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        }
    }
    </style>
    """
    
    st.markdown(cards_html, unsafe_allow_html=True)

def mobile_filter_panel(filters):
    """
    Cria painel de filtros colapsável para mobile
    
    Args:
        filters: Lista de dicionários com configurações de filtros
    """
    with st.expander("🔍 Filtros", expanded=False):
        for filter_config in filters:
            if filter_config['type'] == 'radio':
                filter_config['value'] = st.radio(
                    filter_config['label'],
                    filter_config['options'],
                    key=filter_config.get('key', filter_config['label'])
                )
            elif filter_config['type'] == 'selectbox':
                filter_config['value'] = st.selectbox(
                    filter_config['label'],
                    filter_config['options'],
                    key=filter_config.get('key', filter_config['label'])
                )
            elif filter_config['type'] == 'date_range':
                col1, col2 = st.columns(2)
                with col1:
                    filter_config['start_date'] = st.date_input(
                        "Data inicial",
                        key=f"{filter_config.get('key', filter_config['label'])}_start"
                    )
                with col2:
                    filter_config['end_date'] = st.date_input(
                        "Data final",
                        key=f"{filter_config.get('key', filter_config['label'])}_end"
                    )
    
    return filters

def mobile_optimized_folium_map(map_data, height=400):
    """
    Cria mapa Folium otimizado para mobile
    """
    # Configurações específicas para mobile
    mobile_map_config = {
        'width': '100%',
        'height': height,
        'key': 'mobile_optimized_map'
    }
    
    # Adicionar controles touch-friendly
    if hasattr(map_data, 'get_root'):
        # CSS para melhorar controles do mapa
        map_style = """
        <style>
        .folium-map {
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        }
        
        /* Controles maiores para touch */
        .leaflet-control-zoom a {
            width: 44px !important;
            height: 44px !important;
            line-height: 44px !important;
            font-size: 18px !important;
            border-radius: 8px !important;
            margin-bottom: 4px !important;
        }
        
        .leaflet-control-layers {
            border-radius: 8px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        }
        
        .leaflet-control-layers-toggle {
            width: 44px !important;
            height: 44px !important;
            border-radius: 8px !important;
        }
        
        /* Popup responsivo */
        .leaflet-popup-content-wrapper {
            border-radius: 8px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        }
        
        .leaflet-popup-content {
            font-size: 14px !important;
            line-height: 1.4 !important;
            max-width: 250px !important;
        }
        
        /* Tooltip responsivo */
        .leaflet-tooltip {
            font-size: 12px !important;
            padding: 6px 10px !important;
            border-radius: 6px !important;
            max-width: 200px !important;
            word-wrap: break-word !important;
        }
        
        @media (max-width: 480px) {
            .leaflet-control-zoom {
                margin-top: 10px !important;
                margin-right: 10px !important;
            }
            
            .leaflet-popup-content {
                max-width: 200px !important;
                font-size: 13px !important;
            }
        }
        </style>
        """
        st.markdown(map_style, unsafe_allow_html=True)
    
    return st_folium(map_data, **mobile_map_config)

# Função removida - barra de navegação mobile não é mais necessária

def mobile_loading_overlay():
    """
    Cria overlay de loading otimizado para mobile
    """
    loading_html = """
    <div id="mobile-loading" class="loading-overlay" style="display: none;">
        <div class="loading-content">
            <div class="loading-spinner"></div>
            <div class="loading-text">Carregando dados...</div>
        </div>
    </div>
    
    <style>
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.9);
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .loading-content {
        text-align: center;
        padding: 20px;
    }
    
    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #0066cc;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 12px;
    }
    
    .loading-text {
        font-size: 14px;
        color: #666;
        font-weight: 500;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    
    <script>
    function showMobileLoading() {
        document.getElementById('mobile-loading').style.display = 'flex';
    }
    
    function hideMobileLoading() {
        document.getElementById('mobile-loading').style.display = 'none';
    }
    
    // Auto-hide loading após 5 segundos
    setTimeout(hideMobileLoading, 5000);
    </script>
    """
    
    st.markdown(loading_html, unsafe_allow_html=True)

def mobile_toast_notifications():
    """
    Sistema de notificações toast para mobile
    """
    toast_html = """
    <div id="toast-container"></div>
    
    <style>
    #toast-container {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        max-width: 300px;
    }
    
    .toast {
        background: #333;
        color: white;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        animation: slideIn 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .toast.success {
        background: #27ae60;
    }
    
    .toast.error {
        background: #e74c3c;
    }
    
    .toast.warning {
        background: #f39c12;
    }
    
    .toast.info {
        background: #3498db;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    @media (max-width: 480px) {
        #toast-container {
            left: 10px;
            right: 10px;
            max-width: none;
        }
    }
    </style>
    
    <script>
    function showToast(message, type = 'info', duration = 3000) {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (container.contains(toast)) {
                    container.removeChild(toast);
                }
            }, 300);
        }, duration);
    }
    
    // Exemplos de uso:
    // showToast('Dados carregados com sucesso!', 'success');
    // showToast('Erro ao carregar dados', 'error');
    // showToast('Carregando...', 'info');
    </script>
    """
    
    st.markdown(toast_html, unsafe_allow_html=True)

# Exemplo de uso integrado
def create_mobile_first_page():
    """
    Exemplo de página completa usando componentes mobile-first
    """
    # Configurar página
    st.set_page_config(
        page_title="Nokekoi Mobile",
        page_icon="📱",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Aplicar melhorias mobile
    from mobile_responsive_improvements import apply_mobile_first_improvements
    apply_mobile_first_improvements()
    
    # Header mobile
    mobile_header_with_menu()
    
    # Métricas
    metrics_data = [
        {"title": "Focos de Calor TI", "value": "142", "delta": -5},
        {"title": "Focos Buffer", "value": "89", "delta": 12},
        {"title": "Alertas RADD", "value": "23", "delta": 0},
        {"title": "Área Total", "value": "15.2 ha", "delta": -2}
    ]
    mobile_metrics_cards(metrics_data)
    
    # Filtros
    filters = [
        {
            "type": "radio",
            "label": "Período de análise",
            "options": ["15 dias", "1 mês", "3 meses", "6 meses"],
            "key": "time_filter"
        }
    ]
    selected_filters = mobile_filter_panel(filters)
    
    # Mapa (exemplo)
    st.subheader("🗺️ Mapa Interativo")
    # Aqui seria integrado o mapa real
    st.info("Mapa Folium otimizado para mobile seria renderizado aqui")
    
    # Navegação inferior
    pages = [
        {"name": "Focos", "icon": "🔥", "url": "#", "active": True},
        {"name": "Desmate", "icon": "🪵", "url": "#"},
        {"name": "Info", "icon": "ℹ️", "url": "#"}
    ]
    mobile_bottom_navigation(pages)
    
    # Notificações e loading
    mobile_toast_notifications()
    mobile_loading_overlay()

if __name__ == "__main__":
    create_mobile_first_page()