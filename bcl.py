# -*- coding: utf-8 -*-
import json
import os
import sys
import time
import urllib
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path
import requests
import glob
import subprocess
from modules.help_module import help
from modules.service_control_module import start, stop, restart, status
from modules.blacklist_handler import ban
from modules.dbupdate_module import updatedb
from modules.installer import install
from modules.maintenance_module import reset, logclear

with open("data/banner.txt", "r") as banner_file:
    banner_content = banner_file.read()

with open("versions.json") as versionfile:
    version_string = versionfile.read()
versions = json.loads(version_string)
versionfile.close()

print(banner_content)
print(f"                                                 Bot Command Line Version: {versions['bcl']}")

commander = "wao-commander"
announcer = "wao-announcer"
indexer = "wao-index"
index = "wao-index"

def checkUpdate():
    response = requests.get("https://raw.githubusercontent.com/DjQuro/wao-abo-bot/main/versions.json")
    status = str(response.status_code)
    if response.ok:
        with urllib.request.urlopen(
                "https://raw.githubusercontent.com/DjQuro/wao-abo-bot/main/versions.json") as remoteVersion:
            rem_version_string = remoteVersion.read()
            remoteVersion = json.loads(rem_version_string)
        if versions['bcl'] != remoteVersion['bcl']:
            print(
                f"Installed Announcer-Version: {versions['announcer']} - Please Update! (New Version: {remoteVersion['bcl']})")
    else:
        print(f"Update-Check failed! ERROR: {status}")

def handle_exception(error_message):
    print(error_message)
    time.sleep(5)
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    sys.exit()

def process_command(command, argument):
    if command == 'status':
        status(argument)
    elif command == 'ban':
        ban(argument)
    else:
        globals()[command](argument)
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        handle_exception("Usage: python bcl.py <command> [argument]\nYou can use python bcl.py help for Commands")

    command = sys.argv[1]
    argument = sys.argv[2] if len(sys.argv) > 2 else None

    process_command(command, argument)

    # Nach dem Ausführen des initialen Befehls, ermöglicht es dem Benutzer, weitere Befehle einzugeben
    while True:
        user_input = input("Enter another command (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        elif user_input:
            command, argument = user_input.split(maxsplit=1)
            process_command(command, argument)
