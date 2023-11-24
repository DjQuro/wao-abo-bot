import json
import os
import sys
import time

with open("/root/WAO-Abobot/config.json") as f:
    json_string = f.read()
config = json.loads(json_string)

def ban(dj):
    try:
        if dj:
            with open("/root/WAO-Abobot/blacklist.json") as blacklistf:
                json_string = blacklistf.read()
            blacklistArray = json.loads(json_string)
            blacklist = blacklistArray["blacklist"]
            blacklistf.close()
            if dj in blacklist:
                handle_exception(f"{dj} is already blacklisted!")
            elif dj in config["immune"]:
                handle_exception(f"{dj} cannot be banned!")
                
            else:
                blacklist.append(dj)
                with open(f"/root/WAO-Abobot/blacklist.json", "w") as blacklistf:
                    data = {
                        "blacklist": blacklist
                    }
                    json_string = json.dumps(data, indent=4)
                    blacklistf.write(json_string)
                blacklistf.close()
                print(f"{dj} has been blacklisted!")
        else:
            print("You need to provide a name! Usage: ban [dj]")
    except Exception as e:
        handle_exception(f"Error in ban: {e}")

def handle_exception(error_message):
    print(error_message)