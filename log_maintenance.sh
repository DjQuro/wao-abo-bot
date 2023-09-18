#!/bin/bash

# Definiere die Pfade zu den Verzeichnissen
log_dir="/root/WAO-Abobot"
source_dir="$log_dir"
dest_dir="$log_dir/logs"
log_file="logs.log"

# Verschiebe die logs.log-Datei ins neue Verzeichnis
mv "$source_dir/$log_file" "$dest_dir/$(date +\%Y-\%m-\%d).log"

# Erstelle eine neue logs.log-Datei
touch "$source_dir/$log_file"
echo "New Log" >> $source_dir/$log_file

# Lösche Log-Dateien, die älter als 7 Tage sind
find "$dest_dir" -type f -name "*.log" -mtime +7 -exec rm {} \;
