# -*- coding: utf-8 -*-
import json
import logging
import os
import sys
import time
import urllib
import urllib.parse
from datetime import datetime
from pathlib import Path

import requests

with open("versions.json") as versionfile:
    version_string = versionfile.read()
versions = json.loads(version_string)
versionfile.close()

with open("config.json") as f:
    json_string = f.read()
config = json.loads(json_string)

with open("blacklist.json") as bansjson:
    json_string = bansjson.read()
blacklist = json.loads(json_string)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[ %(asctime)s - %(levelname)s - Announcer] %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('/root/WAO-Abobot/logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


def error(context):
    """Log Errors caused by Updates."""
    with open("status.json") as statusfile:
        json_string = statusfile.read()
    statuslist = json.loads(json_string)
    statuslist['announcer'] += 1

    # Schreibe die aktualisierte statuslist zurück in die Datei
    with open("status.json", "w") as statusfile:
        json.dump(statuslist, statusfile)

    error_msg = context.get("error", "Unbekannter Fehler")
    logger.error('Caused Error "%s"', error_msg)

    # Send error message
    message = f'⚠️⚠️⚠️ STÖRUNG! - [ANNOUNCER] Fehler "{error_msg}"'
    content = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage?chat_id={config['adminID']}&parse_mode=Markdown&text={message}"
    try:
        requests.get(content)
    except Exception as e:
        logger.error('Failed to send error message to Telegram. Error: %s', str(e))
        with open("status.json") as statusfile:
            json_string = statusfile.read()
        statuslist = json.loads(json_string)
        statuslist['announcer'] += 1
        
        with open("status.json", "w") as statusfile:
            json.dump(statuslist, statusfile)


def checkUpdate():
    response = requests.get("https://raw.githubusercontent.com/DjQuro/wao-abo-bot/main/versions.json")
    status = str(response.status_code)
    if response.ok:
        with urllib.request.urlopen(
                "https://raw.githubusercontent.com/DjQuro/wao-abo-bot/main/versions.json") as remoteVersion:
            rem_version_string = remoteVersion.read()
            remoteVersion = json.loads(rem_version_string)
        if versions['announcer'] == remoteVersion['announcer']:
            logger.info(f"Installed Announcer-Version: {versions['announcer']} - Up to Date!")
        else:
            logger.info(
                f"Installed Announcer-Version: {versions['announcer']} - Please Update! (New Version: {remoteVersion['announcer']})")
    else:
        logger.error(f"Update-Check failed! ERROR: {status}")


# Create the base URL string
with open("stations.json") as f:
    stationlist = json.load(f)

base_url = "https://api.weareone.fm/v1/showplan/{station}/1"
base_url_morgen = "https://api.weareone.fm/v1/showplan/{station}/2"
stations = stationlist["stations"]
stationCount = len(stations)

logger.info(f"WAO Bot {versions['announcer']} started - loaded {stationCount} stations")


def newday():
    aktuelle_zeit_unix = time.time()
    aktuelle_zeit = time.localtime(aktuelle_zeit_unix).tm_hour
    start_zeit = 23  # 23:00 Uhr
    end_zeit = 0  # 00:00 Uhr

    if start_zeit <= aktuelle_zeit <= 24 or aktuelle_zeit == start_zeit:
        return True
    else:
        return False


def check():
    rootdir = 'data'
    for subdir in os.scandir(rootdir):
        if subdir.is_dir():
            chatid = subdir.name
            try:
                with open(f"data/{chatid}/subs.json") as s:
                    subs = json.load(s)
                with open(f"data/{chatid}/config.json") as c:
                    chatConfig = json.load(c)
                    minTime = chatConfig['minInfo'] * 60
                with open(f'data/{chatid}/stations.json') as s:
                    stationslist = json.load(s)
                    stations = stationslist["stations"]

                cache_file = Path(f"data/{chatid}/cache.json")
                if cache_file.is_file():
                    with open(cache_file) as sentShows:
                        sent = json.load(sentShows)["sent"]
                else:
                    with open(cache_file, 'w+') as f:
                        f.write('{"sent": []}')
                    sent = []

                for station, id in stations.items():
                    endpoint_url = base_url.format(station=id)
                    try:
                        response = requests.get(endpoint_url, timeout=10)
                        status = str(response.status_code)
                        if response.ok:
                            data = response.json()
                            for x in data:
                                if x["m"] in subs["subscriptions"] and x["s"] // 1000 > time.time() and x['m'] not in blacklist['blacklist']:
                                    uid = x["mi"] + x["s"] + x["e"]
                                    startUnix = x["s"] // 1000
                                    startOffset = startUnix - time.time()
                                    if minTime >= startOffset and uid not in sent:
                                        process_show(x, subs, minTime, sent, chatid, cache_file, station)
                        else:
                            logger.error(f"[{station}] FEHLER {status} von {endpoint_url}")
                    except requests.exceptions.Timeout:
                        error_msg = f"Timeout beim Abrufen der Daten für {station}."
                        error({"error": error_msg})

                if newday():
                    for station, id in stations.items():
                        endpoint_url = base_url_morgen.format(station=id)
                        try:
                            response = requests.get(endpoint_url, timeout=10)
                            status = str(response.status_code)
                            if response.ok:
                                data = response.json()
                                for x in data:
                                    if x["m"] in subs["subscriptions"] and x["s"] // 1000 > time.time() and x['m'] not in blacklist['blacklist']:
                                        uid = x["mi"] + x["s"] + x["e"]
                                        startUnix = x["s"] // 1000
                                        startOffset = startUnix - time.time()
                                        if minTime >= startOffset and uid not in sent:
                                            process_show(x, subs, minTime, sent, chatid, cache_file, station)
                            else:
                                logger.error(f"[{station}] FEHLER {status} von {endpoint_url}")
                        except requests.exceptions.Timeout:
                            error_msg = f"Timeout beim Abrufen der Daten für {station}."
                            error({"error": error_msg})
            except Exception as e:
                error_msg = f"Fehler in der Check-Funktion für ChatID {chatid}. Fehlermeldung: {str(e)}"
                error({"error": error_msg})

def process_show(x, subs, minTime, sent, chatid, cache_file, station):
    if x["m"] in subs["subscriptions"] and x["s"] // 1000 > time.time() and x['m'] not in blacklist['blacklist']:
        uid = x["mi"] + x["s"] + x["e"]
        startUnix = x["s"] // 1000
        startOffset = startUnix - time.time()
        if minTime >= startOffset and uid not in sent:
            show = x["n"]
            dj = x["m"]
            start_time = datetime.fromtimestamp(startUnix).strftime("%H:%M")
            end_time = datetime.fromtimestamp(x["e"] // 1000).strftime("%H:%M")
            message = f"⏰📣 Die Show {show} von {dj} auf {station} startet um {start_time} Uhr #weareone!"
            logger.info(f"Announced {dj}, {show}, {uid} von {start_time} Uhr bis {end_time} Uhr @ {chatid}")
            encoded_message = urllib.parse.quote(message)
            content = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage?chat_id={chatid}&parse_mode=Markdown&text={encoded_message}"
            requests.get(content)
            sent.append(uid)
            with open(cache_file, "w") as sentShows:
                json.dump({"sent": sent}, sentShows)


checkUpdate()
while True:
    try:
        check()
    except Exception as e:
        error_msg = f"Unbekannter Fehler im Hauptprozess. Fehler: {str(e)}"
        error({"error": error_msg})
    time.sleep(60)
