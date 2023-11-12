#!/bin/bash

# Definiere die Pfade zu den Verzeichnissen
log_dir="/root/WAO-Abobot"
source_dir="$log_dir"
dest_dir="$log_dir/logs"
log_file="logs.log"

# Dienste stoppen
systemctl stop wao-announcer.service
systemctl stop wao-commander.service
systemctl stop wao-index.service

# Verschiebe die logs.log-Datei ins neue Verzeichnis
mv "$source_dir/$log_file" "$dest_dir/$(date +\%Y-\%m-\%d).log"

# Erstelle eine neue logs.log-Datei
touch "$source_dir/$log_file"

# Lösche den Statusfile
rm "$log_dir/status.json"

#Erstelle einen neuen Statusfile
touch "$log_dir/status.json"

#Schreibe die nötigen Daten in den Statusfile
echo '{
  "announcer": 0,
  "commander": 0,
  "indexer": 0
}' > $log_dir/status.json

# Starte Dienste neu
systemctl start wao-announcer.service
systemctl start wao-commander.service
systemctl start wao-index.service

# Lösche Log-Dateien, die älter als 7 Tage sind
find "$dest_dir" -type f -name "*.log" -mtime +7 -exec rm {} \;
