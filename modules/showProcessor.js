// modules/showProcessor.js
const logger = require('./logger');
const notification = require('./notification');
const blacklistHandler = require('./blacklistHandler');
const cacheHelper = require('./cacheHelper');  // Importiere cacheHelper
const moment = require('moment'); // Für die Zeitformatierung (ggf. installieren: npm install moment)

async function processShowsInParallel(showData, config, blacklist) {
    const cache = await cacheHelper.loadCache();
    const processedShows = cache.processedShows || [];

    const processPromises = showData.map(show => {
        return new Promise((resolve, reject) => {
            try {
                // Überprüfe, ob die Show-Daten vollständig sind
                if (!show || !show.n || !show.m || processedShows.includes(show.n)) {
                    logger.info(`Die Show ${show.n || 'Unbekannt'} wurde bereits verarbeitet oder ist ungültig.`);
                    return resolve();
                }

                // Überprüfe, ob das Zeitfeld existiert und korrekt ist
                const startTime = show.s ? moment(show.s).format('YYYY-MM-DD HH:mm:ss') : 'Unbekannte Zeit';

                if (!blacklistHandler.isBlacklisted(show, blacklist)) {
                    processShows([show], config);
                    notification.sendNotification(`${show.dateLabel}: ${show.n} von ${show.m} startet um ${startTime}!`);
                    processedShows.push(show.n); // Show zur Liste der verarbeiteten Shows hinzufügen
                } else {
                    logger.info(`Die Show ${show.n} von ${show.m} steht auf der Blacklist und wird übersprungen.`);
                }
                resolve();
            } catch (error) {
                reject(error);
            }
        });
    });

    await Promise.all(processPromises);

    await cacheHelper.saveCache({
        ...cache,
        processedShows
    });
}

function processShows(shows, config) {
    shows.forEach(show => {
        logger.info(`Verarbeite Show: ${show.n} von ${show.m}`);
        // Logik zur Show-Verarbeitung hier
    });
}

module.exports = { processShows, processShowsInParallel };


