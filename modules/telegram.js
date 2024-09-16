const fetch = require('node-fetch');
const logger = require('./logger');
const commands = require('./commands');  // Lade das commands-Modul

// Funktion zum Senden einer Telegram-Nachricht
function sendTelegramMessage(message, config) {
    const telegramToken = config.telegramToken;
    const chatId = config.telegramChatId;

    if (!telegramToken || !chatId) {
        logger.error('Telegram-Konfiguration fehlt!');
        return;
    }

    const url = `https://api.telegram.org/bot${telegramToken}/sendMessage`;
    const payload = {
        chat_id: chatId,
        text: message
    };

    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
        .then(response => response.json())
        .then(data => {
            if (data.ok) {
                logger.info(`Telegram-Benachrichtigung gesendet: ${message}`);
            } else {
                logger.error(`Telegram-Fehler: ${data.description}`);
            }
        })
        .catch(error => {
            logger.error(`Fehler beim Senden der Telegram-Benachrichtigung: ${error.message}`);
        });
}

// Funktion zur Überprüfung, ob der Absender der Administrator ist
function isAdmin(chatId, config) {
    return chatId === config.adminChatId;
}

// Funktion zum Verarbeiten von Telegram-Befehlen
async function handleTelegramMessage(chatId, message, config) {
    const [command, ...args] = message.split(' ');

    switch (command) {
        case '/subscribe':
            if (args.length > 0) {
                const djName = args.join(' ');
                const response = await commands.subscribeDJ(chatId, djName);
                sendTelegramMessage(response, config);
            } else {
                sendTelegramMessage('Bitte einen DJ-Namen angeben.', config);
            }
            break;

        case '/unsubscribe':
            if (args.length > 0) {
                const djName = args.join(' ');
                const response = await commands.unsubscribeDJ(chatId, djName);
                sendTelegramMessage(response, config);
            } else {
                sendTelegramMessage('Bitte einen DJ-Namen angeben.', config);
            }
            break;

        case '/stations':
            if (args.length > 0) {
                const stationId = parseInt(args[0], 10);
                if (!isNaN(stationId)) {
                    const response = await commands.toggleStation(chatId, stationId);
                    sendTelegramMessage(response, config);
                } else {
                    sendTelegramMessage('Ungültige Station ID.', config);
                }
            } else {
                sendTelegramMessage('Bitte eine Station ID angeben.', config);
            }
            break;

        case '/time':
            if (args.length > 0) {
                const minutes = parseInt(args[0], 10);
                if (!isNaN(minutes)) {
                    const response = await commands.setNotificationTime(chatId, minutes);
                    sendTelegramMessage(response, config);
                } else {
                    sendTelegramMessage('Ungültige Zeitangabe.', config);
                }
            } else {
                sendTelegramMessage('Bitte eine Benachrichtigungszeit angeben.', config);
            }
            break;

        default:
            sendTelegramMessage('Unbekannter Befehl.', config);
            break;
    }
}

module.exports = { sendTelegramMessage, isAdmin, handleTelegramMessage };
