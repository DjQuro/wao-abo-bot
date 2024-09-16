const { loadSubsJson, saveJsonFile, loadStationsJson } = require('./cacheHelper');
const path = require('path');

// DJ-Abonnement-Management
async function subscribeDJ(chatId, djName) {
    console.log(`subscribeDJ aufgerufen für ChatID: ${chatId} und DJ: ${djName}`);
    const subs = await loadSubsJson();
    console.log(`subs.json geladen: ${JSON.stringify(subs)}`);

    const chatSubs = subs.chats[chatId] || { djs: [], notificationTime: 15 };
    if (chatSubs.djs.includes(djName)) {
        return `Der DJ ${djName} ist bereits abonniert.`;
    }

    chatSubs.djs.push(djName);
    subs.chats[chatId] = chatSubs;
    await saveJsonFile(path.join(__dirname, '../config/subs.json'), subs);
    console.log(`subs.json gespeichert: ${JSON.stringify(subs)}`);
    return `Der DJ ${djName} wurde erfolgreich abonniert!`;
}

// Befehl /unsubscribe für das Entfernen eines DJ-Abos
async function unsubscribeDJ(chatId, djName) {
    console.log(`unsubscribeDJ aufgerufen für ChatID: ${chatId} und DJ: ${djName}`);
    const subs = await loadSubsJson();
    console.log(`subs.json geladen: ${JSON.stringify(subs)}`);

    const chatSubs = subs.chats[chatId] || { djs: [], notificationTime: 15 };
    if (!chatSubs.djs.includes(djName)) {
        return `Der DJ ${djName} ist nicht abonniert.`;
    }

    chatSubs.djs = chatSubs.djs.filter(dj => dj !== djName);
    subs.chats[chatId] = chatSubs;
    await saveJsonFile(path.join(__dirname, '../config/subs.json'), subs);
    console.log(`subs.json gespeichert: ${JSON.stringify(subs)}`);
    return `Der DJ ${djName} wurde erfolgreich abbestellt.`;
}

// Sender-Verwaltung
async function toggleStation(chatId, stationId) {
    const stations = await loadStationsJson();
    const chatStations = stations.chats[chatId] || { stations: [] };
    if (chatStations.stations.includes(stationId)) {
        chatStations.stations = chatStations.stations.filter(station => station !== stationId);
        stations.chats[chatId] = chatStations;
        await saveJsonFile(path.join(__dirname, 'stations.json'), stations);
        return `Sender ${stationId} wurde deaktiviert.`;
    } else {
        chatStations.stations.push(stationId);
        stations.chats[chatId] = chatStations;
        await saveJsonFile(path.join(__dirname, 'stations.json'), stations);
        return `Sender ${stationId} wurde aktiviert.`;
    }
}

// Benachrichtigungszeit setzen
async function setNotificationTime(chatId, minutes) {
    const subs = await loadSubsJson();
    const chatSubs = subs.chats[chatId] || { djs: [], notificationTime: 15 };
    chatSubs.notificationTime = minutes;
    subs.chats[chatId] = chatSubs;
    await saveJsonFile(path.join(__dirname, 'subs.json'), subs);
    return `Die Benachrichtigungszeit wurde auf ${minutes} Minuten festgelegt.`;
}

module.exports = { subscribeDJ, unsubscribeDJ, toggleStation, setNotificationTime };
