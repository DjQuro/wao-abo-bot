const moment = require('moment');
const logger = require('./logger');
const notification = require('./notification');
const cacheHelper = require('./cacheHelper');
const telegram = require('./telegram');  // Telegram-Modul importieren

async function processShowsInParallel(showData, config, blacklist) {
    const cache = await cacheHelper.loadCache();
    const processedShows = cache.processedShows || [];

    const processPromises = showData.map(({ stationId, shows }) => {
        return new Promise((resolve, reject) => {
            try {
                shows.forEach(show => {
                    const showStartTime = moment(show.s);
                    const now = moment();

                    // Ankündigung 15 Minuten vorher
                    const timeUntilStart = showStartTime.diff(now, 'minutes');
                    if (timeUntilStart <= 15 && !processedShows.some(ps => ps.id === show.mi && ps.start === show.s)) {
                        logger.info(`Ankündigung für Show: ${show.n}`);
                        notification.sendNotification(show, stationId, config);  // Übergabe der Konfiguration
                        processedShows.push({ id: show.mi, start: show.s, end: show.e });
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

