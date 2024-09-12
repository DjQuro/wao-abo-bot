// modules/showProcessor.js
const logger = require('./logger');
const notification = require('./notification');
const blacklistHandler = require('./blacklistHandler');

async function processShowsInParallel(showData, config, blacklist) {
    const processPromises = showData.map(show => {
        return new Promise((resolve, reject) => {
            try {
                if (!blacklistHandler.isBlacklisted(show, blacklist)) {
                    processShows([show], config); // Vorhandene Show-Verarbeitung aufrufen
                    notification.sendNotification(show);
                } else {
                    logger.info(`Die Show ${show.n} von ${show.m} steht auf der Blacklist und wird übersprungen.`);
                }
                resolve();
            } catch (error) {
                reject(error); // Fehler weitergeben
            }
        });
    });

    // Warte auf die parallele Verarbeitung aller Shows
    await Promise.all(processPromises);
}

// Vorhandene Funktion zur sequentiellen Show-Verarbeitung
function processShows(shows, config) {
    shows.forEach(show => {
        logger.info(`Verarbeite Show: ${show.n} von ${show.m}`);
        // Logik zur Show-Verarbeitung hier
    });
}

module.exports = { processShows, processShowsInParallel };

