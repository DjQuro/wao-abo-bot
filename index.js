const configLoader = require('./modules/configLoader');
const apiHelper = require('./modules/apiHelper');
const showProcessor = require('./modules/showProcessor');
const blacklistHandler = require('./modules/blacklistHandler');
const logger = require('./modules/logger');
const telegram = require('./modules/telegram'); // Telegram-Modul importieren

async function main() {
    try {
        const config = await configLoader.loadConfig('./config/config.json');
        const blacklist = await blacklistHandler.loadBlacklist('./config/blacklist.json');
        const stationIds = [5, 6, 7, 8, 10, 11, 13, 14]; // Beispielhafte Sender-IDs

        // Sende eine Nachricht an den Telegram-Bot, dass der Bot gestartet ist
        telegram.sendTelegramMessage('🎉 Der Bot wurde gestartet und überwacht jetzt die Shows!', config);

        const showData = await Promise.all(
            stationIds.map(stationId => apiHelper.fetchShowData(stationId, config.apiBaseUrl))
        );

        await showProcessor.processShowsInParallel(showData, config, blacklist);
    } catch (error) {
        logger.error(`Fehler im Hauptprozess: ${error.message}`);
    }
}

// Main-Funktion jede Minute ausführen
setInterval(main, 60 * 1000); // alle 60 Sekunden

// Starte den Bot sofort
main();
