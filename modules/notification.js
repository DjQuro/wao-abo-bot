const { DateTime } = require("luxon");
const logger = require('./logger');

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

function sendNotification(show, stationId) {
    try {
        // Logge die Show-Daten
        logger.info(`Roh-Daten: ${JSON.stringify(show)}`);

        // Verwende die Felder ohne Standardwerte
        const showName = show.n;
        const djName = show.m;

        // Unix-Zeit umwandeln, falls vorhanden
        const startUnix = show.s;
        const startTime = show.s ? DateTime.fromMillis(show.s).toFormat('HH:mm') : 'Invalid DateTime';

        // Holen des Sendernamens
        const stationName = stations[stationId] || 'Unbekannter Sender';

        // Logge jeden Wert separat zur Verifikation
        logger.info(`Showname: ${show.n}`);
        logger.info(`DJ-Name: ${show.m}`);
        logger.info(`Startzeit: ${startTime}`);
        logger.info(`Sender: ${stationName}`);

        // Erstelle die Benachrichtigung mit Sendername
        const notificationMessage = `📣 Benachrichtigung: Die Show ${showName} von ${djName} läuft auf ${stationName} und startet ${show.dateLabel} um ${startTime}!`;
        console.log(notificationMessage);
        logger.info(`Benachrichtigung gesendet: ${notificationMessage}`);
    } catch (error) {
        logger.error(`Fehler beim Senden der Benachrichtigung: ${error.message}`);
    }
}

module.exports = { sendNotification };
