
const fetch = require('node-fetch');

// Funktion zum Abrufen von Show-Daten von einer API
async function fetchShowData(apiUrl) {
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error(`Fehler beim Abrufen der API-Daten: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fehler bei der API-Anfrage:', error);
        return null;
    }
}

module.exports = { fetchShowData };
