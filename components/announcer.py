# -*- coding: utf-8 -*-
import json
import os
import sys
import time
import urllib
import urllib.parse
from datetime import datetime
from pathlib import Path
from scripts.showprocessor import process_show
from scripts.error import error
from scripts.update_check import checkUpdate
from scripts.showplan_check import check as check_showplan
import requests
import traceback

with open("/root/WAO-Abobot/config.json") as f:
    json_string = f.read()
config = json.loads(json_string)

component = "announcer"

# Create the base URL string
with open("/root/WAO-Abobot/stations.json") as f:
    stationlist = json.load(f)

base_url = "https://api.weareone.fm/v1/showplan/{station}/1"
base_url_morgen = "https://api.weareone.fm/v1/showplan/{station}/2"
stations = stationlist["stations"]
stationCount = len(stations)


def newday():
    aktuelle_zeit_unix = time.time()
    aktuelle_zeit = time.localtime(aktuelle_zeit_unix).tm_hour
    start_zeit = 23  # 23:00 Uhr
    end_zeit = 0  # 00:00 Uhr

    if start_zeit <= aktuelle_zeit <= 24 or aktuelle_zeit == start_zeit:
        return True
    else:
        return False

with open("/root/WAO-Abobot/versions.json") as versionfile:
    version_string = versionfile.read()
versions = json.loads(version_string)
versionfile.close()

update_available = checkUpdate(component)   

if update_available:
    print(f"Installed Announcer version: {versions['announcer']} - Up to Date!")
else:
    print(f"Installed Announcer version: {versions['announcer']} - Please Update!")

try:
    while True:
        try:
            check_showplan(base_url)
            if newday():
                check_showplan(base_url_morgen)
        except Exception as e:
            traceback_str = traceback.format_exc()
            error_msg = f"Unbekannter Fehler im Hauptprozess. Fehler: {str(e)}\n{traceback_str}"
            error(component, {"error": error_msg})
    time.sleep(60)
except KeyboardInterrupt:
    print("Program terminated by user.")
