const logger = require('./modules/logger');
logger.info(`Loading /modules/logger`);
const configLoader = require('./modules/configLoader');
logger.info(`Loading /modules/configLoader`);
const apiHelper = require('./modules/apiHelper');
logger.info(`Loading /modules/apiHelper`);
const showProcessor = require('./modules/showProcessor');
logger.info(`Loading /modules/showProcessor`);
const blacklistHandler = require('./modules/blacklistHandler');
logger.info(`Loading /modules/blacklistHandler`);
const telegram = require('./modules/telegram'); // Telegram-Modul importieren
logger.info(`Loading /modules/telegram`);

logger.info(`Bot gestartet`);
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

// Main-Funktion jede Minute ausführen
setInterval(main, 60 * 1000); // alle 60 Sekunden

// Starte den Bot sofort
main();
