
const fs = require('fs').promises;

// Funktion zum Laden von JSON-Konfigurationsdateien
async function loadConfig(filePath) {
    try {
        const data = await fs.readFile(filePath, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error('Fehler beim Laden der Konfiguration:', error);
        throw error;
    }
}

module.exports = { loadConfig };
