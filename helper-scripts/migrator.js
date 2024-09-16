const fs = require('fs').promises;
const path = require('path');
const logger = require('../modules/logger'); // Pfad zu deinem logger

// Pfade zu den alten Daten
const oldDataPath = path.join(__dirname, '../botold');
const djsOldPath = path.join(oldDataPath, 'djs.json'); // Alte DJ-Datenbank

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

// Migration der Abonnements und Sender
async function migrateSubscriptionsAndStations(chatId) {
    // Alte Abonnements und Sender laden
    const oldSubsPath = path.join(oldDataPath, `${chatId}/subs.json`);
    const oldStationsPath = path.join(oldDataPath, `${chatId}/stations.json`);

    const oldSubs = await loadOldData(oldSubsPath);
    const oldStations = await loadOldData(oldStationsPath);

    // Neue Abonnements laden
    const newSubs = await loadOldData(subsPath) || defaultSubsStructure;
    const newStations = await loadOldData(stationsPath) || defaultStationsStructure;

    // Migriere Abonnements
    if (oldSubs && oldSubs.subscriptions) {
        const chatSubs = newSubs.chats[chatId] || { djs: [], notificationTime: 15 };
        chatSubs.djs = oldSubs.subscriptions; // Übernehmen der alten Abonnements
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

    // Beispiel-Chat-IDs, die migriert werden sollen
    const chatIds = ['318491860', '123456789']; // Diese IDs müssen aus deinen alten Daten kommen

    // Migriere Abonnements und Sender für jeden Chat
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
