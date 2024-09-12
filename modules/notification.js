const { DateTime } = require("luxon"); // Für Zeitumwandlungen

function sendNotification(show) {
    const showName = show.n;
    const djName = show.m;

    // Zeitstempel korrigieren (Unix-Zeit durch 1000 teilen)
    const startUnix = show.s / 1000;
    const startTime = DateTime.fromSeconds(startUnix).toFormat('HH:mm');

    console.log(`📣 Benachrichtigung: Die Show ${showName} von ${djName} startet um ${startTime}!`);
}

module.exports = { sendNotification };