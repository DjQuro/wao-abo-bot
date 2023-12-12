import json
import time
import requests
import urllib
import urllib.parse
from datetime import datetime

with open("/root/WAO-Abobot/config.json") as f:
    json_string = f.read()
config = json.loads(json_string)

with open("/root/WAO-Abobot/blacklist.json") as bansjson:
    json_string = bansjson.read()
blacklist = json.loads(json_string)

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
            print(f"Announced {dj}, {show}, {uid} von {start_time} Uhr bis {end_time} Uhr @ {chatid}")
            encoded_message = urllib.parse.quote(message)
            content = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage?chat_id={chatid}&parse_mode=Markdown&text={encoded_message}"
            requests.get(content)
            sent.append(uid)
            with open(cache_file, "w") as sentShows:
                json.dump({"sent": sent}, sentShows)
                