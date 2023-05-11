# -*- coding: utf-8 -*-
import json
import logging
import os
import sys
import time
import urllib
import urllib.parse
from datetime import datetime

import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[ %(asctime)s - %(levelname)s ] %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

with open("config.json") as f:
    json_string = f.read()
config = json.loads(json_string)
f.close()

with open("versions.json") as versionfile:
    version_string = versionfile.read()
versions = json.loads(version_string)
versionfile.close()


def checkUpdate():
    with urllib.request.urlopen(
            "https://raw.githubusercontent.com/DjQuro/wao-abo-bot/main/versions.json") as remoteVersion:
        rem_version_string = remoteVersion.read()
        remoteVersion = json.loads(rem_version_string)

    if versions['commander'] == remoteVersion['commander']:
        logger.info(f"Installed Commander-Version: {versions['commander']} - Up to Date!")
    else:
        logger.info(
            f"Installed Commander-Version: {versions['commander']} - Please to Version: {remoteVersion['commander']})")


def main():
    updater = Updater(config['bot_token'], use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CallbackQueryHandler(button_unsubscribe, pattern='^remove_'))
    dp.add_handler(CallbackQueryHandler(button_subscribe, pattern='^add_'))
    dp.add_handler(CommandHandler('next', checksubs))
    dp.add_handler(CommandHandler('time', setTime))
    dp.add_handler(CommandHandler('announce', announce))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()



def announce(update, context):
    id = str(update.effective_chat.id)
    if id == config["adminID"]:
        message = " ".join(context.args)
        rootdir = 'data'
        for rootdir, dirs, files in os.walk(rootdir):
            for subdir in dirs:
                chatid = os.path.join(subdir)
                encoded_message = urllib.parse.quote(message)
                content = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage?chat_id={chatid}&parse_mode=Markdown&text={encoded_message}"
                requests.get(content)
        update.message.reply_text("Ankündigung an alle Nutzer gesendet!")
    else:
        update.message.reply_text("Du hast keine Berechtigung dazu!")


def setTime(update, context):
    id = str(update.effective_chat.id)
    minutes = " ".join(context.args)

    if update.message.chat.type == "group" or update.message.chat.type == "supergroup":
        user_id = update.message.from_user.id
        chat_id = update.message.chat_id
        user = context.bot.get_chat_member(chat_id, user_id)
        if user.status in ["administrator", "creator"]:
            if minutes:
                userConfig = f"data/{id}/config.json"
                f = open(userConfig, 'w+')
                f.write('{"minInfo": ' + minutes + '}')
                f.close()
                update.message.reply_text(f"Frühste Benachrichtigung auf {minutes} Minuten gesetzt")
            else:
                with open(f"data/{id}/config.json") as userConfig:
                    json_string = userConfig.read()
                conf = json.loads(json_string)
                update.message.reply_text(f"Die frühste Benachrichtigung bleibt bei {conf['minInfo']} Minuten!")
        else:
            if minutes:
                update.message.reply_text("Du bist kein Gruppenadmin")
            else:
                with open(f"data/{id}/config.json") as userConfig:
                    json_string = userConfig.read()
                conf = json.loads(json_string)
                update.message.reply_text(
                    f"Die frühste Benachrichtigung ist auf {conf['minInfo']} Minuten eingestellt.")
    else:
        if minutes:
            userConfig = f"data/{id}/config.json"
            f = open(userConfig, 'w+')
            f.write('{"minInfo": ' + minutes + '}')
            f.close()
            update.message.reply_text(f"Frühste Benachrichtigung auf {minutes} Minuten gesetzt")
        else:
            with open(f"data/{id}/config.json") as userConfig:
                json_string = userConfig.read()
            conf = json.loads(json_string)
            update.message.reply_text(f"Die frühste Benachrichtigung bleibt bei {conf['minInfo']} Minuten!")


def start(update, context):
    id = str(update.effective_chat.id)
    if update.message.chat.type == "group" or update.message.chat.type == "supergroup":
        user_id = update.message.from_user.id
        chat_id = update.message.chat_id
        user = context.bot.get_chat_member(chat_id, user_id)
        if user.status in ["administrator", "creator"]:
            logger.info(f"Welcoming {id}")
            os.mkdir(f"data/{id}")
            logger.info(f"Creating data/{id}")
            subfile = f"data/{id}/subs.json"
            f = open(subfile, 'w+')
            f.write('{"subscriptions": []}')
            f.close()
            logger.info(f"Creating data/{id}/subs.json")
            cachefile = f"data/{id}/cache.json"
            f = open(cachefile, 'w+')
            f.write('{"sent": []}')
            f.close()
            logger.info(f"Creating data/{id}/cache.json")
            configfile = f"data/{id}/config.json"
            f = open(configfile, 'w+')
            f.write('{"minInfo": ' + config["defaultTime"] + '}')
            f.close()
            logger.info(f"Creating data/{id}/config.json - Default value: {config['defaultTime']} Minutes")
            logger.info("READY!")
            context.bot.send_message(chat_id=id,
                                     text="Herzlich Willkommen beim WAO Abo Bot! \n\r "
                                          "Nutze /subscribe DJ-NAME um einen DJ zu abonnieren.\n\r\n\r "
                                          "Beispiel: /subscribe Quro \n\r\n\r "
                                          "Der Name muss wie bei WAO auf der Website geschrieben sein")
        else:
            update.message.reply_text("Du bist kein Gruppenadmin")
    else:
        logger.info(f"Welcoming {id}")
        os.mkdir(f"data/{id}")
        logger.info(f"Creating data/{id}")
        subfile = f"data/{id}/subs.json"
        f = open(subfile, 'w+')
        f.write('{"subscriptions": []}')
        f.close()
        logger.info(f"Creating data/{id}/subs.json")
        cachefile = f"data/{id}/cache.json"
        f = open(cachefile, 'w+')
        f.write('{"sent": []}')
        f.close()
        logger.info(f"Creating data/{id}/cache.json")
        configfile = f"data/{id}/config.json"
        f = open(configfile, 'w+')
        f.write('{"minInfo": ' + config["defaultTime"] + '}')
        f.close()
        logger.info(f"Creating data/{id}/config.json - Default value: {config['defaultTime']} Minutes")
        logger.info("READY!")
        context.bot.send_message(chat_id=id,
                                 text="Herzlich Willkommen beim WAO Abo Bot! \n\r "
                                      "Nutze /subscribe DJ-NAME um einen DJ zu abonnieren.\n\r\n\r "
                                      "Beispiel: /subscribe Quro \n\r\n\r "
                                      "Der Name muss wie bei WAO auf der Website geschrieben sein")


def unsubscribe(update, context):
    id = str(update.effective_chat.id)

    # Lade die Liste der abonnierten DJs
    with open(f"data/{id}/subs.json") as f:
        subs = json.load(f)
    subscribed_djs = subs["subscriptions"]

    # Erstelle ein Inline Keyboard mit den abonnierten DJs
    keyboard = []
    row = []
    for dj in subscribed_djs:
        if len(row) == 4:
            keyboard.append(row)
            row = []
        row.append(InlineKeyboardButton(dj, callback_data=f"remove_{dj}"))
    if row:
        keyboard.append(row)

    # Erstelle eine Antwort-Tastatur mit dem Inline Keyboard
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Frage den Benutzer, welchen DJ er abbestellen möchte
    update.message.reply_text(
        "Welchen DJ möchtest du deabonnieren?",
        reply_markup=reply_markup
    )


def button_unsubscribe(update, context):
    query = update.callback_query
    dj = query.data[7:]
    id = str(query.message.chat_id)

    # Lade die vorhandenen Abonnements des Benutzers
    with open(f"data/{id}/subs.json") as f:
        subs = json.load(f)

    # Entferne den DJ aus den Abonnements
    subs["subscriptions"].remove(dj)

    # Speichere die aktualisierte Abonnementliste
    with open(f"data/{id}/subs.json", "w") as f:
        json.dump(subs, f)

    # Sende eine Bestätigungsnachricht an den Benutzer
    query.answer(text=f"{dj} wurde erfolgreich deabonniert.")
    logger.info(f"{query.message.from_user.username} hat {dj} deabonniert!")


def subscribe(update, context):
    id = str(update.effective_chat.id)

    # Lade die Liste der abonnierten DJs
    with open(f"data/{id}/subs.json") as f:
        subs = json.load(f)

    # Stelle sicher, dass der Schlüssel "subscriptions" in der subs.json-Datei vorhanden ist
    if "subscriptions" not in subs:
        subs["subscriptions"] = []

    subscribed_djs = subs["subscriptions"]

    # Lade die Liste aller DJs aus der djs.json-Datei und filtere die bereits abonnierten aus
    with open("djs.json") as f:
        all_djs = json.load(f)
    available_djs = [dj for dj in all_djs if dj not in subscribed_djs]

    # Erstelle ein Inline Keyboard mit den verfügbaren DJs
    keyboard = []
    row = []
    for dj in available_djs:
        row.append(InlineKeyboardButton(dj, callback_data=f"add_{dj}"))
        if len(row) == 4:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    # Erstelle eine Antwort-Tastatur mit dem Inline Keyboard
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Frage den Benutzer, welchen DJ er abonnieren möchte
    update.message.reply_text(
        "Welchen DJ möchtest du abonnieren?",
        reply_markup=reply_markup
    )


def button_subscribe(update, context):
    query = update.callback_query
    dj = query.data[4:]
    id = str(query.message.chat_id)

    # Lade die vorhandenen Abonnements des Benutzers
    with open(f"data/{id}/subs.json") as f:
        subs = json.load(f)

    # Füge den neuen DJ zum Abonnement hinzu, wenn er noch nicht abonniert ist
    if dj not in subs["subscriptions"]:
        subs["subscriptions"].append(dj)

        # Speichere die aktualisierte Abonnementliste
        with open(f"data/{id}/subs.json", "w") as f:
            json.dump(subs, f)

        # Sende eine Bestätigungsnachricht an den Benutzer
        query.answer(text=f"{dj} wurde erfolgreich abonniert.")
        logger.info(f"{query.message.from_user.username} hat {dj} abonniert!")
    else:
        # Wenn der DJ bereits abonniert ist, sende eine Fehlermeldung an den Benutzer
        query.answer(text=f"{dj} ist bereits abonniert.")


def checksubs(update, context):
    id = str(update.effective_chat.id)
    showCount = 0
    with open("stations.json") as f:
        json_string = f.read()
        stationlist = json.loads(json_string)

    base_url = "https://api.weareone.fm/v1/showplan/{station}/1"
    stations = stationlist["stations"]
    # Iterate over the stations in the dictionary
    for station, id in stations.items():
        # Use string formatting to insert the station ID into the URL
        endpoint_url = base_url.format(station=id)

        now = time.time()
        # Send a GET request to the generated Endpoint
        response = requests.get(endpoint_url)
        # Check the response status code
        status = str(response.status_code)
        if response.status_code == 200:
            # Parse the JSON data from the response
            with urllib.request.urlopen(endpoint_url) as url:
                data = json.load(url)
            for x in data:
                show = x["n"]
                dj = x["m"]
                startUnix = x["s"]
                startUnix = startUnix // 1000
                startTime = datetime.fromtimestamp(startUnix).strftime("%d.%m.%Y um %H:%M")
                startOffset = startUnix - now
                if 900 >= startOffset > 0:
                    showCount = showCount + 1
                    context.bot.send_message(chat_id=update.effective_chat.id,
                                             text=f"Die Show {show} von {dj} auf {station} startet am {startTime}!")
        else:
            logger.error(f"[{station}] FEHLER {status} von {endpoint_url}")
    if showCount == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="In den nächsten 15 Minuten beginnen keine Shows!")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.error('Update "%s" caused error "%s"', update, context.error)
    message = f'Update "{update}" caused error "{context.error}"'
    content = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage?chat_id={config['adminID']}&parse_mode=Markdown&text={message}"
    requests.get(content)


checkUpdate()
main()
