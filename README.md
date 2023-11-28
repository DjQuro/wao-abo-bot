[![Python application](https://github.com/DjQuro/wao-abo-bot/actions/workflows/python-app.yml/badge.svg)](https://github.com/DjQuro/wao-abo-bot/actions/workflows/python-app.yml)
[![Bandit](https://github.com/DjQuro/wao-abo-bot/actions/workflows/bandit.yml/badge.svg)](https://github.com/DjQuro/wao-abo-bot/actions/workflows/bandit.yml)
[![dependency-review](https://github.com/DjQuro/wao-abo-bot/actions/workflows/dependency-review.yml/badge.svg)](https://github.com/DjQuro/wao-abo-bot/actions/workflows/dependency-review.yml)

dependency-review.yml
# We.aRe.oNe Abo Bot
Telegrambot zum abonnieren von DJs der We.aRe.oNe Sendegruppe

Zurzeit verfügbar in Telegram unter https://t.me/wao_announce_bot

Featurerequests und Fehler bitte über die Issue Funktion melden.

# Benötigte Packages (Self-Hosting)
```bash
pip install -r Requirements.txt
```

# Commands
| Befehl | Funktion | Anwendung |
|----------|----------|----------|
| /start  | Erster Befehl zum Anlegen des Datensatzes im Bot (Wird nur einmal benötigt!) In Gruppen nur für Admins | /start  |
| /next  | Welche Sendungen beginnen in den nächsten 15 Minuten? (Bezogen auf ALLE DJs)  | /next |
| /time  | Setzt die Frühste Benachrichtigungszeit in Minuten (Ohne Argument wird diese nur ausgegeben) | /time 30  |
| /announce  | Nur für die ChatID in AdminID - Sendet eine Nachricht an ALLE USER! | /announce Hallo Welt!  |
| /subscribe  | Einen DJ abonnieren. Schreibe den Namen des DJs wie in der WAO App  | /subscribe  |
| /unsubscribe  | Ein Abo beenden.  | /unsubscribe  |
| /subs  | Alle Abos anzeigen.  | /subs /abos /subscriptions  |
| /live  | Abruf der aktuellen Track/Showdaten.  | /live  |
| /stations  | Aktiviert oder Deaktiviert abrufbare Sender.  | /stations  |


# Config (Self-Hosting)
In der Config unter bot_token den Bot Token angeben. Zudem wird für die Verwendung eine AdminID benötigt. Das ist die ChatID des Chats zwischen dem Admin und dem Bot.

# Wo funktioniert der Bot?
Der Bot funktioniert im Privatchat sowie in Gruppen und Supergruppen (Achtung! In Gruppen können /time und /start NUR von Gruppenadmins ausgeführt werden)
Als Ankündigungsbot in einem Channel ist dieser Bot leider nicht nutzbar! Hierfür kann mein Announcer-Bot aus meinem anderen Repository gezogen werden (folgt)

# To Do
- Performance anpassen (Der Abstand zwischen den gesendeten Nachrichten ist teilweise sehr hoch)
- Wir brauchen mehr Gummibären!
- Supportfunktion für Betreiber

