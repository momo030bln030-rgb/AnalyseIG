# Facebook Profile Analyzer - Umgehungstechniken & Best Practices

## 🔍 WIE MAN FACEBOOK-DATEN EXTRAHIERT

### 1. OFFIZIELLE WEGE (Empfohlen & Legal)
- **Facebook Graph API**: Offizielle API mit Genehmigung
- **Browser DevTools**: Manuelles Abrufen öffentlicher Daten
- **Öffentliche Seiten**: Posts von Seiten/Unternehmungen

### 2. WEB-SCRAPING METHODEN

#### Methode A: HTML-Parsing (Browser-Sichtweise)
```python
# Extrahiert HTML-Inhalt von öffentlichen Seiten
- Profil-Name aus <title> Tag
- Bio aus Meta-Beschreibung
- Posts aus HTML-Struktur
- Kommentare (teilweise sichtbar)
```

#### Methode B: Regex-Extraktion
```python
# Findet Daten in JavaScript/JSON
- Profil-ID: "_profile_id_"
- Namen in Variablen
- Post-IDs und Inhalte
- Engagement-Statistiken
```

### 3. PRIVATE PROFILE UMGEHEN (Grenzen)

❌ **Was NICHT möglich ist:**
- Private Nachrichten abrufen
- Vollständig private Posts sehen
- Passwort hacken
- Session-Cookies stehlen (modern unmöglich)

✅ **Was MÖGLICH ist:**
- Öffentliche Daten von Friend-Listen
- Archivierte Daten (Google Cache, Archive.org)
- Gelöschte Inhalte (cached versions)
- Öffentliche Kommentare

## 📊 DATEN EXTRAHIEREN - TECHNIKEN

### Technique 1: Browser Automation (Selenium)
```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.facebook.com/username")
# Login möglich
html = driver.page_source
# Extrahiere Daten
```

**Vorteil**: Funktioniert mit JavaScript
**Nachteil**: Langsam, zu viele Detektionen

### Technique 2: Request-Headers Manipulation
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'text/html,application/json',
    'Accept-Language': 'de-DE,de;q=0.9',
    'Cookie': 'locale=de_DE'  # Lokalisierung
}
# Mimikry eines echten Browsers
```

### Technique 3: GraphQL Queries (Insider-Wissen)
```
Facebook nutzt interne GraphQL Endpoints:
- /graphql/ (Primary)
- /graphql_batch/ (Batch Requests)

Beispiel Query:
{
  user(id: "USER_ID") {
    name
    profile_picture
    bio
    friends
  }
}
```

### Technique 4: Google Cache & Archive.org
```python
# Für gelöschte Inhalte:
google_cache = f"http://webcache.googleusercontent.com/cache:{facebook_url}"
wayback = f"https://web.archive.org/web/*/{facebook_url}"

# Enthält ältere Versionen des Profils
```

### Technique 5: Reverse Image Search
```python
# Finde Profil-Bilder auf anderen Plattformen
- Google Images
- TinEye
- Yandex Images
# Oft sind die gleichen Bilder auf anderen Seiten
```

## 🎯 NAME-SUCHE STRATEGIEN

### 1. Standardsuche
```
Name: "Max Mueller"
```

### 2. Mit Zusatzinformationen
```
Name: "Max Mueller" Lokation: "Berlin" Alter: "25-35"
Name: "Max Mueller" Arbeit: "Google" Schule: "TU Berlin"
```

### 3. Umgekehrte Suche
```
Email → Facebook
Telefon → Facebook
Profilbild → Google Reverse Image
User-ID → Facebook URL rekonstruieren
```

### 4. Benutzernamen-Generierung
```
Muster:
- firstname.lastname (max.mueller)
- firstname_lastname (max_mueller)
- firstnamelastname (maxmueller)
- firstname.lastname.123 (max.mueller.123)
- f.lastname (m.mueller)

Dann systematisch testen
```

## 🚫 FACEBOOK ANTI-SCRAPING MASSNAHMEN

### 1. Rate Limiting
```
Problem: Max 50 Requests pro Minute wird blockiert
Lösung: 
- Delays zwischen Requests (2-5 Sekunden)
- Rotating User-Agents
- IP-Rotation (VPN, Proxy)
```

### 2. JavaScript Rendering
```
Problem: Inhalte laden dynamisch
Lösung:
- Selenium/Playwright für JS-Rendering
- HeadlessBrowser
```

### 3. Login-Anforderung
```
Problem: Private Profile nur mit Login sichtbar
Lösung:
- Mit gültigem Account scrapen (bei Einhaltung der ToS)
- Account-Farming (nicht empfohlen)
```

## 💡 BEST PRACTICES - LEGAL & ETHISCH

### ✅ ERLAUBT:
1. **Öffentliche Daten** scrapen (Posts, öffentliche Profile)
2. **Archive.org** nutzen für ältere Inhalte
3. **Google Cache** abrufen
4. **Reverse Image Search**
5. **Daten zu Bildungszwecken** sammeln
6. **Mit Account** scrapen (dich selbst) - wenn in ToS erlaubt

### ❌ NICHT ERLAUBT:
1. **Private Nachrichten** abrufen
2. **Passwörter** hacken
3. **Cookies/Sessions** stehlen
4. **Persönliche Daten** missbrauchen
5. **DSGVO-Verletzung** (EU-Recht)
6. **Mass-Scraping** ohne Genehmigung
7. **Spam/Phishing** mit Daten

## 🛠️ WERKZEUGE ZUM UMGEHEN

### 1. VPN/Proxy
```
- Vermeidet IP-Bans
- Verändert Geo-Location
- Tools: ExpressVPN, NordVPN, Tor
```

### 2. Rotating User-Agents
```python
import random
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
    'Mozilla/5.0 (X11; Linux x86_64)'
]
headers['User-Agent'] = random.choice(user_agents)
```

### 3. Request Delays
```python
import time
time.sleep(random.uniform(2, 5))  # Zufälliger Delay
```

### 4. Proxy Rotation
```python
proxies = {
    'http': 'http://proxy1.com:8080',
    'https': 'http://proxy2.com:8080'
}
response = requests.get(url, proxies=proxies)
```

### 5. Browser Fingerprinting
```
Verstecke dich als echter Browser:
- Echte User-Agent
- Realistische Request-Header
- Cookies aktualisieren
- JavaScript aktivieren
```

## 📈 ERWEITERTE TECHNIKEN

### 1. Account-basiertes Scraping
```python
# Mit echtem Facebook-Account
session = FacebookSession(username, password)
profile = session.get_profile(profile_id)
# Viel mehr Zugriff auf private Daten
# ABER: Verstößt gegen Facebook ToS
```

### 2. API Reverse Engineering
```
1. Facebook-Seite öffnen
2. DevTools → Network Tab
3. API-Calls beobachten
4. GraphQL Queries extrahieren
5. Nachbauen in Python
```

### 3. Paralleles Scraping
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(scrape_profile, profile_ids)
# Schneller aber SEHR auffällig
```

## ⚠️ SICHERHEIT & RISIKEN

### Account-Ban Risiko
- Mass-Scraping → Account Ban
- API Missbrauch → Permanenter Ban
- Lösung: Langsam scrapen, Delays nutzen

### IP-Ban
- Zu viele Requests → IP-Ban
- Lösung: VPN, Proxy-Rotation

### Rechtliche Konsequenzen
- DSGVO Verletzung: 50.000€ Geldbuße+
- Hacking-Vorwurf: Strafverfolgung
- Datenmissbrauch: Zivilklage

## 🎓 TUTORIAL - PROFIL ANALYSIEREN

```bash
# 1. Skript starten
python facebook_analyzer.py

# 2. Im Code ändern:
search_name = "Max Mueller"  # Suche nach Name

# 3. Output:
# - facebook_USER_FULL_REPORT.json (Report)
# - Profildaten, Posts, Kommentare
# - Namen, Erwähnungen
# - Gelöschte Inhalte Analysis

# 4. Weitere Analysen
analyzer = FacebookProfileAnalyzer()
profiles = analyzer.search_person("Max Mueller")
for profile in profiles:
    report = analyzer.generate_full_report(profile['id'])
```

## 📚 RESSOURCEN

- **Facebook Graph API Docs**: https://developers.facebook.com/docs/graph-api
- **Archive.org**: https://web.archive.org
- **BeautifulSoup**: https://www.crummy.com/software/BeautifulSoup/
- **Requests**: https://requests.readthedocs.io

---

**⚖️ Disclaimer**: Dieses Tool dient zu Bildungszwecken. Einhaltung aller lokalen Gesetze ist erforderlich!
