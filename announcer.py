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


# Senderfunction for public announce
def telegram_public_message(message):
    encoded_message = urllib.parse.quote(message)
    content = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage?chat_id={chatid}&parse_mode=Markdown&text={encoded_message}"
    requests.get(content)


# Create the base URL string
with open("stations.json") as f:
    json_string = f.read()
stationlist = json.loads(json_string)

base_url = "https://api.weareone.fm/v1/showplan/{station}/1"
stations = stationlist["stations"]
stationCount = 0
for station, id in stations.items():
    stationCount = stationCount + 1

logger.info(f"WAO Bot {versions['announcer']} started - loaded {stationCount} stations")


def check():
    rootdir = 'data'
    for rootdir, dirs, files in os.walk(rootdir):
        for subdir in dirs:
            chatid = os.path.join(subdir)
            global current_time, status
            with open(f"data/{chatid}/subs.json") as s:
                sub_string = s.read()
            subs = json.loads(sub_string)
            # Iterate over the stations in the dictionary
            for station, id in stations.items():
                # Use string formatting to insert the station ID into the URL
                endpoint_url = base_url.format(station=id)

                now = time.time()
                current_time = datetime.fromtimestamp(now).strftime("%d.%m.%Y %H:%M")
                # Send a GET request to the generated Endpoint
                response = requests.get(endpoint_url)
                # Check the response status code
                status = str(response.status_code)
                if response.status_code == 200:
                    # Parse the JSON data from the response
                    with urllib.request.urlopen(endpoint_url) as url:
                        data = json.load(url)
                    cache = Path(f"data/{chatid}/cache.json")
                    if cache.is_file():
                        with open(f"data/{chatid}/cache.json") as sentShows:
                            sentJson = sentShows.read()
                        sent = json.loads(sentJson)
                        sent = sent["sent"]
                        sentShows.close()
                    else:
                        f = open(cache, 'w+')
                        f.write('{"sent": []}')
                        f.close()
                        with open(f"data/{chatid}/cache.json") as sentShows:
                            sentJson = sentShows.read()
                        sent = json.loads(sentJson)
                        sent = sent["sent"]
                        sentShows.close()

                    for x in data:
                        show = x["n"]
                        dj = x["m"]
                        startUnix = x["s"]
                        endUnix = x["e"]
                        endUnix = endUnix // 1000
                        startUnix = startUnix // 1000
                        startTime = datetime.fromtimestamp(startUnix).strftime(
                            "%d.%m.%Y um %H:%M"
                        )
                        endTime = datetime.fromtimestamp(endUnix).strftime(
                            "%H:%M"
                        )
                        startOffset = startUnix - now

                        if x["m"] in subs["subscriptions"] and x["s"] // 1000 > now:
                            uid = x["mi"] + x["s"] + x["e"]
                            if 900 >= startOffset and uid not in sent:
                                message = (
                                    f"⏰📣 Die Show {show} von {dj} auf {station} startet am {startTime}🎙️ #weareone!")
                                encoded_message = urllib.parse.quote(message)
                                content = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage?chat_id={chatid}&parse_mode=Markdown&text={encoded_message}"
                                requests.get(content)
                                sent.append(uid)
                                with open(f"data/{chatid}/cache.json", "w") as sentShows:
                                    data = {
                                        "sent": sent
                                    }
                                    json_string = json.dumps(data, indent=4)
                                    sentShows.write(json_string)
                    s.close()

                else:
                    logger.error(f"[{station}] FEHLER {status} von {endpoint_url}")


checkUpdate()
while True:
    check()
    time.sleep(60)
