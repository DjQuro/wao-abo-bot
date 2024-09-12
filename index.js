const configLoader = require('./modules/configLoader');
const apiHelper = require('./modules/apiHelper');
const showProcessor = require('./modules/showProcessor');
const blacklistHandler = require('./modules/blacklistHandler');
const logger = require('./modules/logger');

// Hauptfunktion des Programms
async function main() {
    try {
        // Lade die Konfiguration
        const config = await configLoader.loadConfig('./config/config.json');

        // Lade die Blacklist
        const blacklist = await blacklistHandler.loadBlacklist('./config/blacklist.json');

        // Beispielhafte Sender-IDs (kannst du anpassen)
        const stationIds = [5, 6, 7, 8, 10, 11, 13, 14];

        // API-Anfragen für mehrere Sender parallel abwickeln
        const allShowData = await apiHelper.fetchShowsForStations(stationIds, config);

        // NEU: Überprüfe, ob die Daten gültig sind, bevor sie verarbeitet werden
        const validShowData = allShowData.filter(show => show && show.n && show.m);
        if (validShowData.length === 0) {
            logger.error('Keine gültigen Show-Daten gefunden.');
            return;
        }

        // Parallele Show-Verarbeitung
        await showProcessor.processShowsInParallel(validShowData, config, blacklist);

    } catch (error) {
        logger.error(`Fehler im Hauptprozess: ${error.message}`); // Fehlerprotokollierung
    }
}

// Starte das Programm
main();
