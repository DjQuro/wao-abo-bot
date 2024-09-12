const { createLogger, format, transports } = require('winston');
const { combine, timestamp, printf, colorize } = format;

// Definiere das Ausgabeformat für das Logging
const logFormat = printf(({ level, message, timestamp }) => {
    return `${timestamp} [${level}]: ${message}`;
});

// Logger-Konfiguration
const logger = createLogger({
    level: 'info',
    format: combine(
        timestamp(),
        logFormat
    ),
    transports: [
        new transports.Console({ format: combine(colorize(), logFormat) }), // Ausgabe in der Konsole
        new transports.File({ filename: 'error.log', level: 'error' }), // Fehlerprotokollierung in Datei
        new transports.File({ filename: 'combined.log' }) // Alle Logs in einer Datei
    ]
});

module.exports = logger;
