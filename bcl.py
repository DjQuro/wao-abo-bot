# -*- coding: utf-8 -*-
import json
import sys
import time
from datetime import datetime
import traceback
from modules.help_module import help
from modules.service_control_module import start, stop, restart
from modules.blacklist_handler import ban
from modules.dbupdate_module import updatedb
from modules.installer import install
from modules.maintenance_module import reset, logclear
from modules.public_announce import announce
from modules.update_module import checkUpdate, update, getUpdate
from modules.backup_module import backup
from modules.showprocessor import process_show
from modules.error import error
from modules.update_check import checkUpdate
from modules.showplan_check import check as check_showplan

with open("/root/WAO-Abobot/data/banner.txt", "r") as banner_file:
    banner_content = banner_file.read()

with open("/root/WAO-Abobot/versions.json") as versionfile:
    version_string = versionfile.read()
versions = json.loads(version_string)
versionfile.close()
component = "bcl"

print(banner_content)

update_available = checkUpdate("bcl")

if update_available:
    print(f"                                                 Bot Command Line Version: {versions['bcl']}\n                                                 New Update available!")
else:
    print(f"                                                 Bot Command Line Version: {versions['bcl']}\n")

def handle_exception(error_message):
    print(error_message)


def process_command(command, argument):
    if command == 'notify':
        send_update()
    else:
        globals()[command](argument)
    
def newday():
    aktuelle_zeit_unix = time.time()
    aktuelle_zeit = time.localtime(aktuelle_zeit_unix).tm_hour
    start_zeit = 23  # 23:00 Uhr
    end_zeit = 0  # 00:00 Uhr

    if start_zeit <= aktuelle_zeit <= 24 or aktuelle_zeit == start_zeit:
        return True
    else:
        return False

def send_update():
    with open("/root/WAO-Abobot/config.json") as f:
        json_string = f.read()
    config = json.loads(json_string)

    # Create the base URL string
    with open("/root/WAO-Abobot/stations.json") as f:
        stationlist = json.load(f)

    base_url = "https://api.weareone.fm/v1/showplan/{station}/1"
    base_url_morgen = "https://api.weareone.fm/v1/showplan/{station}/2"
    stations = stationlist["stations"]
    stationCount = len(stations)
    try:
        check_showplan(base_url)
        if newday():
            check_showplan(base_url_morgen)

        with open("/root/WAO-Abobot/status.json", "r") as f:
            status = json.load(f)
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status["notify_check"] = current_timestamp
        with open("/root/WAO-Abobot/status.json", "w") as f:
            json.dump(status, f)
        print('\033[F', end='', flush=True)
        print(f"Notification command successfully performed at {current_timestamp}")
    except Exception as e:
        traceback_str = traceback.format_exc()
        error_msg = f"Unbekannter Fehler im Hauptprozess. Fehler: {str(e)}\n{traceback_str}"
        error(component, {"error": error_msg})
    
if __name__ == '__main__':
    # Überprüfe, ob Argumente übergeben wurden
    if len(sys.argv) > 1:
        # Wenn Argumente vorhanden sind, führe den Befehl aus
        command = sys.argv[1]
        argument = sys.argv[2] if len(sys.argv) > 2 else None
        process_command(command, argument)

        # Nach dem Ausführen des initialen Befehls ermöglicht es dem Benutzer, weitere Befehle einzugeben
        while True:
            user_input = input("Enter another command (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break
            elif user_input:
                command, argument = user_input.split(maxsplit=1)
                process_command(command, argument)
    else:
        # Wenn keine Argumente übergeben wurden, starte direkt in der Kommandozeile
        while True:
            user_input = input("Enter a command (or 'exit' 'quit' or 'q' to quit): ")

            if user_input.lower() == 'exit' or 'quit' or 'q':
                break
            elif user_input:
                if ' ' in user_input:
                    command, argument = user_input.split(maxsplit=1)
                else:
                    command = user_input
                    argument = None
                    process_command(command, argument)
