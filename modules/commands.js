const { loadSubsJson, saveJsonFile, loadStationsJson } = require('./cacheHelper');
const path = require('path');

// Abonnements je Chat abrufen
async function getAllSubscriptions() {
    const subs = await loadSubsJson();
    return subs.chats || {};
}

// DJ-Abonnement hinzufügen
async function subscribeDJ(chatId, djName) {
    const subs = await loadSubsJson();
    const chatSubs = subs.chats[chatId] || { djs: [], notificationTime: 15 };
    if (chatSubs.djs.includes(djName)) {
        return `Der DJ ${djName} ist bereits abonniert.`;
    }

    chatSubs.djs.push(djName);
    subs.chats[chatId] = chatSubs;
    await saveJsonFile(path.join(__dirname, '../config/subs.json'), subs);
    return `Der DJ ${djName} wurde erfolgreich abonniert!`;
}

// DJ-Abonnement entfernen
async function unsubscribeDJ(chatId, djName) {
    const subs = await loadSubsJson();
    const chatSubs = subs.chats[chatId] || { djs: [], notificationTime: 15 };
    if (!chatSubs.djs.includes(djName)) {
        return `Der DJ ${djName} ist nicht abonniert.`;
    }

    chatSubs.djs = chatSubs.djs.filter(dj => dj !== djName);
    subs.chats[chatId] = chatSubs;
    await saveJsonFile(path.join(__dirname, '../config/subs.json'), subs);
    return `Der DJ ${djName} wurde erfolgreich abbestellt.`;
}

// Sender aktivieren oder deaktivieren
async function toggleStation(chatId, stationId) {
    const stations = await loadStationsJson();
    const chatStations = stations.chats[chatId] || { stations: [] };
    if (chatStations.stations.includes(stationId)) {
        chatStations.stations = chatStations.stations.filter(station => station !== stationId);
        stations.chats[chatId] = chatStations;
        await saveJsonFile(path.join(__dirname, '../config/stations.json'), stations);
        return `Sender ${stationId} wurde deaktiviert.`;
    } else {
        chatStations.stations.push(stationId);
        stations.chats[chatId] = chatStations;
        await saveJsonFile(path.join(__dirname, '../config/stations.json'), stations);
        return `Sender ${stationId} wurde aktiviert.`;
    }
}

// Benachrichtigungszeit festlegen
async function setNotificationTime(chatId, minutes) {
    const subs = await loadSubsJson();
    const chatSubs = subs.chats[chatId] || { djs: [], notificationTime: 15 };
    chatSubs.notificationTime = minutes;
    subs.chats[chatId] = chatSubs;
    await saveJsonFile(path.join(__dirname, '../config/subs.json'), subs);
    return `Die Benachrichtigungszeit wurde auf ${minutes} Minuten festgelegt.`;
}

// Liste aller abonnierten DJs im Chat ausgeben
async function listSubscribedDJs(chatId) {
    const subs = await loadSubsJson();
    const chatSubs = subs.chats[chatId] || { djs: [] };
    if (chatSubs.djs.length === 0) {
        return `Keine DJs im Chat abonniert.`;
    }

    const sortedDjs = chatSubs.djs.sort();
    const count = sortedDjs.length;
    return `Es sind ${count} DJs abonniert:\n` + sortedDjs.join('\n');
}

module.exports = { getAllSubscriptions, subscribeDJ, unsubscribeDJ, toggleStation, setNotificationTime, listSubscribedDJs };
