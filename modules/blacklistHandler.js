
const fs = require('fs').promises;

// Funktion zum Laden der Blacklist
async function loadBlacklist(filePath) {
    try {
        const data = await fs.readFile(filePath, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error('Fehler beim Laden der Blacklist:', error);
        throw error;
    }
}

// Funktion zur Überprüfung, ob eine Show auf der Blacklist steht
function isBlacklisted(show, blacklist) {
    return blacklist.includes(show.dj);
}

module.exports = { loadBlacklist, isBlacklisted };
