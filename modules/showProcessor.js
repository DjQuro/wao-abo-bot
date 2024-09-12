const cacheHelper = require('./cacheHelper');
const logger = require('./logger');
const notification = require('./notification');

// Parallele Show-Verarbeitung mit Caching
async function processShowsInParallel(showData, config, blacklist) {
    const cache = await cacheHelper.loadCache();
    const processedShows = cache.processedShows || [];

    const processPromises = showData.map(show => {
        return new Promise((resolve, reject) => {
            try {
                // Überprüfe, ob die Show bereits verarbeitet wurde
                if (processedShows.includes(show.n)) {
                    logger.info(`Die Show ${show.n} wurde bereits verarbeitet und wird übersprungen.`);
                    return resolve();
                }

                if (!blacklistHandler.isBlacklisted(show, blacklist)) {
                    processShows([show], config);
                    notification.sendNotification(show);
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

    // Warte auf die parallele Verarbeitung aller Shows
    await Promise.all(processPromises);

    // Speichere die aktualisierte Liste der verarbeiteten Shows
    await cacheHelper.saveCache({
        ...cache,
        processedShows
    });
}

module.exports = { processShowsInParallel };
