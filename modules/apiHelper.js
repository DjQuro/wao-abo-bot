const fetch = require('node-fetch');
const logger = require('./logger'); // Füge das Logger-Modul hinzu

// Funktion zum Abrufen von Show-Daten von einer API
async function fetchShowData(apiUrl) {
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error(`Fehler beim Abrufen der API-Daten: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        logger.error(`API-Fehler: ${error.message}`); // Fehlerprotokollierung
        return null;
    }
}

module.exports = { fetchShowData };
