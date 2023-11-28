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
            day = 0
            new = 0
            dj_count = 0
            deleted = 0
            base_url = "https://api.weareone.fm/v1/showplan/{station}/{day}"
            with open("blacklist.json") as blacklistfile:
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

                    if response.ok:
                        data = response.json()

                        # Aktualisiere alle Einträge der Station
                        for entry in data:
                            dj_name = entry['m']
                            last_seen = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Prüfe, ob DJ bereits in djs.json existiert und nicht auf der Blacklist steht
                        if dj_name not in djs and dj_name not in blacklist['blacklist']:
                            djs[dj_name] = {"last_seen": last_seen}
                            new += 1
                        else:
                            if dj_name in djs:
                                dj_count += 1
                                # Prüfe, ob DJ seit maxInactivityDays Tagen nicht mehr erkannt wurde
                                if datetime.strptime(djs[dj_name]["last_seen"], "%Y-%m-%d %H:%M:%S") < datetime.now() - timedelta(config["maxInactivityDays"]) and djs[dj_name] not in config["immune"]:
                                    del djs[dj_name]
                                    deleted += 1
                                    dj_count -= 1
                                # Prüfe, ob DJ gebannt wurde
                                elif dj_name in blacklist['blacklist']:
                                    del djs[dj_name]
                                    deleted += 1
                                    dj_count -= 1
                                else:
                                    djs[dj_name]["last_seen"] = last_seen

                    else:
                        print(f"ERROR {status} from  {endpoint_url}")
                        time.sleep(5)
                        # Clear the terminal based on the operating system
                        if os.name == 'nt':  # Windows
                            os.system('cls')
                        else:  # Unix-based systems
                            os.system('clear')
                        sys.exit()

                # Speichere die aktualisierte djs.json
                with open(djs_file, "w") as f:
                    json.dump(djs, f)
                day += 1

            print(f"Database update successful! New Entrys:{new} Purged Entrys:{deleted} Registered DJs:{new + dj_count}")

    except Exception as e:
        handle_exception(f"Error in updateDB: {e}")

def handle_exception(error_message):
    print(error_message)