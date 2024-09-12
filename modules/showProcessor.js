const moment = require('moment');
const logger = require('./logger');
const notification = require('./notification');
const telegram = require('./telegram');  // Telegram-Modul importieren

async function processShowsInParallel(showData, config, blacklist) {
    const cache = await cacheHelper.loadCache();
    const processedShows = cache.processedShows || [];
    const extendedShows = cache.extendedShows || [];
    const cancelledShows = cache.cancelledShows || [];

    const processPromises = showData.map(({ stationId, shows }) => {
        return new Promise((resolve, reject) => {
            try {
                shows.forEach(show => {
                    const showName = show.n;
                    const showStartTime = moment(show.s);
                    const now = moment();

                    // Ankündigung 15 Minuten vorher
                    const timeUntilStart = showStartTime.diff(now, 'minutes');
                    if (timeUntilStart <= 15 && !processedShows.some(ps => ps.id === show.mi && ps.start === show.s)) {
                        logger.info(`Ankündigung für Show: ${showName}`);
                        notification.sendNotification(show, stationId);
                        telegram.sendTelegramMessage(`📣 Benachrichtigung: Die Show ${showName} startet in 15 Minuten auf ${stationId}!`, config);
                        processedShows.push({ id: show.mi, start: show.s, end: show.e });
                    }

                    // Verlängerung und Absage - wie zuvor
                    // ...
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
        processedShows,
        extendedShows,
        cancelledShows
    });
}

module.exports = { processShowsInParallel };
