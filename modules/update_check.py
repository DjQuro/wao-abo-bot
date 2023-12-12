import urllib
import urllib.parse
import requests
import json
import logging
import sys
from modules.error import error

def checkUpdate(component):
    with open("/root/WAO-Abobot/versions.json") as versionfile:
        version_string = versionfile.read()
    versions = json.loads(version_string)
    versionfile.close()
    response = requests.get("https://raw.githubusercontent.com/DjQuro/wao-abo-bot/main/versions.json")
    status = str(response.status_code)
    if response.ok:
        with urllib.request.urlopen(
                "https://raw.githubusercontent.com/DjQuro/wao-abo-bot/main/versions.json") as remoteVersion:
            rem_version_string = remoteVersion.read()
            remoteVersion = json.loads(rem_version_string)
        if versions[component] == remoteVersion[component]:
            return True
        else:
            return False
    else:
        error(component, f"Update-Check failed! ERROR: {status}")