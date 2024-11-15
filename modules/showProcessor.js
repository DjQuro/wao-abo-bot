const moment = require('moment');
const logger = require('./logger');
const notification = require('./notification');
const cacheHelper = require('./cacheHelper');
const telegram = require('./telegram');
const commands = require('./commands');

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

                    // Ignoriere abgelaufene Shows
                    if (now.isAfter(showStartTime)) {
                        return;
                    }

                    // Oster-Ei-Bedingung
                    if (show.m === "Quro" && show.n.includes("Housealarm") && showStartTime.diff(now, 'minutes') <= config.notificationTime) {
                        const easterEggMessage = `🚨 Der Housealarm wird heute um ${showStartTime.format('HH:mm')} auf ${notification.stations[stationId]} durch ${show.m} ausgelöst!`;
                        telegram.sendTelegramMessage(easterEggMessage, config);
                        logger.info(`Easter-Egg Nachricht gesendet: ${easterEggMessage}`);
                        return;
                    }

                    // Abonnements und Benachrichtigungen je Chat
                    const allChatPromises = Object.entries(commands.getAllSubscriptions()).map(async ([chatId, chatSubs]) => {
                        if (chatSubs.djs.includes(show.m) || chatSubs.stations.includes(stationId)) {
                            if (!processedShows.some(ps => ps.id === show.mi && ps.start === show.s) &&
                                showStartTime.diff(now, 'minutes') <= chatSubs.notificationTime) {
                                logger.info(`Ankündigung für Show: ${show.n} im Chat ${chatId}`);
                                notification.sendNotification(show, stationId, config, chatId);
                                processedShows.push({ id: show.mi, start: show.s, end: show.e });
                            }

                            // Verlängerungen erkennen und senden
                            const previousEndTime = processedShows.find(ps => ps.id === show.mi)?.end;
                            if (previousEndTime && show.e > previousEndTime) {
                                logger.info(`Verlängerung der Show ${show.n} erkannt und gemeldet.`);
                                notification.sendExtension(show, stationId, chatId);
                                extendedShows.push({ id: show.mi, end: show.e });
                            }

                            // Absagen erkennen und senden
                            if (!shows.find(s => s.mi === show.mi) && !cancelledShows.includes(show.mi)) {
                                logger.info(`Absage der Show ${show.n} erkannt.`);
                                notification.sendCancellation(show.n, show.m, stationId, config);
                                cancelledShows.push(show.mi);
                            }
                        }
                    });

                    return Promise.all(allChatPromises).then(resolve).catch(reject);
                });
            } catch (error) {
                reject(error);
            }
        });
    });

    await Promise.all(processPromises);

    // Speichere den Cache
    await cacheHelper.saveCache({
        ...cache,
        processedShows,
        cancelledShows,
        extendedShows
    });
}

module.exports = { processShowsInParallel };
