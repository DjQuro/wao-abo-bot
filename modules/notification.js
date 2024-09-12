const { DateTime } = require("luxon");
const logger = require('./logger');
const telegram = require('./telegram'); // Du hast vergessen, telegram zu importieren

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

function sendNotification(show, stationId, config) {  // Config als Parameter
    try {
        // Logge die Show-Daten
        logger.info(`Roh-Daten: ${JSON.stringify(show)}`);

        const showName = show.n;
        const djName = show.m;

        // Start- und Endzeit der Show umwandeln
        const startUnix = show.s;
        const endUnix = show.e;
        const startTime = DateTime.fromMillis(startUnix).toFormat('HH:mm');
        const endTime = DateTime.fromMillis(endUnix).toFormat('HH:mm');

        // Sendername holen
        const stationName = stations[stationId] || `Sender mit ID ${stationId}`;

        // Überprüfen, ob das dateLabel vorhanden ist
        const dateLabel = show.dateLabel || 'heute';

        // Erstelle die Benachrichtigung mit Start- und Endzeit
        const notificationMessage = `📣 Benachrichtigung: Die Show ${showName} von ${djName} auf ${stationName} startet ${dateLabel} um ${startTime} Uhr und geht bis ${endTime} Uhr!`;

        // Sende die Nachricht an den Telegram-Bot
        telegram.sendTelegramMessage(notificationMessage, config);
        console.log(notificationMessage);
        logger.info(`Benachrichtigung gesendet: ${notificationMessage}`);
    } catch (error) {
        logger.error(`Fehler beim Senden der Benachrichtigung: ${error.message}`);
    }
}

module.exports = { sendNotification };
