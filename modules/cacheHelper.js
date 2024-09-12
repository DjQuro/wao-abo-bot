const fs = require('fs').promises;
const path = require('path');

// Datei, in der der Cache gespeichert wird
const cacheFilePath = path.join(__dirname, '../cache/cache.json');

// Funktion zum Laden des Caches
async function loadCache() {
    try {
        const data = await fs.readFile(cacheFilePath, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        return {}; // Falls kein Cache vorhanden ist, leere Daten zurückgeben
    }
}

// Funktion zum Speichern des Caches
async function saveCache(cacheData) {
    try {
        await fs.writeFile(cacheFilePath, JSON.stringify(cacheData, null, 2));
    } catch (error) {
        console.error('Fehler beim Speichern des Caches:', error);
    }
}

// Funktion zum Überprüfen, ob eine Show im Cache vorhanden ist
function isCacheValid(cacheTimestamp, cacheDuration) {
    const now = Date.now();
    return (now - cacheTimestamp) < cacheDuration;
}

module.exports = { loadCache, saveCache, isCacheValid };
