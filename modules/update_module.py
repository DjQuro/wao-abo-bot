import json
import requests
import urllib
import urllib.parse
import git
from modules.backup_module import backup
from modules.service_control_module import start, stop

with open("/root/WAO-Abobot/versions.json") as versionfile:
    version_string = versionfile.read()
versions = json.loads(version_string)
versionfile.close()

def checkUpdate(component):
    response = requests.get("https://raw.githubusercontent.com/DjQuro/wao-abo-bot/main/versions.json")
    status = str(response.status_code)
    if response.ok:
        with urllib.request.urlopen(
            "https://raw.githubusercontent.com/DjQuro/wao-abo-bot/main/versions.json") as remoteVersion:
            rem_version_string = remoteVersion.read()
            remoteVersion = json.loads(rem_version_string)
        if versions[component] != remoteVersion[component]:
          return True
        else:
          return False
    else:
        print('\033[F', end='', flush=True)
        print(f"Update-Check failed! ERROR: {status}")
        
def update(arg=None):
    update_available_commander = checkUpdate('commander')
    update_available_announcer = checkUpdate('announcer')
    update_available_bcl = checkUpdate('bcl')
    
    if update_available_commander:
        print(f"Commander: New Update available!")
    else:
        print(f"Commander: Up To Date!")
        
    if update_available_announcer:
        print(f"Announcer: New Update available!")
    else:
        print(f"Announcer: Up To Date!")
        
    if update_available_bcl:
        print(f"BCL: New Update available!")
    else:
        print(f"BCL: Up To Date!")

def getUpdate(arg=None):
    update_available_commander = checkUpdate('commander')
    update_available_announcer = checkUpdate('announcer')
    update_available_bcl = checkUpdate('bcl')
    if update_available_commander or update_available_announcer or update_available_bcl:
        print('\033[F', end='', flush=True)
        backup()
        print('\033[F', end='', flush=True)
        stop()
        try:
             repo = git.Repo('/root/WAO-Abobot')
             origin = repo.remote(name='origin')
             origin.pull()
             print('\033[F', end='', flush=True)
             print(f"Erfolgreich von {repo.remotes.origin.url} aktualisiert.")
             return repo
             start()
             
        except git.exc.GitCommandError as e:
             
             print('\033[F', end='', flush=True)
             print(f"Fehler beim Aktualisieren des Repositoriums: {e}")
             return None
             start()
    else:
        print('\033[F', end='', flush=True)
        print("No update required!")