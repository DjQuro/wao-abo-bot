#!/bin/bash

# Service-Dateien installieren
for service_file in services/*.service; do
  sudo cp "$service_file" /etc/systemd/system/
  sudo systemctl enable $(basename "$service_file")
  sudo systemctl start $(basename "$service_file")
done

# Services-Ordner löschen
rm -r services

# Cronjob für log_maintenance.sh hinzufügen
(crontab -l 2>/dev/null; echo "0 0 * * * /root/WAO-Abobot/log_maintenance.sh") | crontab -

# Python 3 und pip installieren (falls nicht bereits installiert)
sudo apt-get update
sudo apt-get install -y python3 python3-pip

# Pakete aus requirements.txt installieren
pip3 install -r requirements.txt

# Alle zuvor installierten Services neu starten
for service_file in /etc/systemd/system/*.service; do
  sudo systemctl restart $(basename "$service_file" .service)
done
