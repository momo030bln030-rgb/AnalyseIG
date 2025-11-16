# Facebook & Instagram Scraper Tools - QUICK START GUIDE

## 📁 Übersicht der Skripte

### **INSTAGRAM Tools**
```
1. ig.py                    - Original Instagram Scraper mit Login
2. ig_working.py            - Verbesserte Basis-Version
3. ig_complete.py           - VOLLSTÄNDIGER Scraper (empfohlen)
   └─ Posts, Kommentare, Likes, Hashtags, Erwähnungen, Engagement
```

### **FACEBOOK Tools**
```
1. facebook_analyzer.py      - Basis-Analyzer (Name-Suche + Profil)
2. facebook_advanced_scraper.py - ERWEITERT mit Umgehungstechniken
   └─ Archive.org, Google Cache, Reverse Image Search, Filter-Suche
```

---

## 🚀 SCHNELLSTART

### Instagram - Posts & Kommentare abrufen
```bash
cd c:\Users\MoMo-Bln\Downloads\Music\ig
python ig_complete.py
```
**Dann ändern (Zeile ~365):**
```python
target_username = "cristiano"  # Dein Ziel-Account
```

### Facebook - Profil suchen & analysieren
```bash
python facebook_analyzer.py
```
**Dann ändern (Zeile ~470):**
```python
search_name = "Max Mueller"  # Name zum Suchen
```

### Facebook - FORTGESCHRITTENE ANALYSE
```bash
python facebook_advanced_scraper.py
```
**Nutzt:**
- Archive.org (gelöschte Inhalte)
- Google Cache (ältere Versionen)
- Reverse Image Search
- Erweiterte Filter-Suche

---

## 🎯 ANWENDUNGSBEISPIELE

### Beispiel 1: Instagram-Profil analysieren
```python
from ig_complete import InstagramFullScraper

scraper = InstagramFullScraper()
report = scraper.generate_full_report("instagram")

# Ergebnis: instagram_FULL_REPORT.json
```

### Beispiel 2: Facebook-Person suchen
```python
from facebook_analyzer import FacebookProfileAnalyzer

analyzer = FacebookProfileAnalyzer()
profiles = analyzer.search_person("Max Mueller")

for profile in profiles[:5]:
    print(f"{profile['name']}: {profile['url']}")
```

### Beispiel 3: Gelöschte Facebook-Inhalte wiederherstellen
```python
from facebook_advanced_scraper import AdvancedFacebookScraper

scraper = AdvancedFacebookScraper(use_delays=True)
report = scraper.analyze_profile_advanced("username")

# Archivierte Versionen abrufen
for snapshot in report['archive_org']['snapshots']:
    print(snapshot['url'])
```

### Beispiel 4: Profilbild reverse-suchen
```python
results = scraper.reverse_image_search("https://example.com/image.jpg")

print(results['google_images'])   # Google Images
print(results['tineye'])          # TinEye
print(results['yandex'])          # Yandex Images
```

---

## 📊 WAS WIRD EXTRAHIERT?

### INSTAGRAM
✅ Profildaten (Name, Bio, Follower, Website)
✅ Posts (Text, Likes, Kommentare, Datum)
✅ Kommentare (Autor, Text, Likes)
✅ Likes (Anzahl, Sample Nutzer)
✅ Hashtags (bis zu 50)
✅ Erwähnungen (bis zu 50)
✅ Engagement-Statistiken (Ø Likes, Kommentare, Rate)

### FACEBOOK
✅ Profildaten (Name, Bio, Lokation, Arbeit, Schule)
✅ Posts (teilweise öffentlich)
✅ Kommentare (öffentliche)
✅ Likes (öffentliche)
✅ Erwähnungen
✅ Gelöschte Inhalte (via Archive.org & Google Cache)
✅ Reverse Image Search (Links zu Duplikaten)

---

## ⚙️ KONFIGURATION

### Verzögerungen einstellen (respektful scraping)
```python
scraper = AdvancedFacebookScraper(use_delays=True)  # Aktiviert
scraper = AdvancedFacebookScraper(use_delays=False) # Schnell (risky!)
```

### Proxy verwenden
```python
proxy = {
    'http': 'http://proxy.example.com:8080',
    'https': 'http://proxy.example.com:8080'
}
scraper = AdvancedFacebookScraper(proxy=proxy)
```

### Custom User-Agent
```python
scraper.session.headers.update({
    'User-Agent': 'Your Custom User-Agent'
})
```

---

## 🔍 TECHNIKEN ZUM UMGEHEN VON BLOCKADEN

### 1. Rate Limiting
**Problem:** Zu viele Requests werden blockiert
**Lösung:**
```python
scraper = AdvancedFacebookScraper(use_delays=True)  # Automatische Verzögerung
```

### 2. Private Profile
**Problem:** Private Daten nicht sichtbar
**Lösung:**
- Archive.org für ältere öffentliche Versionen
- Reverse Image Search
- Mit echtem Account scrapen

### 3. IP-Ban
**Problem:** Zu viele Requests von einer IP
**Lösung:**
```python
proxy = {'http': 'socks5://127.0.0.1:9050'}  # Tor oder VPN
scraper = AdvancedFacebookScraper(proxy=proxy)
```

### 4. Gelöschte Inhalte
**Problem:** Seite wurde gelöscht
**Lösung:**
```python
archive_data = scraper.get_from_archive_org("username")
cache_data = scraper.get_from_google_cache("username")
```

---

## 📈 AUSGABE-FORMATE

Alle Reports werden als **JSON-Dateien** gespeichert:

```
instagram_username_FULL_REPORT.json
facebook_username_FULL_REPORT.json
facebook_username_ADVANCED_REPORT.json
```

**Struktur:**
```json
{
  "target": "username",
  "timestamp": "2025-11-16T08:04:11",
  "profile": { ... },
  "posts": [ ... ],
  "comments": [ ... ],
  "engagement": { ... },
  "archive_org": { ... },
  "google_cache": { ... }
}
```

---

## 📚 ABHÄNGIGKEITEN

```bash
pip install requests beautifulsoup4
```

Das ist alles was du brauchst!

---

## ⚠️ LEGALE & ETHISCHE HINWEISE

✅ **ERLAUBT:**
- Öffentliche Daten scrapen
- Archive.org nutzen
- Reverse Image Search
- Zu Bildungszwecken

❌ **NICHT ERLAUBT:**
- Private Nachrichten abrufen
- Passwörter hacken
- Personal Data zu Missbrauch nutzen
- Spam/Phishing
- DSGVO Verletzung

---

## 🆘 FEHLERBEHANDLUNG

### "Status 404" Fehler
```
Profil existiert nicht oder URL falsch
→ Überprüfe Benutzernamen
→ Versuche manuelle URL
```

### "Rate Limit Hit"
```
Zu viele Requests
→ Aktiviere Delays: use_delays=True
→ Nutze Proxy
→ Warte ein paar Stunden
```

### "Private Profile"
```
Kein Zugriff auf private Daten
→ Nutze Archive.org für alte Versionen
→ Versuche Reverse Image Search
→ Mit eigenem Account scrapen
```

---

## 📞 SUPPORT & RESSOURCEN

- **BeautifulSoup Docs:** https://www.crummy.com/software/BeautifulSoup/
- **Requests Docs:** https://requests.readthedocs.io
- **Archive.org API:** https://archive.org/help/wayback_api.php
- **Facebook Privacy:** https://www.facebook.com/privacy

---

## 📝 BEISPIEL-WORKFLOW

```
1. Starte Skript
   python facebook_analyzer.py

2. Eingabe-Name eingeben
   "Max Mueller"

3. Script sucht Profile
   → Findet mehrere Matches

4. Analysiert bestes Match
   → Extrahiert öffentliche Daten
   → Sucht Archive.org
   → Generiert Report

5. Speichert Daten
   → facebook_maxmueller_FULL_REPORT.json

6. Öffne Report
   → Alle Informationen im JSON Format
```

---

**⚖️ Disclaimer: Dieses Tool dient zu Bildungs- und Forschungszwecken. Nutzer sind verantwortlich für die Einhaltung aller lokalen Gesetze und Plattform-ToS.**

Viel Erfolg! 🚀
