# DO NOT USE! NOT FOR PRODUCTION USE! JUST COMPLETE REWORK!

# NICHT FÜR DEN PRODUKTIVEN EINSATZ BESTIMMT! 

Contribution allowed!
Beteiligung erlaubt!

# To Do vor Release von 2.0
- Commandsystem neu Schreiben
- DJ Fetcher Routine neu machen
- Ankündigungen nach Abosystem
- DJ-Channel Integration
- Administration per Webpanel
- Events seitens WAO korrekt ausgeben!
- Testen, Testen, Testen!!!

# EOL der Python-Version
Die aktuelle Version des Bots ist in Python geschrieben! Ich habe mich entschieden den Bot ab jetzt in JS weiter zu entwickeln!
Deshalb wird der Support für die Python-Umgebung zum Release der JS Version eingestellt! Der Wechsel in Produktiv erfolgt nach Planung am 21.12.2024!
Der derzeitige Entwickungsstand kann unter dem Branch 2.0_JS-Rework eingesehen werden!

# We.aRe.oNe Abo Bot
Telegrambot zum abonnieren von DJs der We.aRe.oNe Sendegruppe
Featurerequests und Fehler bitte über die Issue Funktion melden.

# Abhängigkeiten installieren
```bash
npm install
```
# Commands (Noch nicht in 2.0 enthalten)
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