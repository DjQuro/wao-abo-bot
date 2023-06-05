# -*- coding: utf-8 -*-
import json
import logging
import os
import sys
import time
import urllib
import urllib.parse
import requests
#import wao.api

from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

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


def init():
    if config['testmode'] == True:
        id = 13370815
        logger.warning("Test-Mode Enabled!")
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
        stationsfile = f"data/{id}/stations.json"
        with open("data/318491860/stations.json") as preset:
            json_string = preset.read()
        f = open(stationsfile, 'w+')
        f.write(json_string)
        f.close()
        logger.info("READY!")
    else:
        if config['bot_token'] == "<yourbottokenhere>":
            logger.error("Invalid Bot Token")
        else:
            logger.info(f"Authorized with {config['bot_token']} Starting!")
            if config['adminID'] == "<adminchatidhere>":
                logger.error("Invalid Admin Chat ID - These are required for Announce and Error Reporting!")
            checkUpdate()
            main()


def main():
    updater = Updater(config['bot_token'], use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler('subscriptions', list_subs))
    dp.add_handler(CommandHandler('abos', list_subs))
    dp.add_handler(CommandHandler('subs', list_subs))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CallbackQueryHandler(button_unsubscribe, pattern='^remove_'))
    dp.add_handler(CallbackQueryHandler(button_subscribe, pattern='^add_'))
    dp.add_handler(CommandHandler('next', checksubs))
    dp.add_handler(CommandHandler('time', setTime))
    dp.add_handler(CommandHandler('announce', announce))
    dp.add_handler(CommandHandler('live', now_live))
    dp.add_handler(CallbackQueryHandler(live_button, pattern='^live_'))
    dp.add_handler(CommandHandler('stations', get_stations_keyboard))
    dp.add_handler(CallbackQueryHandler(handle_station_subscription, pattern=r"toggle_station_.*"))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

def get_stations_keyboard(update, context):
    chat_id = update.effective_chat.id
    stations_file = f"data/{chat_id}/stations.json"
    sender_file = "sender.json"

    with open(stations_file, "r") as file:
        stations_data = json.load(file)

    with open(sender_file, "r") as file:
        sender_data = json.load(file)

    keyboard = []
    for sender in sender_data:
        sender_name = sender_data[sender].get("name")
        sender_id = sender_data[sender].get("id")
        if sender_name and sender_id:
            button_text = f"❌ {sender_name}" if sender_name in stations_data["stations"] else f"➕ {sender_name}"
            button_callback = f"toggle_station_{sender_name}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=button_callback)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=chat_id, text="Wähle einen Sender aus:", reply_markup=reply_markup)


def handle_station_subscription(update, context):
    chat_id = update.callback_query.message.chat_id
    stations_file = f"data/{chat_id}/stations.json"
    sender_file = "sender.json"
    callback_data = update.callback_query.data
    sender_name = callback_data.split("_")[-1]

    with open(stations_file, "r") as file:
        stations_data = json.load(file)

    if sender_name in stations_data["stations"]:
        del stations_data["stations"][sender_name]
    else:
        with open(sender_file, "r") as file:
            sender_data = json.load(file)
            sender_id = None
            for sender, data in sender_data.items():
                if data["name"] == sender_name:
                    sender_id = data["id"]
                    break
            if sender_id:
                stations_data["stations"][sender_name] = sender_id

    with open(stations_file, "w") as file:
        json.dump(stations_data, file, indent=4)

    update.callback_query.message.reply_text("Deine Auswahl wurde aktualisiert.")
    update.callback_query.message.delete()

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


def now_live(update, context):
    keyboard = []
    json_data = get_radio_data()
    row = []
    for station_key, station_value in json_data.items():
        if isinstance(station_value, dict):
            # Erstellt einen InlineKeyboardButton für jeden Sender und fügt ihn zur aktuellen Zeile hinzu
            row.append(InlineKeyboardButton(station_key, callback_data=f"live_{station_key}"))
            # Wenn drei Buttons in der Zeile erreicht sind, füge die Zeile zur Tastatur hinzu und starte eine neue Zeile
            if len(row) == 2:
                keyboard.append(row)
                row = []

    # Füge die letzte Zeile zur Tastatur hinzu, falls nicht bereits geschehen
    if row:
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Wähle einen Sender:', reply_markup=reply_markup)


def live_button(update, context):
    query = update.callback_query
    station_key = query.data[5:]

    json_data = get_radio_data()
    station_value = json_data.get(station_key, {})

    dj_value = station_value.get('dj', 'Playlist')
    sn_value = station_value.get('sn', 'Kein Showname')
    t_value = station_value.get('t', 'Unbekannter Titel')
    a_value = station_value.get('a', 'Unbekannter Artist')
    if dj_value != 'Playlist':
        message = f"ℹ️Live auf {station_key}.FMℹ️\n\r\n\r🎧{t_value}\n\r{a_value}\n\r🎙️{dj_value}, {sn_value}"
    else:
        message = f"ℹ️Live auf {station_key}.FMℹ️\n\r\n\r🎧{t_value}\n\r{a_value}\n\rKein DJ on Air"

    query.edit_message_text(text=message)


def get_radio_data():
    radio_url = "https://api.weareone.fm/v1/radio"
    response = requests.get(radio_url)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        return {}


def setTime(update, context):
    id = str(update.effective_chat.id)
    minutes = " ".join(context.args)

    if update.message.chat.type == "group" or update.message.chat.type == "supergroup":
        user_id = update.message.from_user.id
        chat_id = update.message.chat_id
        user = context.bot.get_chat_member(chat_id, user_id)
        if user.status in ["administrator", "creator"]:
            if minutes:
                minutes = int(minutes)  # Konvertiere den Eingabe-String in eine Ganzzahl
                if minutes > 1440:
                    update.message.reply_text(
                        "Alles über den heutigen Tag kann der Bot nicht sehen! Bitte wähle einen Wert zwischen 1 und 1440.")
                else:
                    if minutes < 1:
                        update.message.reply_text(
                            "Bitte wähle einen Wert zwischen 1 und 1440.")
                    else:
                        with open(f"data/{id}/config.json") as userConfig:
                            json_string = userConfig.read()
                        conf = json.loads(json_string)
                        update.message.reply_text(
                            f"Die frühste Benachrichtigung ist auf {conf['minInfo']} Minuten eingestellt.")
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
            minutes = int(minutes)  # Konvertiere den Eingabe-String in eine Ganzzahl
            if minutes > 1440:
                update.message.reply_text(
                    "Alles über den heutigen Tag kann der Bot nicht sehen! Bitte wähle einen Wert zwischen 1 und 1440.")
            else:
                if minutes < 1:
                    update.message.reply_text(
                        "Bitte wähle einen Wert zwischen 1 und 1440.")
                else:
                    userConfig = f"data/{id}/config.json"
                    f = open(userConfig, 'w+')
                    f.write('{"minInfo": ' + str(minutes) + '}')
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
            stationsfile = f"data/{id}/stations.json"
            with open("sender.json") as preset:
                json_string = preset.read()
            f = open(stationsfile, 'w+')
            f.write(json_string)
            f.close()
            logger.info(f"Creating data/{id}/stations.json")
            logger.info("READY!")
            context.bot.send_message(chat_id=id,
                                     text="Herzlich Willkommen beim WAO Abo Bot! \n\r "
                                          "Nutze /subscribe um einen DJ zu abonnieren.\n\r\n\r ")
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
        stationsfile = f"data/{id}/stations.json"
        with open("sender.json") as preset:
            json_string = preset.read()
        f = open(stationsfile, 'w+')
        f.write(json_string)
        f.close()
        logger.info("READY!")
        context.bot.send_message(chat_id=id,
                                 text="Herzlich Willkommen beim WAO Abo Bot! \n\r "
                                      "Nutze /subscribe um einen DJ zu abonnieren.\n\r\n\r ")

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
    message = update.message.reply_text(
        "Welchen DJ möchtest du deabonnieren?",
        reply_markup=reply_markup
    )

    # Speichere die Nachrichten-ID für das spätere Löschen
    context.user_data["message_id"] = message.message_id


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

    # Lösche die vorherige Nachricht mit dem Inline-Keyboard
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=context.user_data["message_id"])

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
    message = update.message.reply_text(
        "Welchen DJ möchtest du abonnieren?",
        reply_markup=reply_markup
    )

    # Speichere die Nachrichten-ID für das spätere Löschen
    context.user_data["message_id"] = message.message_id


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

        # Lösche die vorherige Nachricht mit dem Inline-Keyboard
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=context.user_data["message_id"])

        # Sende eine Bestätigungsnachricht an den Benutzer
        query.answer(text=f"{dj} wurde erfolgreich abonniert.")
        logger.info(f"{query.message.from_user.username} hat {dj} abonniert!")
    else:
        # Wenn der DJ bereits abonniert ist, sende eine Fehlermeldung an den Benutzer
        query.answer(text=f"{dj} ist bereits abonniert.")



def blacklist(update, context):
    id = str(update.effective_chat.id)
    dj = " ".join(context.args)
    if id != config['adminID']:
        context.bot.send_message(chat_id=update.effective_chat.id, text="KEINE BERECHTIGUNG!")
    else:
        if dj:
            with open("blacklist.json") as blacklistf:
                json_string = blacklistf.read()
            blacklistArray = json.loads(json_string)
            blacklist = blacklistArray["blacklist"]
            blacklistf.close()
            if dj in blacklist:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"{dj} ist bereits auf der Blacklist!")
            else:
                blacklist.append(dj)
                logger.info(f"{update.message.from_user.username} hat {dj} in die Blacklist aufgenommen!")
                with open(f"blacklist.json", "w") as blacklistf:
                    data = {
                        "blacklist": blacklist
                    }
                    json_string = json.dumps(data, indent=4)
                    blacklistf.write(json_string)
                blacklistf.close()
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Du hast {dj} auf die Blacklist gesetzt!")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Bitte gib an, wen du bannen möchtest.")


def checksubs(update, context):
    id = str(update.effective_chat.id)
    showCount = 0
    with open(f"data/{id}/stations.json") as f:
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
                                 text="In den nächsten 15 Minuten beginnen keine Shows auf deinen abonnierten Kanälen!")


def list_subs(update, context):
    id = str(update.effective_chat.id)
    i = 0
    with open(f"data/{id}/subs.json") as subfile:
        json_string = subfile.read()
    subs = json.loads(json_string)
    for sub in subs["subscriptions"]:
        if i == 0:
            subnames = sub
        else:
            subnames = subnames + "\n\r"
            subnames = subnames + sub
        i = i + 1
    if i == 0:
        update.message.reply_text("Du hast keinen DJ abonniert")
    elif i == 1:
        update.message.reply_text("Du hast einen DJ abonniert\n\r\n\r" + subnames)
    else:
        update.message.reply_text("Du hast " + str(i) + " DJs abonniert\n\r\n\r" + subnames)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.error('Update "%s" caused error "%s"', update, context.error)
    message = f'Update "{update}" caused error "{context.error}"'
    content = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage?chat_id={config['adminID']}&parse_mode=Markdown&text={message}"
    requests.get(content)


init()
