const fs = require('fs').promises;
const path = require('path');
const logger = require('./logger');

// Datei, in der der Cache gespeichert wird
const cacheFilePath = path.join(__dirname, '../cache/cache.json');

// Funktion zum Laden des Caches
async function loadCache() {
    try {
        const data = await fs.readFile(cacheFilePath, 'utf8');
        logger.info('Cache erfolgreich geladen.');
        return JSON.parse(data);
    } catch (error) {
        if (error.code === 'ENOENT') {
            logger.info('Cache-Datei existiert nicht, starte mit leerem Cache.');
            return {}; // Falls kein Cache vorhanden ist, leere Daten zurückgeben
        } else {
            logger.error('Fehler beim Laden des Caches:', error);
            return {}; // Rückgabe eines leeren Caches bei Fehler
        }
    }
}

// Funktion zum Speichern des Caches
async function saveCache(cacheData) {
    try {
        logger.info('Speichere Cache-Daten...');
        await fs.writeFile(cacheFilePath, JSON.stringify(cacheData, null, 2));
        logger.info('Cache erfolgreich gespeichert.');
    } catch (error) {
        logger.error('Fehler beim Speichern des Caches:', error);
    }
}

// Funktion zum Überprüfen, ob der Cache noch gültig ist
function isCacheValid(cacheTimestamp) {
    const now = Date.now();
    const cacheDate = new Date(cacheTimestamp);

    // Cache ist nur bis Mitternacht gültig
    const currentDate = new Date();
    if (currentDate.getDate() !== cacheDate.getDate()) {
        return false;
    }

    // Cache sollte mindestens jede Minute erneuert werden
    const cacheAgeInMs = now - cacheTimestamp;
    return cacheAgeInMs < 60 * 1000; // 60 Sekunden Cache-Dauer
}

module.exports = { loadCache, saveCache, isCacheValid };
