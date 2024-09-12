const { DateTime } = require("luxon");
const logger = require('./logger');

function sendNotification(show) {
    try {
        // Verwende direkt die Felder ohne Standardwerte
        const showName = show.n; 
        const djName = show.m;

        // Unix-Zeit umwandeln, falls vorhanden
        const startUnix = show.s;
        const startTime = startUnix ? DateTime.fromMillis(startUnix).toFormat('HH:mm') : 'Invalid DateTime';

        // Erstelle die Benachrichtigung ohne Fallback
        const notificationMessage = `📣 Benachrichtigung: Die Show ${showName} von ${djName} startet ${show.dateLabel} um ${startTime}!`;
        console.log(notificationMessage);
        logger.info(`Benachrichtigung gesendet: ${notificationMessage}`);
    } catch (error) {
        logger.error(`Fehler beim Senden der Benachrichtigung: ${error.message}`);
    }
}

module.exports = { sendNotification };



