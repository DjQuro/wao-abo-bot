import json
import subprocess
from datetime import datetime, timedelta

with open("/root/WAO-Abobot/config.json") as f:
    json_string = f.read()
config = json.loads(json_string)
f.close()

def check_service_status(service_name):
    try:
        result = subprocess.run(['systemctl', 'is-active', service_name], capture_output=True, text=True, check=True)
        status = result.stdout.strip()
        return 'active' if status == 'active' else 'dead'
    except subprocess.CalledProcessError:
        return 'dead'


def status(update, context):
    chat_id = update.effective_chat.id
    with open("/root/WAO-Abobot/versions.json") as f:
        json_string = f.read()
    versions = json.loads(json_string)
    f.close()
    commander = check_service_status("wao-commander")
    monitoring = check_service_status("botmon")

    with open("/root/WAO-Abobot/status.json") as statusfile:
        json_string = statusfile.read()
    statuslist = json.loads(json_string)

    # Konvertiere den notify_check-String in ein Datetime-Objekt
    notify_check_time = datetime.strptime(statuslist['notify_check'], '%Y-%m-%d %H:%M:%S')

    # Berechne die Zielzeit (5 Minuten nach notify_check)
    target_time = notify_check_time + timedelta(minutes=5)

    if notify_check_time <= target_time:
        announcerindicator = '🟢'
    else:
        announcerindicator = '🟡'

    if statuslist['commander'] <= config["maxErrorBeforeYellow"] and commander == 'active':
        commanderindicator = '🟢'
    elif commander != 'dead':
        commanderindicator = '🟡'
    else:
        commanderindicator = '🔴'

    if statuslist['botmon'] <= config["maxErrorBeforeYellow"] and monitoring == 'active':
        monitoringindicator = '🟢'
    elif monitoring != 'dead':
        monitoringindicator = '🟡'
    else:
        monitoringindicator = '🔴'

    if monitoring == 'active' and commander == 'active' and statuslist['announcer'] <= config["maxErrorBeforeYellow"] and \
            statuslist['commander'] <= config["maxErrorBeforeYellow"]:
        message = (
            f"Verfügbarkeit der Dienste:\n\n"
            f"{announcerindicator} - Announcer\n"
            f"{commanderindicator} - Commander\n"
            f"{monitoringindicator} - Monitoring\n\n"
            f"Alle Dienste laufen Störungsfrei!\n\n"
            f"Letztes Datenbank-Update: {statuslist['db_check']}\n"
            f"Letztes Showplan-Update: {statuslist['notify_check']}\n\n"
            f"Commander Version: {versions['commander']}\n"
            f"BCL Version: {versions['bcl']}\n"
            f"Deine ChatID: {chat_id}\n"
            f"Die ChatID kannst du im Supportfall angeben!"
        )
        context.bot.send_message(chat_id=chat_id, text=message)
    elif monitoring == 'active' and commander == 'active' and statuslist['announcer'] >= config["maxErrorBeforeYellow"] or \
            statuslist['commander'] >= config["maxErrorBeforeYellow"]:
        message = (
            f"Verfügbarkeit der Dienste:\n\n"
            f"{announcerindicator} - Announcer\n"
            f"{commanderindicator} - Commander\n"
            f"{monitoringindicator} - Monitoring\n\n"
            f"Aktuell können vereinzelte Störungen auftreten\n\n"
            f"Letztes Datenbank-Update: {statuslist['db_check']}\n"
            f"Letztes Showplan-Update: {statuslist['notify_check']}\n\n"
            f"Commander Version: {versions['commander']}\n"
            f"BCL Version: {versions['bcl']}\n"
            f"Deine ChatID: {chat_id}\n"
            f"Die ChatID kannst du im Supportfall angeben!"
        )
        context.bot.send_message(chat_id=chat_id, text=message)
    elif monitoring == 'dead' or commander == 'dead':
        message = (
            f"Verfügbarkeit der Dienste:\n\n"
            f"{announcerindicator} - Announcer\n"
            f"{commanderindicator} - Commander\n"
            f"{monitoringindicator} - Monitoring\n\n"
            f"Ein oder mehrere Dienste sind ausgefallen!\n\n"
            f"Letztes Datenbank-Update: {statuslist['db_check']}\n"
            f"Letztes Showplan-Update: {statuslist['notify_check']}\n\n"
            f"Commander Version: {versions['commander']}\n"
            f"BCL Version: {versions['bcl']}\n"
            f"Deine ChatID: {chat_id}\n"
            f"Die ChatID kannst du im Supportfall angeben!"
        )
        context.bot.send_message(chat_id=chat_id, text=message)