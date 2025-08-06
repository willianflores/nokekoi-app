#!/bin/bash

# Nokekoi App Backup Script
# Autor: Sistema de backup automático
# Data: 2024

set -e

# Configuration
BACKUP_DIR="/backup/nokekoi"
APP_DIR="/home/srvadmin/nokekoiApp"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="nokekoi_backup_$DATE"
RETENTION_DAYS=30

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create backup directory
create_backup_dir() {
    if [ ! -d "$BACKUP_DIR" ]; then
        mkdir -p "$BACKUP_DIR"
        log_info "Backup directory created: $BACKUP_DIR"
    fi
}

# Backup application files
backup_app() {
    log_info "Starting application backup..."
    
    cd "$APP_DIR"
    
    # Create temporary directory for this backup
    TEMP_BACKUP="$BACKUP_DIR/temp_$DATE"
    mkdir -p "$TEMP_BACKUP"
    
    # Files to backup
    log_info "Backing up application files..."
    cp -r *.py "$TEMP_BACKUP/" 2>/dev/null || log_warn "No Python files found"
    cp -r pages/ "$TEMP_BACKUP/" 2>/dev/null || log_warn "No pages directory found"
    cp -r scripts/ "$TEMP_BACKUP/" 2>/dev/null || log_warn "No scripts directory found"
    cp -r img/ "$TEMP_BACKUP/" 2>/dev/null || log_warn "No img directory found"
    cp -r .streamlit/ "$TEMP_BACKUP/" 2>/dev/null || log_warn "No .streamlit directory found"
    
    # Configuration files
    cp requirements.txt "$TEMP_BACKUP/" 2>/dev/null || log_warn "No requirements.txt found"
    cp .env "$TEMP_BACKUP/env.backup" 2>/dev/null || log_warn "No .env file found"
    cp env.example "$TEMP_BACKUP/" 2>/dev/null || log_warn "No env.example found"
    cp README.md "$TEMP_BACKUP/" 2>/dev/null || log_warn "No README.md found"
    cp *.sh "$TEMP_BACKUP/" 2>/dev/null || log_warn "No shell scripts found"
    
    log_info "Application files backed up to $TEMP_BACKUP"
}

# Backup datasets (metadata only, not the large files)
backup_datasets_metadata() {
    log_info "Backing up datasets metadata..."
    
    if [ -d "$APP_DIR/datasets" ]; then
        mkdir -p "$TEMP_BACKUP/datasets_structure"
        
        # Create structure information
        find "$APP_DIR/datasets" -type f -name "*.parquet" -exec ls -lh {} \; > "$TEMP_BACKUP/datasets_structure/parquet_files.txt"
        find "$APP_DIR/datasets" -type f -name "*.shp" -exec ls -lh {} \; > "$TEMP_BACKUP/datasets_structure/shp_files.txt"
        find "$APP_DIR/datasets" -type f -name "*.tif" -exec ls -lh {} \; > "$TEMP_BACKUP/datasets_structure/tif_files.txt"
        
        # Directory structure
        tree "$APP_DIR/datasets" > "$TEMP_BACKUP/datasets_structure/directory_tree.txt" 2>/dev/null || \
        find "$APP_DIR/datasets" -type d > "$TEMP_BACKUP/datasets_structure/directories.txt"
        
        log_info "Datasets metadata backed up"
    else
        log_warn "No datasets directory found"
    fi
}

# Backup logs
backup_logs() {
    log_info "Backing up logs..."
    
    if [ -d "/var/log" ]; then
        mkdir -p "$TEMP_BACKUP/logs"
        
        # Copy recent log files
        find /var/log -name "*nokekoi*" -mtime -7 -exec cp {} "$TEMP_BACKUP/logs/" \; 2>/dev/null || true
        
        # Application logs
        if [ -f "$APP_DIR/log.txt" ]; then
            cp "$APP_DIR/log.txt" "$TEMP_BACKUP/logs/"
        fi
        
        log_info "Logs backed up"
    fi
}

# Create compressed archive
create_archive() {
    log_info "Creating compressed archive..."
    
    cd "$BACKUP_DIR"
    tar -czf "${BACKUP_NAME}.tar.gz" -C temp_$DATE .
    
    # Remove temporary directory
    rm -rf "temp_$DATE"
    
    # Get archive size
    ARCHIVE_SIZE=$(du -h "${BACKUP_NAME}.tar.gz" | cut -f1)
    log_info "Backup archive created: ${BACKUP_NAME}.tar.gz ($ARCHIVE_SIZE)"
}

# Clean old backups
cleanup_old_backups() {
    log_info "Cleaning up old backups (older than $RETENTION_DAYS days)..."
    
    find "$BACKUP_DIR" -name "nokekoi_backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete
    
    log_info "Old backups cleaned up"
}

# Verify backup
verify_backup() {
    log_info "Verifying backup integrity..."
    
    if tar -tzf "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" > /dev/null 2>&1; then
        log_info "✅ Backup verification successful"
    else
        log_error "❌ Backup verification failed"
        exit 1
    fi
}

# Send notification (optional)
send_notification() {
    if [ ! -z "$ALERT_EMAIL" ]; then
        echo "Nokekoi App backup completed successfully at $(date)" | \
        mail -s "Nokekoi Backup Success - $DATE" "$ALERT_EMAIL" 2>/dev/null || \
        log_warn "Failed to send email notification"
    fi
}

# Main backup function
main() {
    log_info "🔥 Starting Nokekoi App backup process..."
    
    # Load environment variables if available
    if [ -f "$APP_DIR/.env" ]; then
        export $(grep -v '^#' "$APP_DIR/.env" | xargs) 2>/dev/null || true
    fi
    
    # Create backup
    create_backup_dir
    backup_app
    backup_datasets_metadata
    backup_logs
    create_archive
    verify_backup
    cleanup_old_backups
    
    log_info "✅ Backup process completed successfully!"
    log_info "Backup file: $BACKUP_DIR/${BACKUP_NAME}.tar.gz"
    
    # Optional notification
    send_notification
}

# Error handling
trap 'log_error "Backup failed! Check the logs for details."; exit 1' ERR

# Run main function
main "$@" 