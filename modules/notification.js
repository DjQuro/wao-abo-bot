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

// Benachrichtigungsfunktion für Show-Ankündigung
function sendNotification(show, stationId, config) {
    try {
        const showName = show.n || 'Unbekannte Show';
        const djName = show.m || 'Unbekannter DJ';
        const stationName = stations[stationId] || `Sender mit ID ${stationId}`;
        const startUnix = show.s;
        const endUnix = show.e;

        // Debugging: Überprüfen, ob die Endzeit existiert
        if (!endUnix) {
            logger.error(`Endzeit für Show ${showName} von ${djName} auf ${stationName} fehlt!`);
            return;
        }

        const startTime = DateTime.fromMillis(startUnix).toFormat('HH:mm');
        const endTime = DateTime.fromMillis(endUnix).toFormat('HH:mm');
        const dateLabel = show.dateLabel || 'heute';

        // Easter Egg: Special message for Quro and Housealarm
        if (djName === 'Quro' && showName.includes('Housealarm')) {
            const easterEggMessage = `🚨 Der Housealarm wird heute um ${startTime} auf ${stationName} durch ${djName} ausgelöst!`;
            telegram.sendTelegramMessage(easterEggMessage, config);
            logger.info(`EasterEgg Benachrichtigung gesendet: ${easterEggMessage}`);
        } else {
            const notificationMessage = `📣 Die Show ${showName} von ${djName} auf ${stationName} startet ${dateLabel} um ${startTime} Uhr und geht bis ${endTime} Uhr!`;
            // Sende die Nachricht an den Telegram-Bot
            telegram.sendTelegramMessage(notificationMessage, config);
            logger.info(`Benachrichtigung gesendet: ${notificationMessage}`);
        }
    } catch (error) {
        logger.error(`Fehler beim Senden der Show-Ankündigung: ${error.message}`);
    }
}

// Benachrichtigungsfunktion für Absage
function sendCancellation(showName, djName, stationId, config) {
    try {
        const stationName = stations[stationId] || `Sender mit ID ${stationId}`;
        const notificationMessage = `🚫 Die Sendung ${showName} von ${djName} auf ${stationName} wurde abgesagt!`;

        // Sende die Nachricht an den Telegram-Bot
        telegram.sendTelegramMessage(notificationMessage, config);
        logger.info(`Benachrichtigung gesendet: ${notificationMessage}`);
    } catch (error) {
        logger.error(`Fehler beim Senden der Absage-Benachrichtigung: ${error.message}`);
    }
}

// Benachrichtigungsfunktion für Verlängerung
function sendExtension(showName, djName, stationId, endTime, config) {
    try {
        // Überprüfe, ob die Endzeit vorhanden ist
        if (!endTime) {
            logger.error(`Endzeit für die Verlängerung der Show ${showName} von ${djName} fehlt!`);
            return;
        }

        const stationName = stations[stationId] || `Sender mit ID ${stationId}`;
        const formattedEndTime = DateTime.fromMillis(endTime).toFormat('HH:mm');
        const notificationMessage = `⏱️ Die Sendung ${showName} von ${djName} auf ${stationName} wurde bis ${formattedEndTime} verlängert!`;

        // Sende die Nachricht an den Telegram-Bot
        telegram.sendTelegramMessage(notificationMessage, config);
        logger.info(`Benachrichtigung gesendet: ${notificationMessage}`);
    } catch (error) {
        logger.error(`Fehler beim Senden der Verlängerungs-Benachrichtigung: ${error.message}`);
    }
}

module.exports = { sendNotification, sendCancellation, sendExtension };
