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
from modules.service_control_module import start, stop, restart
from modules.blacklist_handler import ban
from modules.dbupdate_module import updatedb
from modules.installer import install
from modules.maintenance_module import reset, logclear
from modules.public_announce import announce
from modules.update_module import checkUpdate, update, getUpdate
from modules.backup_module import backup

with open("/root/WAO-Abobot/data/banner.txt", "r") as banner_file:
    banner_content = banner_file.read()

with open("/root/WAO-Abobot/versions.json") as versionfile:
    version_string = versionfile.read()
versions = json.loads(version_string)
versionfile.close()
component = "bcl"

print(banner_content)

update_available = checkUpdate(component)

if update_available:
    print(f"                                                 Bot Command Line Version: {versions['bcl']}\n                                                 New Update available!")
else:
    print(f"                                                 Bot Command Line Version: {versions['bcl']}\n")

def handle_exception(error_message):
    print(error_message)


def process_command(command, argument):
    globals()[command](argument)
    
if __name__ == '__main__':
    # Überprüfe, ob Argumente übergeben wurden
    if len(sys.argv) > 1:
        # Wenn Argumente vorhanden sind, führe den Befehl aus
        command = sys.argv[1]
        argument = sys.argv[2] if len(sys.argv) > 2 else None
        process_command(command, argument)

        # Nach dem Ausführen des initialen Befehls ermöglicht es dem Benutzer, weitere Befehle einzugeben
        while True:
            user_input = input("Enter another command (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break
            elif user_input:
                command, argument = user_input.split(maxsplit=1)
                process_command(command, argument)
    else:
        # Wenn keine Argumente übergeben wurden, starte direkt in der Kommandozeile
        while True:
            user_input = input("Enter a command (or 'exit' to quit): ")

            if user_input.lower() == 'exit':
                break
            elif user_input:
                if ' ' in user_input:
                    command, argument = user_input.split(maxsplit=1)
                else:
                    command = user_input
                    argument = None
                    process_command(command, argument)
