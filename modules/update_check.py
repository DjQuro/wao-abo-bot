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
    
    with open("/root/WAO-Abobot/config.json") as configFile:
        config_string = configFile.read()
    config = json.loads(config_string)
    configFile.close()
    versionfile.close()
    response = requests.get(f"https://raw.githubusercontent.com/DjQuro/wao-abo-bot/{config['updateBranch']}/versions.json")
    status = str(response.status_code)
    if response.ok:
        with urllib.request.urlopen(
                f"https://raw.githubusercontent.com/DjQuro/wao-abo-bot/{config['updateBranch']}/versions.json") as remoteVersion:
            rem_version_string = remoteVersion.read()
            remoteVersion = json.loads(rem_version_string)
        if remoteVersion != "404:Not Found" and versions[component] == remoteVersion[component]:
            return False
        else:
            return True, remoteVersion[component]
    else:
        error(component, f"Update-Check failed! ERROR: {status}")
