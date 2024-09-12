const fetch = require('node-fetch');
const { exec } = require('child_process');
const fs = require('fs').promises;

// Funktion zum Laden der aktuellen Version
async function loadLocalVersion(filePath) {
    try {
        const data = await fs.readFile(filePath, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error('Fehler beim Laden der lokalen Version:', error);
        throw error;
    }
}

// Funktion zum �berpr�fen, ob ein Update verf�gbar ist
async function checkForUpdate(versionUrl, localVersionPath) {
    try {
        const response = await fetch(versionUrl);
        if (!response.ok) {
            throw new Error(`Fehler beim Abrufen der Version: ${response.status}`);
        }

        const remoteVersion = await response.json();
        const localVersion = await loadLocalVersion(localVersionPath);

        if (remoteVersion.bcl !== localVersion.bcl) {
            console.log("Neues Update verf�gbar!");
            return true;
        } else {
            console.log("Keine Updates verf�gbar.");
            return false;
        }
    } catch (error) {
        console.error('Fehler beim �berpr�fen auf Updates:', error);
        return false;
    }
}

// Funktion zum Ausf�hren des Updates
async function updateSystem() {
    exec('git pull', (error, stdout, stderr) => {
        if (error) {
            console.error(`Fehler beim Aktualisieren: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`Fehlerausgabe beim Aktualisieren: ${stderr}`);
            return;
        }
        console.log(`Aktualisierung erfolgreich: ${stdout}`);
    });
}

module.exports = { checkForUpdate, updateSystem };