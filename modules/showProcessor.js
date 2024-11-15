const moment = require('moment');
const logger = require('./logger');
const notification = require('./notification');
const telegram = require('./telegram');
const { loadSubsJson } = require('./cacheHelper');
const { loadCache, saveCache } = require('./cacheHelper');  // Cache laden und speichern

async function processShowsInParallel(showData, config, blacklist) {
    const now = moment();
    const subs = await loadSubsJson();  // Abonnements für alle Chats laden
    const cache = await loadCache();  // Lade den Cache
    const processedShows = cache.processedShows || [];  // Falls kein Cache vorhanden, leer starten
    const cancelledShows = cache.cancelledShows || [];
    const extendedShows = cache.extendedShows || [];

    const processPromises = showData.map(({ stationId, shows }) => {
        return new Promise((resolve, reject) => {
            try {
                shows.forEach(show => {
                    const showStartTime = moment(show.s);
                    const showEndTime = moment(show.e);
                    const showName = show.n || 'Unbekannte Show';
                    const djName = show.m || 'Unbekannter DJ';

                    // Nur kommende Shows melden (nicht vergangene oder laufende Shows)
                    if (now.isAfter(showStartTime)) {
                        logger.info(`Die Show ${showName} wird nicht gemeldet, da sie bereits begonnen hat oder vergangen ist.`);
                        return; // Überspringen
                    }

                    // Überprüfen, ob der DJ im aktuellen Chat abonniert wurde
                    const chatSubs = subs.chats[show.chatId] || { djs: [] };

                    if (!chatSubs.djs.includes(djName)) {
                        return; // Wenn der DJ nicht abonniert ist, überspringen
                    }

                    // Check für die Ankündigungszeit, nur innerhalb der richtigen Zeitspanne benachrichtigen
                    const timeUntilStart = showStartTime.diff(now, 'minutes');
                    if (timeUntilStart <= chatSubs.notificationTime) {
                        logger.info(`Ankündigung für Show: ${showName}`);
                        notification.sendNotification(show, stationId, config);
                        processedShows.push({ id: show.mi, start: show.s, end: show.e });
                    }

                    // Verlängerungen und Absagen
                    if (showEndTime.isAfter(now)) {
                        if (!processedShows.some(ps => ps.id === show.mi && ps.end === show.e)) {
                            logger.info(`Verlängerung der Show ${showName} erkannt.`);
                            notification.sendExtension(show, stationId, show.e, config);
                            extendedShows.push({ id: show.mi, end: show.e });
                        }
                    }

                    if (blacklist.includes(djName)) {
                        logger.info(`Absage der Show ${showName} erkannt.`);
                        notification.sendCancellation(showName, djName, stationId, config);
                        cancelledShows.push({ id: show.mi });
                    }

                    // EasterEgg für Housealarm
                    if (djName === 'Quro' && showName.includes('Housealarm')) {
                        notification.sendCustomMessage(show, stationId, config);
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
    await saveCache({
        processedShows,
        cancelledShows,
        extendedShows
    });
}

module.exports = { processShowsInParallel };
