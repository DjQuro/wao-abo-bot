# Wao Abo Bot
Telegrambot zum abonnieren von DJs der We.aRe.oNe Sendegruppe

# Benötigte Packages
```bash
pip install Requests
pip install python-telegram-bot
```

# Commands
/start - Erster Befehl zum Anlegen des Datensatzes im Bot (Wird nur einmal benötigt!)
/subscribe <DJ> - Einen DJ abonnieren. Schreibe den Namen des DJs wie in der WAO App
/unsubscribe <DJ>- Ein Abo beenden. Schreibe den Namen des DJs wie in der WAO App
/subscription - Eine Liste aller Abos
/next - Welche Sendungen beginnen in den nächsten 15 Minuten? (Bezogen auf ALLE DJs)

# Config
In der Config unter bot_token den Bot Token angeben

# Ausschluss von Sendern
Ist ein Sender im Bot nicht gewünscht, kann dieser aus der stations.json entfernt werden
