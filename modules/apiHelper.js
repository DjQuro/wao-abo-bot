const fetch = require('node-fetch');
const logger = require('./logger');
const cacheHelper = require('./cacheHelper');

// Cache-Dauer: Jede Minute wird der Cache überprüft
const CACHE_DURATION = 60 * 1000; // 60 Sekunden in Millisekunden

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

// Funktion zum Abrufen von Shows für mehrere Sender (heute und morgen)
async function fetchShowsForStations(stationIds, config) {
    const cache = await cacheHelper.loadCache();
    const now = Date.now();

    if (cache && cache.timestamp && cacheHelper.isCacheValid(cache.timestamp)) {
        logger.info('Verwende gecachte Show-Daten');
        return cache.data;
    }

    const apiPromises = stationIds.map(stationId => {
        const todayUrl = `${config.apiBaseUrl}/showplan/${stationId}/1`;
        const tomorrowUrl = `${config.apiBaseUrl}/showplan/${stationId}/2`;
        logger.info(`Abrufen von Daten von: ${todayUrl} und ${tomorrowUrl}`);

        return Promise.all([
            fetchShowData(todayUrl).then(shows => shows.map(show => ({ ...show, dateLabel: 'heute' }))),
            fetchShowData(tomorrowUrl).then(shows => shows.map(show => ({ ...show, dateLabel: 'morgen' })))
        ]);
    });

    const allShowData = await Promise.all(apiPromises);
    const flatShowData = allShowData.flat(2);

    // Debugging: Logge die rohen Show-Daten, um zu überprüfen, ob Felder fehlen
    logger.info('Rohe Show-Daten:', JSON.stringify(flatShowData, null, 2));

    await cacheHelper.saveCache({
        timestamp: now,
        data: flatShowData
    });

    return flatShowData;
}



module.exports = { fetchShowData, fetchShowsForStations };
