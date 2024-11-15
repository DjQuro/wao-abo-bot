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

                    // Prüfen, ob die Show heute stattfindet und in den nächsten 15 Minuten beginnt
                    const isToday = showStartTime.isSame(now, 'day');
                    const timeUntilStart = showStartTime.diff(now, 'minutes');
                    if (!isToday || timeUntilStart > 15) {
                        logger.info(`Die Show ${show.n} startet am ${showStartTime.format('YYYY-MM-DD HH:mm')} und wird derzeit nicht gemeldet.`);
                        return; // Überspringe Shows, die nicht heute oder nicht bald starten
                    }

                    // Nur Shows, die nicht verarbeitet wurden und noch kommen
                    if (!processedShows.some(ps => ps.id === show.mi && ps.start === show.s)) {
                        logger.info(`Ankündigung für Show: ${show.n}`);
                        notification.sendNotification(show, stationId, config);
                        processedShows.push({ id: show.mi, start: show.s, end: show.e });
                    }

                    // Verlängerungsprüfung
                    const cachedShow = processedShows.find(ps => ps.id === show.mi);
                    if (cachedShow && cachedShow.end !== show.e) { 
                        // Nur wenn die Endzeit sich geändert hat, wird es als Verlängerung erkannt
                        logger.info(`Verlängerung der Show ${show.n} erkannt.`);
                        notification.sendExtension(show.n, show.m, stationId, show.e, config);
                        cachedShow.end = show.e; // Aktualisiere die Endzeit im Cache
                    }

                    // Absagen
                    if (!shows.some(s => s.mi === show.mi) && !cancelledShows.includes(show.mi)) {
                        logger.info(`Absage der Show ${show.n} erkannt.`);
                        notification.sendCancellation(show.n, show.m, stationId, config);
                        cancelledShows.push(show.mi);
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
