# -*- coding: utf-8 -*-
import json
import logging
import os
import sys
import time
import urllib
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

import requests

with open("versions.json") as versionfile:
    version_string = versionfile.read()
versions = json.loads(version_string)
versionfile.close()

with open("config.json") as f:
    json_string = f.read()
config = json.loads(json_string)

djs_file = "djs.json"

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[ %(asctime)s - %(levelname)s ] %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

with open("stations.json") as f:
    stationlist = json.load(f)
stations = stationlist["stations"]


def checkUpdate():
    with urllib.request.urlopen(
            "https://raw.githubusercontent.com/DjQuro/wao-abo-bot/main/versions.json") as remoteVersion:
        rem_version_string = remoteVersion.read()

        remoteVersion = json.loads(rem_version_string)

    if versions['indexer'] == remoteVersion['indexer']:
        logger.info(f"Installed Announcer-Version: {versions['indexer']} - Up to Date!")
    else:
        logger.warning(
            f"Installed Announcer-Version: {versions['indexer']} - Please Update! (New Version: {remoteVersion['indexer']})")


def updateDB():
    day = 0
    new = 0
    dj_count = 0
    deleted = 0
    base_url = "https://api.weareone.fm/v1/showplan/{station}/{day}"
    logger.info("Datenbank wird aktualisiert!")

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

                    # Prüfe, ob DJ bereits in djs.json existiert
                    if dj_name not in djs:
                        logger.info(f"{dj_name} in die Datenbank aufgenommen.")
                        djs[dj_name] = {"last_seen": last_seen}
                        new += 1
                    else:
                        dj_count += 1
                        # Prüfe, ob DJ seit maxInactivityDays Tagen nicht mehr erkannt wurde
                        if datetime.strptime(djs[dj_name]["last_seen"],
                                             "%Y-%m-%d %H:%M:%S") < datetime.now() - timedelta(180):
                            logger.warning(
                                f"{dj_name} seit 180 Tagen nicht mehr erkannt. Wird aus der Datenbank entfernt.")
                            del djs[dj_name]
                            deleted += 1
                            dj_count -= 1
                        else:
                            djs[dj_name]["last_seen"] = last_seen

            else:
                logger.error(f"[{station}] FEHLER {status} von {endpoint_url}")

        # Speichere die aktualisierte djs.json
        with open(djs_file, "w") as f:
            json.dump(djs, f)
        day += 1
    logger.info(f"Datenbank erfolgreich aktualisiert! Neue Einträge:{new} Gelöschte Einträge:{deleted} Registrierte DJs:{new + dj_count}")

while True:
    checkUpdate()
    updateDB()
    time.sleep(3600)
