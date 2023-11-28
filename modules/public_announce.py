import urllib
import urllib.parse
import requests
import json
import logging
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import requests

with open("/root/WAO-Abobot/config.json") as f:
    json_string = f.read()
config = json.loads(json_string)

def announce(text):
    try:
        if arg:
            message = " ".join(text.args)
            rootdir = '/root/WAO-Abobot/data'
            for rootdir, dirs, files in os.walk(rootdir):
                for subdir in dirs:
                    chatid = os.path.join(subdir)
                    encoded_message = urllib.parse.quote(message)
                    content = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage?chat_id={chatid}&parse_mode=Markdown&text={encoded_message}"
                    requests.get(content)
                    print (f"Sent {chatid}")
            print('DONE!')
        else:
            handle_exception(f"You need to provide a Message!")
    except Exception as e:
        handle_exception(f"Error in announce: {e}")
        
def handle_exception(error_message):
    print(error_message)