const fetch = require('node-fetch');
const logger = require('./logger');

// Funktion zum Abrufen der Shows für eine Station
async function fetchShowData(stationId, apiUrl) {
    try {
        const todayUrl = `${apiUrl}/showplan/${stationId}/1`; // Abruf für heute
        const tomorrowUrl = `${apiUrl}/showplan/${stationId}/2`; // Abruf für morgen

        // Logge die URLs zur Verifizierung
        logger.info(`Abrufen von Daten von: ${todayUrl} und ${tomorrowUrl}`);

        // Daten für heute abrufen
        const responseToday = await fetch(todayUrl);
        const todayData = await responseToday.json();

        // Daten für morgen abrufen
        const responseTomorrow = await fetch(tomorrowUrl);
        const tomorrowData = await responseTomorrow.json();

        // Rückgabe der Daten inklusive der Station-ID
        return {
            stationId, // Sender-ID
            shows: [...todayData, ...tomorrowData] // Shows von heute und morgen
        };
    } catch (error) {
        logger.error(`API-Fehler: ${error.message}`);
        throw new Error(`Fehler beim Abrufen der API-Daten: ${error.message}`);
    }
}

module.exports = { fetchShowData };