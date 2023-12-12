import json
import logging
import os
import sys
import time
import urllib
import urllib.parse
from datetime import datetime
from pathlib import Path
from modules.error import error
from modules.showprocessor import process_show
import requests

component = 'announcer'

with open("/root/WAO-Abobot/blacklist.json") as bansjson:
    json_string = bansjson.read()
blacklist = json.loads(json_string)

with open("/root/WAO-Abobot/config.json") as f:
    json_string = f.read()
config = json.loads(json_string)

def check(base_url):
    rootdir = '/root/WAO-Abobot/data'
    for subdir in os.scandir(rootdir):
        if subdir.is_dir():
            chatid = subdir.name
            try:
                with open(f"/root/WAO-Abobot/data/{chatid}/subs.json") as s:
                    subs = json.load(s)
                with open(f"/root/WAO-Abobot/data/{chatid}/config.json") as c:
                    chatConfig = json.load(c)
                    minTime = chatConfig['minInfo'] * 60
                with open(f'/root/WAO-Abobot/data/{chatid}/stations.json') as s:
                    stationslist = json.load(s)
                    stations = stationslist["stations"]

                cache_file = Path(f"/root/WAO-Abobot/data/{chatid}/cache.json")
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
                            print(f"[{station}] FEHLER {status} von {endpoint_url}")
                    except requests.exceptions.Timeout:
                        error_msg = f"Timeout beim Abrufen der Daten für {station}."
                        error(component, {"error": error_msg})
            except Exception as e:
                error_msg = f"Fehler in der Check-Funktion für ChatID {chatid}. Fehlermeldung: {str(e)}"
                error(component, {"error": error_msg})