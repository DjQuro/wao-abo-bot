const { DateTime } = require("luxon");
const logger = require('./logger');
const telegram = require('./telegram');

// Mapping von Sender-IDs zu Sendernamen
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

// Standard Benachrichtigung
function sendNotification(show, stationId, config) {
    try {
        const showName = show.n || 'Unbekannte Show';
        const djName = show.m || 'Unbekannter DJ';
        const stationName = stations[stationId] || `Sender mit ID ${stationId}`;
        const startUnix = show.s;
        const endUnix = show.e;
        const startTime = DateTime.fromMillis(startUnix).toFormat('HH:mm');
        const endTime = DateTime.fromMillis(endUnix).toFormat('HH:mm');
        const dateLabel = show.dateLabel || 'heute';

        const notificationMessage = `📣 Die Show ${showName} von ${djName} auf ${stationName} startet ${dateLabel} um ${startTime} Uhr und geht bis ${endTime} Uhr!`;

        telegram.sendTelegramMessage(notificationMessage, config);
        logger.info(`Benachrichtigung gesendet: ${notificationMessage}`);
    } catch (error) {
        logger.error(`Fehler beim Senden der Show-Ankündigung: ${error.message}`);
    }
}

// Verlängerungsbenachrichtigung
function sendExtension(show, stationId, endTime, config) {
    try {
        const stationName = stations[stationId] || `Sender mit ID ${stationId}`;
        const formattedEndTime = DateTime.fromMillis(endTime).toFormat('HH:mm');
        const notificationMessage = `⏱️ Die Sendung ${show.n} von ${show.m} auf ${stationName} wurde bis ${formattedEndTime} verlängert!`;

        telegram.sendTelegramMessage(notificationMessage, config);
        logger.info(`Benachrichtigung gesendet: ${notificationMessage}`);
    } catch (error) {
        logger.error(`Fehler beim Senden der Verlängerungs-Benachrichtigung: ${error.message}`);
    }
}

// Absage-Benachrichtigung
function sendCancellation(showName, djName, stationId, config) {
    try {
        const stationName = stations[stationId] || `Sender mit ID ${stationId}`;
        const notificationMessage = `🚫 Die Sendung ${showName} von ${djName} auf ${stationName} wurde abgesagt!`;

        telegram.sendTelegramMessage(notificationMessage, config);
        logger.info(`Benachrichtigung gesendet: ${notificationMessage}`);
    } catch (error) {
        logger.error(`Fehler beim Senden der Absage-Benachrichtigung: ${error.message}`);
    }
}

// EasterEgg für Housealarm
function sendCustomMessage(show, stationId, config) {
    try {
        const stationName = stations[stationId] || `Sender mit ID ${stationId}`;
        const startTime = DateTime.fromMillis(show.s).toFormat('HH:mm');
        const notificationMessage = `🚨 Der Housealarm wird heute um ${startTime} auf ${stationName} durch ${show.m} ausgelöst!`;

        telegram.sendTelegramMessage(notificationMessage, config);
        logger.info(`Benachrichtigung gesendet: ${notificationMessage}`);
    } catch (error) {
        logger.error(`Fehler beim Senden des EasterEgg: ${error.message}`);
    }
}

module.exports = { sendNotification, sendExtension, sendCancellation, sendCustomMessage };
