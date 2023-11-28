import os
import zipfile
from datetime import datetime

def backup(arg=None):
    # Verzeichnis und Dateien für das Backup
    backup_folder = "/root/bot-backups"
    source_folder = "/root/WAO-Abobot"
    
    # Erstelle den Zielpfad für das Zip-Verzeichnis
    today = datetime.today().strftime('%Y-%m-%d')
    zip_filename = f"bot_{today}.zip"
    zip_path = os.path.join(backup_folder, zip_filename)
    
    # Erstelle das Zip-Verzeichnis
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for foldername, subfolders, filenames in os.walk(source_folder):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, source_folder)
                zipf.write(file_path, arcname)
    
    print(f"Backup erfolgreich erstellt: {zip_path}")