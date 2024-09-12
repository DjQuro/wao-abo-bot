const fetch = require('node-fetch');
const logger = require('./logger');
const cacheHelper = require('./cacheHelper');

// Cache-Dauer (z.B. 15 Minuten)
const CACHE_DURATION = 15 * 60 * 1000; // 15 Minuten in Millisekunden

// Funktion zum Abrufen der Show-Daten
async function fetchShowData(apiUrl) {
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error(`Fehler beim Abrufen der API-Daten: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        logger.error(`API-Fehler: ${error.message}`);
        return null;
    }
}

// Funktion zum Abrufen von Shows für mehrere Sender
async function fetchShowsForStations(stationIds, config) {
    const cache = await cacheHelper.loadCache();
    const now = Date.now();

    // Überprüfe, ob wir bereits gecachte Daten haben
    if (cache && cache.timestamp && cacheHelper.isCacheValid(cache.timestamp, CACHE_DURATION)) {
        logger.info('Verwende gecachte Show-Daten');
        return cache.data; // Verwende die gecachten Daten
    }

    // Falls keine gültigen Daten im Cache vorhanden sind, API-Anfragen senden
    const apiPromises = stationIds.map(stationId => {
        const apiUrl = `${config.apiBaseUrl}/showplan/${stationId}/1`;
        logger.info(`Abrufen von Daten von: ${apiUrl}`);
        return fetchShowData(apiUrl);
    });

    const allShowData = await Promise.all(apiPromises);
    const flatShowData = allShowData.flat();

    // Speichere die Show-Daten im Cache
    await cacheHelper.saveCache({
        timestamp: now,
        data: flatShowData
    });

    return flatShowData; // Gebe die neuen Daten zurück
}

module.exports = { fetchShowData, fetchShowsForStations };
