const logger = require('./logger');
const notification = require('./notification');
const blacklistHandler = require('./blacklistHandler');
const cacheHelper = require('./cacheHelper');
const moment = require('moment');

async function processShowsInParallel(showData, config, blacklist) {
    const cache = await cacheHelper.loadCache();
    const processedShows = cache.processedShows || [];

    const processPromises = showData.map(({ stationId, shows }) => {
        return new Promise((resolve, reject) => {
            try {
                // Logge die Shows-Daten inklusive Station-ID
                logger.info(`Station-ID: ${stationId}, Shows: ${JSON.stringify(shows, null, 2)}`);

                if (!shows || shows.length === 0) {
                    logger.error(`Fehler: Keine Shows für Station ${stationId} gefunden.`);
                    return resolve();
                }

                shows.forEach(show => {
                    const showName = show.n || 'Unbekannte Show';
                    if (processedShows.includes(showName)) {
                        logger.info(`Die Show ${showName} wurde bereits verarbeitet.`);
                        return resolve();
                    }

                    // Zeitüberprüfung: Heute oder Morgen?
                    const showTime = moment(show.s);
                    const now = moment();
                    let dateLabel = 'heute';
                    if (showTime.isAfter(now, 'day')) {
                        dateLabel = 'morgen';
                    }

                    // Füge das dateLabel zu den Show-Daten hinzu
                    show.dateLabel = dateLabel;

                    if (!blacklistHandler.isBlacklisted(show, blacklist)) {
                        logger.info(`Verarbeite Show: ${showName} auf Station ${stationId}`);
                        notification.sendNotification(show, stationId);
                        processedShows.push(show.n); // Show zur Liste der verarbeiteten Shows hinzufügen
                    } else {
                        logger.info(`Die Show ${showName} steht auf der Blacklist und wird übersprungen.`);
                    }
                });

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

module.exports = { processShowsInParallel };
