#!/bin/bash

# Переменные
LOG_FILE="/home/jay/Desktop/python/orgproj/orgchar/orgproj/logging/warnings.log"
BACKUP_DIR="/home/jay/Desktop/python/orgproj/orgchar/orgproj/logging/"
DATE=$(date '+%Y%m%d')

# Создание тарбола
tar -czf "$BACKUP_DIR/warnings_log_$DATE.tar.gz" "$LOG_FILE"

echo "" > "$LOG_FILE"

# Отправка тарбола по почте (пример для отправки почтового сообщения с использованием утилиты mail)
# Убедитесь, что у вас настроена почта на вашей системе и утилита mail установлена
#mail -s "Warnings Log Backup" ваша_почта@example.com < "$BACKUP_DIR/warnings_log_$DATE.tar.gz"
