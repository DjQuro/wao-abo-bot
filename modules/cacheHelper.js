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
            return {}; // Falls kein Cache vorhanden ist, leere Daten zur�ckgeben
        } else {
            logger.error('Fehler beim Laden des Caches:', error);
            return {}; // R�ckgabe eines leeren Caches bei Fehler
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

// Funktion zum �berpr�fen, ob der Cache noch g�ltig ist
function isCacheValid(cacheTimestamp, cacheDuration) {
    const now = Date.now();
    return (now - cacheTimestamp) < cacheDuration;
}

module.exports = { loadCache, saveCache, isCacheValid };
