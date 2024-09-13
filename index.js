const logger = require('./modules/logger');
console.log(`Loading /modules/logger`);
const configLoader = require('./modules/configLoader');
console.log(`Loading /modules/configLoader`);
const apiHelper = require('./modules/apiHelper');
console.log(`Loading /modules/apiHelper`);
const showProcessor = require('./modules/showProcessor');
console.log(`Loading /modules/showProcessor`);
const blacklistHandler = require('./modules/blacklistHandler');
console.log(`Loading /modules/blacklistHandler`);
const telegram = require('./modules/telegram'); // Telegram-Modul importieren
console.log(`Loading /modules/telegram`);

async function init() {
try {
        const config = await configLoader.loadConfig('./config/config.json');
        console.log("Telegram-Token: ", config.telegramToken);
        console.log("Chat-ID: ", config.telegramChatId);
	console.log(`Bot started!`);
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

// Main-Funktion jede Minute ausführen
setInterval(main, 60 * 1000); // alle 60 Sekunden

// Starte den Bot sofort
init();
main();
