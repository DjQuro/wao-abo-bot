const moment = require('moment-timezone');

// Funktion, die das Logging übernimmt und die Zeit anpasst
function logWithCorrectTime(level, message) {
    // Zeit in der Zeitzone 'Europe/Berlin' formatieren
    const currentTime = moment().tz('Europe/Berlin').format('DD.MM.YYYY - HH:mm:ss');
    // Konsolenausgabe mit Zeit, Log-Level und Nachricht
    console.log(`[${currentTime}] [${level}]: ${message}`);
}

// Exportiere die Info- und Error-Funktionen
module.exports = {
    // Info-Log
    info: (message) => logWithCorrectTime('info', message),

    // Error-Log
    error: (message) => logWithCorrectTime('error', message)
};

