const fetch = require('node-fetch');
const logger = require('./modules/logger');
const configLoader = require('./modules/configLoader');
const telegram = require('./modules/telegram');
const showProcessor = require('./modules/showProcessor');
const blacklistHandler = require('./modules/blacklistHandler');
const apiHelper = require('./modules/apiHelper');
let lastUpdateId = 0;
const { loadSubsJson } = require('./cacheHelper');

async function init() {
    try {
        const config = await configLoader.loadConfig('./config/config.json');
        console.log("Telegram-Token: ", config.telegramToken);
        console.log("Chat-ID: ", config.telegramChatId);

        // Lade die Abonnements
        const subs = await loadSubsJson();

        // Anzahl der hinterlegten Chats
        const chatCount = Object.keys(subs.chats).length;

        // Berechnung der Gesamtanzahl der abonnierten DJs
        let totalDJs = 0;
        Object.values(subs.chats).forEach(chat => {
            totalDJs += chat.djs.length;
        });

        // Logge die Anzahl der Chats und DJs
        console.log(`Anzahl der hinterlegten Chats: ${chatCount}`);
        console.log(`Gesamtanzahl der abonnierten DJs: ${totalDJs}`);

        console.log(`Bot gestartet!`);

        // Starte den Befehlshandler
        setInterval(() => processTelegramUpdates(config), 5000); // Alle 5 Sekunden nach neuen Nachrichten schauen
    } catch (error) {
        logger.error(`Initialisierung fehlgeschlagen: ${error.message}`);
    }
}


async function main() {
    try {
        const config = await configLoader.loadConfig('./config/config.json');
        const blacklist = await blacklistHandler.loadBlacklist('./config/blacklist.json');
        const stationIds = [5, 6, 7, 8, 10, 11, 13, 14]; // Beispielhafte Sender-IDs

        const showData = await Promise.all(
            stationIds.map(stationId => apiHelper.fetchShowData(stationId, config.apiBaseUrl))
        );

        await showProcessor.processShowsInParallel(showData, config, blacklist);
    } catch (error) {
        logger.error(`Fehler im Hauptprozess: ${error.message}`);
    }
}

// Telegram-Nachrichten abholen und verarbeiten
async function processTelegramUpdates(config) {
    try {
        const url = `https://api.telegram.org/bot${config.telegramToken}/getUpdates?offset=${lastUpdateId + 1}`;
        const response = await fetch(url);
        const data = await response.json();

        if (data.ok) {
            const messages = data.result;

            // Verarbeite jede Nachricht
            messages.forEach(message => {
                const chatId = message.message.chat.id;
                const text = message.message.text;

                // Verarbeite den Befehl
                telegram.handleTelegramMessage(chatId, text, config);

                // Aktualisiere den Offset auf die letzte Update-ID
                lastUpdateId = message.update_id;
            });
        }
    } catch (error) {
        logger.error(`Fehler beim Verarbeiten der Telegram-Nachrichten: ${error.message}`);
    }
}

// Main-Funktion jede Minute ausführen
setInterval(main, 60 * 1000); // alle 60 Sekunden

// Starte den Bot sofort
init();
main();
