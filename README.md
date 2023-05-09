# We.aRe.oNe Abo Bot
Telegrambot zum abonnieren von DJs der We.aRe.oNe Sendegruppe

Zurzeit verfügbar in Telegram unter https://t.me/wao_announce_bot für den Privatbetrieb oder für den gemeinschaftlichen Austausch unter https://t.me/waoabotest

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
| /subscription  | Eine Liste aller Abos  | /subscription  |
| /subscribe  | Einen DJ abonnieren. Schreibe den Namen des DJs wie in der WAO App  | /subscribe Quro  |
| /unsubscribe  | Ein Abo beenden. Schreibe den Namen des DJs wie in der WAO App  | /unsubscribe Quro  |

# Config (Self-Hosting)
In der Config unter bot_token den Bot Token angeben. Zudem wird für die Verwendung eine AdminID benötigt. Das ist die ChatID des Chats zwischen dem Admin und dem Bot.

# Ausschluss von Sendern (Self-Hosting)
Ist ein Sender im Bot nicht gewünscht, kann dieser aus der stations.json entfernt werden

# Wo funktioniert der Bot?
Der Bot funktioniert im Privatchat sowie in Gruppen und Supergruppen (Achtung! In Gruppen können /time und /start NUR von Gruppenadmins ausgeführt werden)
Als Ankündigungsbot in einem Channel ist dieser Bot leider nicht nutzbar! Hierfür kann mein Announcer-Bot aus meinem anderen Repository gezogen werden (folgt)

# To Do
- Performance anpassen (Der Abstand zwischen den gesendeten Nachrichten ist teilweise sehr hoch)
- Inline Keyboard für /unsubscribe
- Reply basierte Commands
- Häufig abonnierte DJs im Subscribe Commands als Inline Keyboard
- Chatunabhängiger Senderauschschluss (Für Genrebasierte Gruppen)
- Channelabo-Modus (statt DJs werden Sender abonniert)
- Wir brauchen mehr Gummibären!
- Chatunabhängige Benachrichtigungen
- Supportfunktion für Betreiber

