import json
import logging
import sys
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

import requests

cache = {}

def load_cache(station):
    return cache.get(station, {"sent": []})

def save_cache(station, data):
    cache[station] = data

def setup_logging():
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

    return logger

def load_config():
    with open("djchannels.json") as f:
        return json.load(f)

def telegram_public_message(message, bot_token, chat_id):
    encoded_message = urllib.parse.quote(message)
    content = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={encoded_message}"
    requests.get(content)

def check(config):
    stations = config.pop("stations")
    base_url = "https://api.weareone.fm/v1/showplan/{station}/1"
    for station, id in stations.items():
        endpoint_url = base_url.format(station=id)

        now = time.time()
        current_time = datetime.fromtimestamp(now).strftime("%d.%m.%Y %H:%M")
        response = requests.get(endpoint_url)
        status = str(response.status_code)
        try:
            if response.status_code == 200:
                data = json.loads(response.text)
                cache_data = load_cache(station)
                sent = cache_data["sent"]

                for x in data:
                    show = x["n"]
                    dj = x["m"]
                    start_unix = x["s"]
                    end_unix = x["e"] // 1000
                    start_unix //= 1000
                    start_time = datetime.fromtimestamp(start_unix).strftime("%d.%m.%Y um %H:%M")
                    end_time = datetime.fromtimestamp(end_unix).strftime("%H:%M")
                    start_offset = start_unix - now

                    for key, value in config.items():
                        if dj in value["djnames"] and start_unix > now:
                            uid = x["mi"] + x["s"] + x["e"]
                            if value["defaultTime"] * 60 >= start_offset and uid not in sent:
                                message = value["message"].format(show=show, station=station, startTime=start_time, endTime=end_time)
                                logger.info(f"[{station}] Die Show {show} von {dj} auf {station} startet um {start_time} bis {end_time} - UID: {uid}")
                                telegram_public_message(message, value["bot_token"], value["chatID"])
                                sent.append(uid)

                save_cache(station, {"sent": sent})

            else:
                logger.error(f"[{station}] FEHLER {status} von {endpoint_url}")
        except requests.exceptions.ConnectionError:
            print("Verbindungsfehler aufgetreten. Versuche es erneut.")

if __name__ == "__main__":
    logger = setup_logging()
    config = load_config()

    while True:
        check(config)
        time.sleep(60)
