#!/bin/bash

# Adiciona o caminho ao comando streamlit no PATH
export PATH=/home/srvadmin/.local/bin:$PATH

# Muda para o diretório do usuário
cd /home/srvadmin/nokekoiApp

# Executa o comando streamlit
streamlit run 1_🔥_Foco_de_Calor.py
