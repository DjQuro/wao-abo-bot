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

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[ %(asctime)s - %(levelname)s ] %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


def checkUpdate():
    with urllib.request.urlopen(
            "https://raw.githubusercontent.com/DjQuro/wao-abo-bot/main/versions.json") as remoteVersion:
        rem_version_string = remoteVersion.read()

        remoteVersion = json.loads(rem_version_string)

    if versions['announcer'] == remoteVersion['announcer']:
        logger.info(f"Installed Announcer-Version: {versions['announcer']} - Up to Date!")
    else:
        logger.info(
            f"Installed Announcer-Version: {versions['announcer']} - Please Update! (New Version: {remoteVersion['announcer']})")


# Create the base URL string
with open("stations.json") as f:
    stationlist = json.load(f)

base_url = "https://api.weareone.fm/v1/showplan/{station}/1"
stations = stationlist["stations"]
stationCount = len(stations)

logger.info(f"WAO Bot {versions['announcer']} started - loaded {stationCount} stations")


def check():
    rootdir = 'data'
    for subdir in os.scandir(rootdir):
        if subdir.is_dir():
            chatid = subdir.name
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
                response = requests.get(endpoint_url)
                status = str(response.status_code)
                if response.ok:
                    data = response.json()
                    for x in data:
                        if x["m"] in subs["subscriptions"] and x["s"] // 1000 > time.time():
                            uid = x["mi"] + x["s"] + x["e"]
                            startUnix = x["s"] // 1000
                            startOffset = startUnix - time.time()
                            if minTime >= startOffset and uid not in sent:
                                show = x["n"]
                                dj = x["m"]
                                start_time = datetime.fromtimestamp(startUnix).strftime("%d.%m.%Y um %H:%M")
                                end_time = datetime.fromtimestamp(x["e"] // 1000).strftime("%H:%M")
                                message = f"⏰📣 Die Show {show} von {dj} auf {station} startet am {start_time}🎙️ #weareone!"
                                encoded_message = urllib.parse.quote(message)
                                content = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage?chat_id={chatid}&parse_mode=Markdown&text={encoded_message}"
                                requests.get(content)
                                sent.append(uid)

                    with open(cache_file, "w") as sentShows:
                        json.dump({"sent": sent}, sentShows)

                else:
                    logger.error(f"[{station}] FEHLER {status} von {endpoint_url}")


checkUpdate()
while True:
    check()
    time.sleep(60)
