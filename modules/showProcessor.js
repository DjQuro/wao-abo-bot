const { DateTime } = require("luxon"); // Für bessere Zeitumwandlungen

function processShows(showData, config) {
    showData.forEach(show => {
        const showName = show.n;
        const djName = show.m;

        // Zeitstempel korrigieren (Unix-Zeit durch 1000 teilen)
        const startUnix = show.s / 1000;
        const endUnix = show.e / 1000;

        // Start- und Endzeit in lesbares Format umwandeln
        const startTime = DateTime.fromSeconds(startUnix).toFormat('HH:mm');
        const endTime = DateTime.fromSeconds(endUnix).toFormat('HH:mm');

        if (showName && djName) {
            console.log(`Verarbeite Show: ${showName} von ${djName} (Start: ${startTime}, Ende: ${endTime})`);
        } else {
            console.log('Fehler: Show oder DJ ist nicht definiert.');
        }
    });
}

module.exports = { processShows };
