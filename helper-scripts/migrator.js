const fs = require('fs').promises;
const path = require('path');
const logger = require('../modules/logger'); // Pfad zu deinem logger

// Pfade zu den alten Daten
const oldDataPath = path.join(__dirname, '../botold/data');
const djsOldPath = path.join(oldDataPath, '../djs.json'); // Alte DJ-Datenbank

// Neue Pfade
const newDataPath = path.join(__dirname, '../data');
const subsPath = path.join(newDataPath, 'subs.json');
const stationsPath = path.join(newDataPath, 'stations.json');
const djsPath = path.join(newDataPath, 'djs.json');

// Standardstrukturen für das neue System
const defaultSubsStructure = { "chats": {} };
const defaultStationsStructure = { "chats": {} };
const defaultDjsStructure = { "djs": [] };

// Funktion zum Erstellen des Ordners, falls er nicht existiert
async function ensureDataDir() {
    try {
        await fs.mkdir(newDataPath, { recursive: true }); // Erstellt den Ordner, wenn er nicht existiert
        logger.info(`Datenverzeichnis ${newDataPath} wurde erstellt oder existiert bereits.`);
    } catch (error) {
        logger.error(`Fehler beim Erstellen des Datenverzeichnisses: ${error.message}`);
    }
}

// Funktion zum Laden alter Daten
async function loadOldData(filePath) {
    try {
        const data = await fs.readFile(filePath, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        logger.error(`Fehler beim Laden der alten Datei ${filePath}: ${error.message}`);
        return null; // Rückgabe null, wenn Datei nicht existiert
    }
}

// Funktion zum Speichern der neuen Daten
async function saveNewData(filePath, data) {
    try {
        await fs.writeFile(filePath, JSON.stringify(data, null, 2), 'utf8');
        logger.info(`Daten erfolgreich gespeichert in ${filePath}`);
    } catch (error) {
        logger.error(`Fehler beim Speichern der Datei ${filePath}: ${error.message}`);
    }
}

// Indexiere den botold/data Ordner, um die Chat-IDs zu finden
async function indexBotOldFolder() {
    try {
        const chatDirs = await fs.readdir(oldDataPath, { withFileTypes: true });
        const chatIds = chatDirs
            .filter(dirent => dirent.isDirectory()) // Nur Ordner (Chat-IDs)
            .map(dirent => dirent.name); // Namen der Ordner (Chat-IDs)

        return chatIds;
    } catch (error) {
        logger.error(`Fehler beim Indexieren des Ordners ${oldDataPath}: ${error.message}`);
        return [];
    }
}

// Migration der Abonnements, Sender und Benachrichtigungszeit
async function migrateSubscriptionsAndStations(chatId) {
    // Pfade zu den alten Abonnements, Senderdaten und Konfigurationsdaten
    const oldSubsPath = path.join(oldDataPath, `${chatId}/subs.json`);
    const oldStationsPath = path.join(oldDataPath, `${chatId}/stations.json`);
    const oldConfigPath = path.join(oldDataPath, `${chatId}/config.json`);

    const oldSubs = await loadOldData(oldSubsPath);
    const oldStations = await loadOldData(oldStationsPath);
    const oldConfig = await loadOldData(oldConfigPath);

    // Neue Abonnements laden
    const newSubs = await loadOldData(subsPath) || defaultSubsStructure;
    const newStations = await loadOldData(stationsPath) || defaultStationsStructure;

    // Migriere Abonnements
    if (oldSubs && oldSubs.subscriptions) {
        const chatSubs = newSubs.chats[chatId] || { djs: [], notificationTime: 15 };
        chatSubs.djs = oldSubs.subscriptions; // Übernehmen der alten Abonnements

        // Migriere Benachrichtigungszeit aus config.json (minInfo)
        if (oldConfig && oldConfig.minInfo) {
            chatSubs.notificationTime = oldConfig.minInfo;
        }

        newSubs.chats[chatId] = chatSubs;
    }

    // Migriere Sender-Aktivierungen
    if (oldStations && oldStations.stations) {
        const chatStations = newStations.chats[chatId] || { stations: [] };
        chatStations.stations = Object.values(oldStations.stations); // Übernehmen der alten Sender
        newStations.chats[chatId] = chatStations;
    }

    // Speichern der neuen Daten
    await saveNewData(subsPath, newSubs);
    await saveNewData(stationsPath, newStations);
}

// Migration der DJ-Datenbank
async function migrateDjs() {
    const oldDjs = await loadOldData(djsOldPath);
    const newDjs = await loadOldData(djsPath) || defaultDjsStructure;

    if (oldDjs && oldDjs.djs) {
        newDjs.djs = [...new Set([...newDjs.djs, ...oldDjs.djs])]; // Vermeide Duplikate und migriere DJs
    }

    await saveNewData(djsPath, newDjs);
}

// Starte den Migrationsprozess
async function migrateAll() {
    await ensureDataDir();  // Stelle sicher, dass das Datenverzeichnis existiert

    // Chat-IDs aus dem botold/data-Ordner indexieren
    const chatIds = await indexBotOldFolder();

    // Migriere Abonnements, Sender und Benachrichtigungszeit für jeden Chat
    for (const chatId of chatIds) {
        await migrateSubscriptionsAndStations(chatId);
    }

    // Migriere DJs
    await migrateDjs();

    logger.info('Migration abgeschlossen!');
}

migrateAll().catch(error => {
    logger.error(`Fehler bei der Migration: ${error.message}`);
});
