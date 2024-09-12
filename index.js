const configLoader = require('./modules/configLoader');
const apiHelper = require('./modules/apiHelper');
const showProcessor = require('./modules/showProcessor');
const blacklistHandler = require('./modules/blacklistHandler');
const notification = require('./modules/notification');
const updateModule = require('./modules/updateModule');
const logger = require('./modules/logger'); // Logger-Modul importieren

// Hauptfunktion des Programms
async function main() {

    const versionUrl = 'https://raw.githubusercontent.com/DjQuro/wao-abo-bot/2.0_JS-Rework/config/versions.json'; // Remote-URL zu deiner versions.json
    const localVersionPath = './config/versions.json'; // Pfad zur lokalen versions.json

    // Überprüfe auf Updates
    const isUpdateAvailable = await updateModule.checkForUpdate(versionUrl, localVersionPath);

    if (isUpdateAvailable) {
        console.log('Ein Update ist verfügbar!');
        // Option zum Aktualisieren ausführen
        await updateModule.updateSystem();
    } else {
        console.log('Keine Updates verfügbar.');
    }

    try {
        // Lade die Konfiguration
        const config = await configLoader.loadConfig('./config/config.json');

        // Lade die Blacklist
        const blacklist = await blacklistHandler.loadBlacklist('./config/blacklist.json');

        // API-Anfrage für Show-Daten
        const showData = await apiHelper.fetchShowData(config.apiUrl);

        // Verarbeite die Shows, die nicht auf der Blacklist stehen
        if (showData) {
            showData.forEach(show => {
                if (!blacklistHandler.isBlacklisted(show, blacklist)) {
                    showProcessor.processShows([show], config);
                    notification.sendNotification(show);
                } else {
                    logger.info(`Die Show ${show.n} von ${show.m} steht auf der Blacklist und wird übersprungen.`);
                }
            });
        }

    } catch (error) {
        logger.error(`Fehler im Hauptprozess: ${error.message}`); // Fehlerprotokollierung
    }
}

// Starte das Programm
main();