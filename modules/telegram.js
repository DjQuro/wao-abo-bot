const fetch = require('node-fetch');
const logger = require('./logger');

function sendTelegramMessage(message, config) {
    const telegramToken = config.telegramToken;
    const chatId = config.telegramChatId;

    // Überprüfen, ob der Telegram-Token und die Chat-ID vorhanden sind
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

module.exports = { sendTelegramMessage };
