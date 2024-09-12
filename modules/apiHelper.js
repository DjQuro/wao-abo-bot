async function fetchShowsForStations(stationIds, config) {
    const cache = await cacheHelper.loadCache();
    const now = Date.now();

    // Überprüfe, ob wir bereits gecachte Daten haben
    if (cache && cache.timestamp && cacheHelper.isCacheValid(cache.timestamp, CACHE_DURATION) && cacheHelper.areShowDataValid(cache.data)) {
        logger.info('Verwende gecachte Show-Daten');
        return cache.data; // Verwende die gecachten Daten
    }

    // Falls keine gültigen Daten im Cache vorhanden sind, API-Anfragen senden
    const apiPromises = stationIds.map(stationId => {
        const apiUrl = `https://api.weareone.fm/v1/showplan/${stationId}/1`;
        return fetchShowData(apiUrl);
    });

    const allShowData = await Promise.all(apiPromises);
    const flatShowData = allShowData.flat();

    // Speichere die Show-Daten im Cache
    await cacheHelper.saveCache({
        timestamp: now,
        data: flatShowData
    });

    return flatShowData;
}
