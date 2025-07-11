#!/bin/bash

# Script para renovar certificados SSL automaticamente
# Certifique-se de que este script seja executado como root

# Caminho para o log de renovação
LOG_FILE="/var/log/ssl_renew.log"

echo "Iniciando renovação de certificados SSL em $(date)" >> $LOG_FILE

# Comando para renovar certificados
certbot renew >> $LOG_FILE 2>&1

# Verificação do status
if [ $? -eq 0 ]; then
    echo "Renovação simulada bem-sucedida em $(date)." >> $LOG_FILE
else
    echo "Erro durante a renovação em $(date)." >> $LOG_FILE
fi