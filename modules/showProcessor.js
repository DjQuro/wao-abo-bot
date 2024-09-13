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
                    const timeUntilStart = showStartTime.diff(now, 'minutes');

                    // Nur kommende Shows melden, die in den nächsten 15 Minuten starten
                    if (timeUntilStart > 15) {
                        logger.info(`Die Show ${show.n} startet um ${showStartTime.format('HH:mm')} und wird nicht gemeldet, da sie mehr als 15 Minuten entfernt ist.`);
                        return; // Überspringe Shows, die mehr als 15 Minuten entfernt sind
                    } else if (now.isAfter(showStartTime) && now.isBefore(showEndTime)) {
                        logger.info(`Die Show ${show.n} läuft und wird nicht erneut angekündigt.`);
                        return; // Überspringe laufende Shows
                    } else if (now.isAfter(showEndTime)) {
                        logger.info(`Die Show ${show.n} ist bereits beendet.`);
                        return; // Überspringe beendete Shows
                    }

                    // Nur Shows, die nicht verarbeitet wurden und noch kommen
                    if (!processedShows.some(ps => ps.id === show.mi && ps.start === show.s)) {
                        logger.info(`Ankündigung für Show: ${show.n}`);
                        notification.sendNotification(show, stationId, config);
                        processedShows.push({ id: show.mi, start: show.s, end: show.e });
                    }

                    // Verlängerungen überprüfen, nur wenn die Show noch läuft
                    const cachedShow = processedShows.find(ps => ps.id === show.mi);
                    if (cachedShow && now.isBefore(showEndTime) && show.e !== cachedShow.end) {
                        logger.info(`Verlängerung der Show ${show.n} erkannt.`);
                        notification.sendExtension(show.n, show.m, stationId, show.e, config);
                        extendedShows.push({ id: show.mi, end: show.e });
                    }

                    // Absage der Show überprüfen
                    if (cancelledShows.includes(show.mi)) {
                        logger.info(`Absage der Show ${show.n} erkannt.`);
                        notification.sendCancellation(show.n, show.m, stationId, config);
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
