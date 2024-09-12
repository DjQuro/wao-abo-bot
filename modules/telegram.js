const fetch = require('node-fetch');
const logger = require('./logger');

// Funktion zum Senden einer Nachricht an Telegram
async function sendTelegramMessage(message, config) {
    const telegramApiUrl = `https://api.telegram.org/bot${config.telegramToken}/sendMessage`;

    try {
        const response = await fetch(telegramApiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                chat_id: config.telegramChatId,
                text: message
            })
        });

        if (!response.ok) {
            throw new Error(`Fehler beim Senden der Nachricht: ${response.statusText}`);
        }

        logger.info(`Telegram-Benachrichtigung gesendet: ${message}`);
    } catch (error) {
        logger.error(`Fehler beim Senden der Telegram-Benachrichtigung: ${error.message}`);
    }
}

module.exports = { sendTelegramMessage };
