# We.aRe.oNe Abo Bot
Telegrambot zum abonnieren von DJs der We.aRe.oNe Sendegruppe

# Benötigte Packages
```bash
pip install Requests
pip install python-telegram-bot
```

# Commands
| Befehl | Funktion | Anwendung |
|----------|----------|----------|
| /start  | Erster Befehl zum Anlegen des Datensatzes im Bot (Wird nur einmal benötigt!) In Gruppen nur für Admins | /start  |
| /next  | Welche Sendungen beginnen in den nächsten 15 Minuten? (Bezogen auf ALLE DJs)  | /next |
| /time  | Setzt die Frühste Benachrichtigungszeit in Minuten (Ohne Argument wird diese nur ausgegeben) | /time 30  |
| /announce  | Nur für die ChatID in AdminID  | /announce Hallo Welt!  |
| /subscription  | Eine Liste aller Abos  | /subscription  |
| /subscribe  | Einen DJ abonnieren. Schreibe den Namen des DJs wie in der WAO App  | /subscribe Quro  |
| /unsubscribe  | Ein Abo beenden. Schreibe den Namen des DJs wie in der WAO App  | /unsubscribe Quro  |

# Config
In der Config unter bot_token den Bot Token angeben

# Ausschluss von Sendern
Ist ein Sender im Bot nicht gewünscht, kann dieser aus der stations.json entfernt werden
