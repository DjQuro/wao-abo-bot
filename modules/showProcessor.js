const logger = require('./logger');
const notification = require('./notification');
const blacklistHandler = require('./blacklistHandler');
const cacheHelper = require('./cacheHelper');
const moment = require('moment');

async function processShowsInParallel(showData, config, blacklist) {
    const cache = await cacheHelper.loadCache();
    const processedShows = cache.processedShows || [];

    const processPromises = showData.map(show => {
        return new Promise((resolve, reject) => {
            try {
                // Debugging: Logge die Show-Daten direkt, wenn sie abgerufen werden
                //logger.info(`Verarbeite Show-Daten (Rohdaten): ${JSON.stringify(show, null, 2)}`);

                // Überprüfe, ob die Show-Daten vollständig sind
                const showName = show.n || 'Unbekannte Show';
                const djName = show.m || 'Unbekannter DJ';

                // Überprüfe, ob die Show bereits verarbeitet wurde
                if (processedShows.includes(showName)) {
                    logger.info(`Die Show ${showName} wurde bereits verarbeitet.`);
                    return resolve();
                }

                // Überprüfe, ob das Zeitfeld existiert und korrekt ist
                const startTime = show.s ? moment(show.s).format('YYYY-MM-DD HH:mm:ss') : 'Unbekannte Zeit';

                if (!blacklistHandler.isBlacklisted(show, blacklist)) {
                    processShows([show], config);

                    // Sende die Benachrichtigung
                    notification.sendNotification(show);

                    processedShows.push(show.n); // Show zur Liste der verarbeiteten Shows hinzufügen
                } else {
                    logger.info(`Die Show ${showName} von ${djName} steht auf der Blacklist und wird übersprungen.`);
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
        logger.info(`Verarbeite Show: ${show.n || 'Unbekannte Show'} von ${show.m || 'Unbekannter DJ'}`);
    });
}

module.exports = { processShows, processShowsInParallel };
