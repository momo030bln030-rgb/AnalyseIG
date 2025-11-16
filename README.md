# Social Media Analyse Tool J+C

Ein Sammlung von Python-Skripten zur Analyse von Social-Media-Profilen (Instagram, Facebook, TikTok, u.a.).

## ⚠️ Wichtige Hinweise

- **Rechtliche Warnung**: Dieses Skript dient zu Bildungszwecken. Unbefugter Zugriff auf private Accounts ist illegal.
- **Instagram Anti-Scraping**: Instagram blockiert aktiv automatisierte Zugriffe, weshalb die Datenextraktion eingeschränkt ist.
- **IP-Bans**: Zu viele Anfragen können zu IP-Bans führen.

## Installation

```bash
pip install requests beautifulsoup4
```

## Verwendung

### Option 1: Interaktives Menü (empfohlen)
```bash
python main.py
```
Hauptmenü mit Optionen für alle Plattformen.

### Option 2: Spezifische Tools

**Instagram Version 1 - Original (`ig.py`):**
```bash
python platforms/instagram/ig.py
```
- Verwendet Web-Scraping und Regex-Extraktion
- Braucht keine Authentifizierung
- Funktioniert für öffentliche Profile

**Instagram Version 2 - Verbessert (`ig_working.py`):**
```bash
python platforms/instagram/ig_working.py
```
- Besseres Error-Handling
- Detaillierte Reports
- Speichert Ergebnisse als JSON

**Instagram Version 3 - Complete (`ig_complete.py`):**
```bash
python platforms/instagram/ig_complete.py
```
- Umfassende Profile & Posts
- Advanced Datenextraktion
- Beste Ergebnisse

## Was wird extrahiert?

- ✓ Profilname & Benutzername
- ✓ Follower/Following Count
- ✓ Anzahl der Posts
- ✓ Verifikationsstatus
- ✓ Bio & Website
- ✓ User ID
- ⚠️ Posts (eingeschränkt wegen Instagram Anti-Scraping)
- ⚠️ Follower-Details (eingeschränkt)

## Beispiel

```python
from platforms.instagram.ig_working import InstagramInvestigator

investigator = InstagramInvestigator()
report = investigator.generate_full_report("instagram")
```

## Ausgabe

Der Report wird in der Konsole angezeigt und als JSON-Datei gespeichert:
```
nineeety.fivee_report.json
```

## Begrenzu ngen

Instagram hat starke Schutzmaßnahmen gegen Web-Scraping eingeführt:
- Daten aus der HTML-Seite sind oft leer
- GraphQL API erfordert spezielle Header
- Private Accounts sind nicht zugänglich
- Rate Limiting ist aktiv

## Alternativen

- **Offizielle Instagram Graph API**: Benötigt Autorisierung
- **Instagram Business API**: Für Business-Accounts
- **Instagrapi Library**: Fortgeschrittenere Scraping-Methode

## Disclaimer

Dieses Projekt dient nur zu Bildungs- und Forschungszwecken. Stelle sicher, dass du alle geltenden Gesetze einhältst.
