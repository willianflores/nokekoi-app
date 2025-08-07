#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extrair textos atualizados da aplicação Nokekoi
para tradução em língua indígena
"""

import json
import re
from datetime import datetime

def extract_texts_from_file(file_path):
    """Extrai textos de um arquivo Python"""
    texts = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Padrões para extrair textos específicos
        patterns = [
            r'st\.sidebar\.header\("([^"]+)"\)',
            r'st\.radio\("([^"]+)"',
            r'st\.markdown\("""([^"]+)"""',
            r'st\.markdown\("([^"]+)"',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                # Limpar o texto
                text = match.strip()
                # Filtrar apenas textos reais (não CSS)
                if (text and len(text) > 3 and 
                    not text.startswith('<style>') and 
                    not text.startswith('/*') and
                    not text.startswith('@media') and
                    'background-color' not in text and
                    'color:' not in text and
                    'font-size' not in text):
                    texts.append(text)
                    
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
        
    return texts

def create_updated_translation_template():
    """Cria template de tradução atualizado"""
    
    # Textos manuais baseados nas últimas atualizações
    manual_texts = {
        "page_titles": [
            "Focos de calor na TI Campinas/Katukina",
            "Alertas de desmatamento na TI Campinas/Katukina", 
            "Informações sobre o projeto"
        ],
        "headers": [
            "Focos de de calor",
            "Alertas de desmatameto",
            "Descrição da Aplicação e dos Dados Disponibilizados",
            "Parceiros do Projeto"
        ],
        "labels": [
            "Selecione o período de análise:"
        ],
        "interface_texts": [
            "15 dias",
            "1 mês", 
            "2 meses",
            "3 meses",
            "6 meses",
            "1 ano"
        ],
        "metric_titles": [
            "Focos de calor na TI",
            "Focos na área de amortecimento",
            "Alertas de desmatamento na TI",
            "Alertas de desmatamento na área de amortecimento"
        ],
        "metric_descriptions": [
            "Terra Indígena Campinas/Katukina",
            "Zona de proteção (buffer 10km)"
        ],
        "descriptions": [
            "Essa aplicação web foi desenvolvida com o propósito de produzir informações que permitam detectar de forma precoce a alteração da cobertura vegetal na Terra Indígena Campinas/Katukina, ajudando a comunidade indígena a proteger seu patrimônio natural."
        ]
    }
    
    # Criar template atualizado
    template = {
        "metadata": {
            "source_language": "Português (Brasil)",
            "target_language": "Língua Indígena",
            "application": "Nokekoi - Sistema de Monitoramento TI Campinas/Katukina",
            "extraction_date": datetime.now().strftime("%a %d %b %Y %H:%M:%S %z"),
            "version": "2.0 - Atualizado com melhorias mobile"
        },
        "texts_to_translate": {
            "page_titles": {
                "description": "Títulos das Páginas",
                "texts": []
            },
            "headers": {
                "description": "Cabeçalhos e Títulos",
                "texts": []
            },
            "labels": {
                "description": "Rótulos de Controles",
                "texts": []
            },
            "interface_texts": {
                "description": "Textos de Interface",
                "texts": []
            },
            "metric_titles": {
                "description": "Títulos dos Cards de Métricas",
                "texts": []
            },
            "metric_descriptions": {
                "description": "Descrições dos Cards de Métricas",
                "texts": []
            },
            "descriptions": {
                "description": "Descrições Longas",
                "texts": []
            }
        }
    }
    
    # Adicionar textos organizados
    for i, text in enumerate(manual_texts["page_titles"]):
        template["texts_to_translate"]["page_titles"]["texts"].append({
            "id": f"page_titles_{i+1:03d}",
            "original_text": text,
            "translation": "",
            "context": "",
            "priority": "high"
        })
    
    for i, text in enumerate(manual_texts["headers"]):
        template["texts_to_translate"]["headers"]["texts"].append({
            "id": f"headers_{i+1:03d}",
            "original_text": text,
            "translation": "",
            "context": "",
            "priority": "high"
        })
    
    for i, text in enumerate(manual_texts["labels"]):
        template["texts_to_translate"]["labels"]["texts"].append({
            "id": f"labels_{i+1:03d}",
            "original_text": text,
            "translation": "",
            "context": "",
            "priority": "high"
        })
    
    for i, text in enumerate(manual_texts["interface_texts"]):
        template["texts_to_translate"]["interface_texts"]["texts"].append({
            "id": f"interface_texts_{i+1:03d}",
            "original_text": text,
            "translation": "",
            "context": "",
            "priority": "medium"
        })
    
    for i, text in enumerate(manual_texts["metric_titles"]):
        template["texts_to_translate"]["metric_titles"]["texts"].append({
            "id": f"metric_titles_{i+1:03d}",
            "original_text": text,
            "translation": "",
            "context": "",
            "priority": "high"
        })
    
    for i, text in enumerate(manual_texts["metric_descriptions"]):
        template["texts_to_translate"]["metric_descriptions"]["texts"].append({
            "id": f"metric_descriptions_{i+1:03d}",
            "original_text": text,
            "translation": "",
            "context": "",
            "priority": "medium"
        })
    
    for i, text in enumerate(manual_texts["descriptions"]):
        template["texts_to_translate"]["descriptions"]["texts"].append({
            "id": f"descriptions_{i+1:03d}",
            "original_text": text,
            "translation": "",
            "context": "",
            "priority": "low"
        })
    
    return template

def main():
    """Função principal"""
    print("🔍 Extraindo textos atualizados da aplicação Nokekoi...")
    
    # Criar template atualizado
    template = create_updated_translation_template()
    
    # Salvar arquivo JSON
    with open('translation_template_updated.json', 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)
    
    print("✅ Template de tradução atualizado salvo como 'translation_template_updated.json'")
    
    # Estatísticas
    total_texts = 0
    for category in template["texts_to_translate"].values():
        total_texts += len(category["texts"])
    
    print(f"📊 Total de textos extraídos: {total_texts}")
    
    return template

if __name__ == "__main__":
    main() 