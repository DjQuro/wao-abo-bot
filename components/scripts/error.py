import logging
import sys
import json
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter(f'[ %(asctime)s - %(levelname)s ] %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('/root/WAO-Abobot/logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

with open("/root/WAO-Abobot/config.json") as f:
    json_string = f.read()
config = json.loads(json_string)

def error(component, context):
    """Log Errors caused by Updates."""
    with open("/root/WAO-Abobot/status.json") as statusfile:
        json_string = statusfile.read()
    statuslist = json.loads(json_string)
    statuslist[component] += 1

    # Schreibe die aktualisierte statuslist zurück in die Datei
    with open("/root/WAO-Abobot/status.json", "w") as statusfile:
        json.dump(statuslist, statusfile)

    error_msg = context.get("error", "Unbekannter Fehler")
    logger.error('Caused Error "%s"', error_msg)

    # Send error message
    message = f'⚠️⚠️⚠️ STÖRUNG! - [{component}] Fehler "{error_msg}"'
    content = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage?chat_id={config['adminID']}&parse_mode=Markdown&text={message}"
    try:
        requests.get(content)
    except Exception as e:
        logger.error('Failed to send error message to Telegram. Error: %s', str(e))
        with open("/root/WAO-Abobot/status.json") as statusfile:
            json_string = statusfile.read()
        statuslist = json.loads(json_string)
        statuslist[component] += 1
        
        with open("/root/WAO-Abobot/status.json", "w") as statusfile:
            json.dump(statuslist, statusfile)