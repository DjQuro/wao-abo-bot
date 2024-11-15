const moment = require('moment');
const logger = require('./logger');
const notification = require('./notification');
const cacheHelper = require('./cacheHelper');
const telegram = require('./telegram');

const stations = {
    5: 'TechnoBase.FM',
    6: 'HouseTime.FM',
    7: 'HardBase.FM',
    8: 'TranceBase.FM',
    10: 'CoreTime.FM',
    11: 'ClubTime.FM',
    13: 'TeaTime.FM',
    14: 'Replay.FM'
};

async function processShowsInParallel(showData, config, blacklist) {
    const cache = await cacheHelper.loadCache();
    const processedShows = cache.processedShows || [];
    const extendedShows = cache.extendedShows || [];
    const cancelledShows = cache.cancelledShows || [];
    const now = moment();

    const processPromises = showData.map(({ stationId, shows }) => {
        return new Promise((resolve, reject) => {
            try {
                shows.forEach(show => {
                    const showStartTime = moment(show.s);
                    const showEndTime = moment(show.e);
                    const stationName = stations[stationId] || `Sender mit ID ${stationId}`;

                    // Nur heutige und baldige Shows verarbeiten
                    if (showStartTime.isAfter(now.add(1, 'day'))) return;

                    // 15 Minuten vor Start melden, inkl. Easter-Egg-Bedingung für Housealarm
                    const timeUntilStart = showStartTime.diff(now, 'minutes');
                    if (timeUntilStart <= 15 && timeUntilStart > 0) {
                        if (show.m === 'Quro' && show.n.includes('Housealarm') && !processedShows.some(ps => ps.id === show.mi && ps.type === 'easterEgg')) {
                            const customMessage = `🚨 Der Housealarm wird heute um ${showStartTime.format('HH:mm')} auf ${stationName} durch ${show.m} ausgelöst!`;
                            notification.sendCustomMessage(customMessage, null, config);
                            processedShows.push({ id: show.mi, start: show.s, type: 'easterEgg' });
                        } else if (!processedShows.some(ps => ps.id === show.mi)) {
                            // Standardmeldung
                            logger.info(`Ankündigung für Show: ${show.n}`);
                            notification.sendNotification(show, stationId, config);
                            processedShows.push({ id: show.mi, start: show.s, end: show.e });
                        }
                    }

                    // Verlängerungsmeldungen nur bei gültiger neuer Endzeit
                    const existingShow = processedShows.find(ps => ps.id === show.mi);
                    if (existingShow && show.e && show.e !== existingShow.end && now.isBefore(showEndTime)) {
                        notification.sendExtension(show.n, show.m, stationId, show.e, config);
                        existingShow.end = show.e;
                        logger.info(`Verlängerung der Show ${show.n} erkannt und gemeldet.`);
                    }

                    // Absagemeldungen nur einmalig senden
                    if (!shows.some(s => s.mi === show.mi) && !cancelledShows.includes(show.mi)) {
                        notification.sendCancellation(show.n, show.m, stationId, config);
                        cancelledShows.push(show.mi);
                        logger.info(`Absage für Show: ${show.n} von ${show.m} gemeldet.`);
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
        extendedShows,
        cancelledShows
    });
}

module.exports = { processShowsInParallel };
