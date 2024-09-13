const moment = require('moment');
const logger = require('./logger');
const notification = require('./notification');
const cacheHelper = require('./cacheHelper');

async function processShowsInParallel(showData, config) {
    const cache = await cacheHelper.loadCache();
    const processedShows = cache.processedShows || [];
    const cancelledShows = cache.cancelledShows || [];

    const allShowsFromApi = [];

    const processPromises = showData.map(({ stationId, shows }) => {
        return new Promise((resolve, reject) => {
            try {
                shows.forEach(show => {
                    allShowsFromApi.push({ id: show.mi, start: show.s, stationId });  // Erfasse alle Shows

                    const showStartTime = moment(show.s);
                    const now = moment();

                    const existingShow = processedShows.find(ps => ps.id === show.mi && ps.start === show.s && ps.stationId === stationId);

                    // Ankündigung 15 Minuten vorher
                    const timeUntilStart = showStartTime.diff(now, 'minutes');
                    if (timeUntilStart <= 15 && !existingShow) {
                        logger.info(`Ankündigung für Show: ${show.n} von ${show.m} auf ${stationId}`);
                        notification.sendNotification(show, stationId, config);  // Ankündigung der Show
                        processedShows.push({ id: show.mi, start: show.s, end: show.e, stationId, showName: show.n, djName: show.m });
                    }

                    // Verlängerung erkennen
                    if (existingShow && existingShow.end < show.e) {
                        notification.sendExtension(existingShow.showName, existingShow.djName, stationId, show.e, config);
                        existingShow.end = show.e;  // Aktualisiere die Endzeit
                    }
                });

                resolve();
            } catch (error) {
                reject(error);
            }
        });
    });

    await Promise.all(processPromises);

    // Absagen erkennen
    const cancelled = processedShows.filter(ps => !allShowsFromApi.some(apiShow => apiShow.id === ps.id && apiShow.start === ps.start && apiShow.stationId === ps.stationId));
    cancelled.forEach(cancelledShow => {
        notification.sendCancellation(cancelledShow.showName, cancelledShow.djName, cancelledShow.stationId, config);
        cancelledShows.push(cancelledShow);
    });

    await cacheHelper.saveCache({
        ...cache,
        processedShows,
        cancelledShows
    });
}

module.exports = { processShowsInParallel };
