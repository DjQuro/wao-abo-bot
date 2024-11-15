const fs = require('fs').promises;
const path = require('path');
const logger = require('./logger');

// Ordner, in dem die JSON-Dateien gespeichert werden sollen
const dataDir = path.join(__dirname, '../data');

// Standardstrukturen für subs.json, stations.json und djs.json
const defaultSubsStructure = {
    "chats": {}
};

const defaultStationsStructure = {
    "chats": {}
};

const defaultDjsStructure = {
    "djs": []
};

// Funktion zum Erstellen des Ordners, falls er nicht existiert
async function ensureDataDir() {
    try {
        const dirExists = await fs.access(dataDir).then(() => true).catch(() => false);
        if (!dirExists) {
            await fs.mkdir(dataDir, { recursive: true });
            logger.info(`Datenverzeichnis ${dataDir} wurde erstellt.`);
        }
    } catch (error) {
        logger.error(`Fehler beim Erstellen des Datenverzeichnisses: ${error.message}`);
    }
}


// Funktion zum Laden der JSON-Dateien
async function loadJsonFile(filePath, defaultStructure) {
    try {
        const data = await fs.readFile(filePath, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        if (error.code === 'ENOENT') {
            // Datei existiert nicht, erstelle die Datei mit der Standardstruktur
            logger.info(`${filePath} nicht gefunden. Erstelle die Datei mit der Standardstruktur.`);
            await saveJsonFile(filePath, defaultStructure);
            return defaultStructure;
        } else {
            logger.error(`Fehler beim Laden der Datei ${filePath}: ${error.message}`);
            throw error;
        }
    }
}

// Funktion zum Speichern der JSON-Dateien
async function saveJsonFile(filePath, data) {
    try {
        await fs.writeFile(filePath, JSON.stringify(data, null, 2), 'utf8');
        logger.info(`Datei ${filePath} erfolgreich gespeichert.`);
    } catch (error) {
        logger.error(`Fehler beim Speichern der Datei ${filePath}: ${error.message}`);
    }
}

// Beispiel für das Laden der subs.json
async function loadSubsJson() {
    await ensureDataDir();  // Stelle sicher, dass der data-Ordner existiert
    const subsPath = path.join(dataDir, 'subs.json');
    return loadJsonFile(subsPath, defaultSubsStructure);
}

// Beispiel für das Laden der stations.json
async function loadStationsJson() {
    await ensureDataDir();  // Stelle sicher, dass der data-Ordner existiert
    const stationsPath = path.join(dataDir, 'stations.json');
    return loadJsonFile(stationsPath, defaultStationsStructure);
}

// Beispiel für das Laden der djs.json
async function loadDjsJson() {
    await ensureDataDir();  // Stelle sicher, dass der data-Ordner existiert
    const djsPath = path.join(dataDir, 'djs.json');
    return loadJsonFile(djsPath, defaultDjsStructure);
}

// Funktion zum Laden des Caches
async function loadCache() {
    const cacheFilePath = path.join(dataDir, 'cache.json');  // Cache wird auch im data-Ordner gespeichert
    try {
        const data = await fs.readFile(cacheFilePath, 'utf8');
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
    const cacheFilePath = path.join(dataDir, 'cache.json');
    try {
        await fs.writeFile(cacheFilePath, JSON.stringify(cacheData, null, 2));
        //logger.info(`Cache erfolgreich gespeichert: ${cacheFilePath}`);
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

module.exports = { loadCache, saveCache, isCacheValid, loadSubsJson, loadStationsJson, loadDjsJson, saveJsonFile };
