import os
import glob
from datetime import datetime, timedelta
from modules.dbupdate_module import updatedb

def logclear(arg=None):
    try:
        if arg:
            print(f"What the f**k does {arg} mean you fool?")
        else:
            print("PLEASE WAIT! BOT WILL RESTART!...")

            # Definiere die Pfade zu den Verzeichnissen
            log_dir = "/root/WAO-Abobot"
            source_dir = log_dir
            dest_dir = os.path.join(log_dir, "logs")
            log_file = "logs.log"

            # Dienste stoppen
            os.system("systemctl stop botmon.service")
            os.system("systemctl stop wao-commander.service")
            
            # Verschiebe die logs.log-Datei ins neue Verzeichnis
            new_log_path = os.path.join(dest_dir, datetime.now().strftime("%Y-%m-%d") + ".log")
            os.rename(os.path.join(source_dir, log_file), new_log_path)

            # Erstelle eine neue logs.log-Datei
            open(os.path.join(source_dir, log_file), "w").close()
            
            # Lösche den Statusfile
            os.remove(os.path.join(log_dir, "status.json"))

            # Erstelle einen neuen Statusfile
            open(os.path.join(log_dir, "status.json"), "w").close()

            # Schreibe die nötigen Daten in den Statusfile
            status_data = '''
            {
              "announcer": 0,
              "commander": 0,
              "botmon": 0,
              "db_check":"1970-01-01 00:00:00",
              "notify_check":"1970-01-01 00:00:00"
            }
            '''
            with open(os.path.join(log_dir, "status.json"), "w") as status_file:
                status_file.write(status_data)

            # Lösche Log-Dateien, die älter als 7 Tage sind
            seven_days_ago = datetime.now() - timedelta(days=7)
            old_log_files = glob.glob(os.path.join(dest_dir, "*.log"))
            for old_log_file in old_log_files:
                file_date = datetime.strptime(old_log_file.split("/")[-1].split(".")[0], "%Y-%m-%d")
                if file_date < seven_days_ago:
                    os.remove(old_log_file)

            # Starte Dienste neu
            os.system("systemctl start wao-commander.service")
            os.system("systemctl start botmon.service")
            updatedb()

            print("LOGCLEAR SUCCESSFUL!")
                    
    except Exception as e:
        handle_exception(f"Error in logclear: {e}")

def reset(arg=None):
    try:
        if arg:
            handle_exception(f"What the f**k does {arg} mean you fool?")
        else:
            print("PLEASE WAIT! RESETTING!...")

            # Definiere die Pfade zu den Verzeichnissen
            log_dir = "/root/WAO-Abobot"
            source_dir = log_dir
            dest_dir = os.path.join(log_dir, "logs")
            log_file = "logs.log"

            # Dienste stoppen
            os.system("systemctl stop botmon.service")
            os.system("systemctl stop wao-commander.service")

            # Lösche den Statusfile
            os.remove(os.path.join(log_dir, "status.json"))

            # Erstelle einen neuen Statusfile
            open(os.path.join(log_dir, "status.json"), "w").close()

            # Schreibe die nötigen Daten in den Statusfile
            status_data = '''
            {
              "announcer": 0,
              "commander": 0,
              "botmon": 0,
              "db_check":"1970-01-01 00:00:00",
              "notify_check":"1970-01-01 00:00:00"
            }
            '''
            with open(os.path.join(log_dir, "status.json"), "w") as status_file:
                status_file.write(status_data)

            # Starte Dienste neu
            os.system("systemctl start wao-commander.service")
            os.system("systemctl start botmon.service")
            updatedb()

            print("RESET SUCCESSFUL!")
    except Exception as e:
        handle_exception(f"Error in reset: {e}")
        
def handle_exception(error_message):
    print(error_message)

