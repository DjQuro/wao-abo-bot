import json
import os
import sys
import time
import urllib
import urllib.parse
from pathlib import Path
from datetime import datetime, timedelta
import requests

with open("/root/WAO-Abobot/stations.json") as f:
    stationlist = json.load(f)
stations = stationlist["stations"]

with open("/root/WAO-Abobot/config.json") as f:
    json_string = f.read()
config = json.loads(json_string)

djs_file = "/root/WAO-Abobot/djs.json"

def updatedb(arg=None):  # Updated function definition
    try:
        if arg:
            handle_exception(f"What the f**k does {arg} mean you fool?")
        else:
            print(f"Thinking, Please wait...")
            print("Loading...")
            day = 0
            new = 0
            dj_count = 0
            deleted = 0
            dj_name = ""
            last_seen = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            base_url = "https://api.weareone.fm/v1/showplan/{station}/{day}"
            with open("/root/WAO-Abobot/blacklist.json") as blacklistfile:
                 json_string = blacklistfile.read()
            blacklist = json.loads(json_string)

            while day < 7:
                if os.path.exists(djs_file):
                    with open(djs_file) as f:
                        djs = json.load(f)
                else:
                    djs = {}

                # Aktualisiere alle Stationen
                for station, id in stations.items():
                    endpoint_url = base_url.format(station=id, day=day)
                    response = requests.get(endpoint_url)
                    status = str(response.status_code)
                    print('\033[F', end='', flush=True)
                    print(f"GET {endpoint_url}                        ")

                    if response.ok:
                        data = response.json()

                        # Aktualisiere alle Einträge der Station
                        for entry in data:
                            dj_name = entry['m']
                        
                            # Prüfe, ob DJ bereits in djs.json existiert und nicht auf der Blacklist steht
                            if dj_name not in djs and dj_name not in blacklist['blacklist']:
                                last_seen = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                djs[dj_name] = {"last_seen": last_seen}
                                new += 1
                                print('\033[F', end='', flush=True)
                                print(f"New DJ {dj_name}                  ")
                            else:
                                if dj_name in djs:
                                    # Prüfe, ob DJ seit maxInactivityDays Tagen nicht mehr erkannt wurde
                                    if datetime.strptime(djs[dj_name]["last_seen"], "%Y-%m-%d %H:%M:%S") < datetime.now() - timedelta(config["maxInactivityDays"]) and djs[dj_name] not in config["immune"]:
                                        del djs[dj_name]
                                        deleted += 1
                                        dj_count -= 1
                                        print('\033[F', end='', flush=True)
                                        print(f"Deleted {dj_name} because inactive                          ")
                                    # Prüfe, ob DJ gebannt wurde
                                    elif dj_name in blacklist['blacklist']:
                                        del djs[dj_name]
                                        deleted += 1
                                        dj_count -= 1
                                        print('\033[F', end='', flush=True)
                                        print(f"Deleted {dj_name} because banned                            ")
                                    else:
                                        djs[dj_name]["last_seen"] = last_seen
                                        dj_count += 1
                                        print('\033[F', end='', flush=True)
                                        print(f"No Action for {dj_name}                                     ")

                # Speichere die aktualisierte djs.json und sortiere Sie alphabetisch
                sorted_djs = dict(sorted(djs.items()))
                with open(djs_file, "w") as f:
                    json.dump(sorted_djs, f)

                day += 1
            print('\033[F', end='', flush=True)
            print(f"Database update successful! New Entrys:{new} Purged Entrys:{deleted} Registered DJs:{new + dj_count}")
            # Öffne die Datei zum Lesen und Laden des JSON-Inhalts
            with open("/root/WAO-Abobot/status.json", "r") as f:
                status = json.load(f)
            
            # Aktuellen Zeitstempel erstellen
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Aktualisiere den Wert für den "db_check"-Schlüssel
            status["db_check"] = current_timestamp
            
            # Öffne die Datei erneut zum Schreiben und Speichern des aktualisierten JSON
            with open("/root/WAO-Abobot/status.json", "w") as f:
                json.dump(status, f)

    except Exception as e:
        handle_exception(f"Error in updateDB: {e}")

def handle_exception(error_message):
    print(error_message)

# Funktion zum Sortieren der JSON-Datei alphabetisch hinzugefügt
def sort_json_file(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        sorted_data = dict(sorted(data.items()))
        with open(file_path, "w") as f:
            json.dump(sorted_data, f, indent=4)
    except Exception as e:
        handle_exception(f"Error sorting JSON file: {e}")

# Aufruf der Funktion, um die djs.json-Datei zu sortieren
sort_json_file(djs_file)
