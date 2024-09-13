const moment = require('moment');
const logger = require('./logger');
const notification = require('./notification');
const cacheHelper = require('./cacheHelper');
const telegram = require('./telegram');

async function processShowsInParallel(showData, config, blacklist) {
    const cache = await cacheHelper.loadCache();
    const processedShows = cache.processedShows || [];
    const cancelledShows = cache.cancelledShows || [];
    const extendedShows = cache.extendedShows || [];

    const now = moment();

    const processPromises = showData.map(({ stationId, shows }) => {
        return new Promise((resolve, reject) => {
            try {
                shows.forEach(show => {
                    const showStartTime = moment(show.s);
                    const showEndTime = moment(show.e);

                    // Nur kommende Shows melden
                    if (now.isAfter(showStartTime)) {
                        logger.info(`Die Show ${show.n} startet um ${showStartTime.format('HH:mm')} und wird nicht gemeldet, da sie bereits begonnen hat oder vergangen ist.`);
                        return; // Überspringe laufende oder vergangene Shows
                    }

                    // Nur Shows, die nicht verarbeitet wurden und noch kommen
                    if (!processedShows.some(ps => ps.id === show.mi && ps.start === show.s)) {
                        logger.info(`Ankündigung für Show: ${show.n}`);
                        notification.sendNotification(show, stationId, config); // Stelle sicher, dass config übergeben wird
                        processedShows.push({ id: show.mi, start: show.s, end: show.e });
                    }

                    // Verlängerungen und Absagen ebenfalls nur für kommende Shows
                    if (now.isBefore(showStartTime)) {
                        // Verlängerung überprüfen
                        const cachedShow = processedShows.find(ps => ps.id === show.mi);
                        if (cachedShow && show.e !== cachedShow.end) {
                            logger.info(`Verlängerung der Show ${show.n} erkannt.`);
                            notification.sendExtension(show.n, show.m, stationId, show.e, config); // Korrekte Parameter übergeben
                            extendedShows.push({ id: show.mi, end: show.e });
                        }

                        // Absage überprüfen
                        if (cancelledShows.includes(show.mi)) {
                            logger.info(`Absage der Show ${show.n} erkannt.`);
                            notification.sendCancellation(show.n, show.m, stationId, config); // Korrekte Parameter übergeben
                        }
                    }

                });

                resolve();
            } catch (error) {
                reject(error);
            }
        });
    });

    await Promise.all(processPromises);

    // Cache speichern
    await cacheHelper.saveCache({
        ...cache,
        processedShows,
        cancelledShows,
        extendedShows
    });
}

module.exports = { processShowsInParallel };
