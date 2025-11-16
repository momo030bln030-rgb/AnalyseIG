# Setup-Assistent für ANALYSE IG

## Überblick

Beim ersten Start von `main.py` wird automatisch ein **interaktiver Setup-Assistent** gestartet, wenn noch keine Konfigurationsdateien vorhanden sind.

## Funktionsweise

Der Setup-Assistent führt Sie durch folgende Schritte:

### Schritt 1: Plattformen auswählen
Sie können auswählen, welche Plattformen Sie nutzen möchten:
- Instagram
- Facebook
- TikTok
- Pinterest
- Tumblr

Für jede ausgewählte Plattform wird eine Konfigurationsdatei erstellt.

### Schritt 2: Allgemeine Einstellungen
Sie können die folgenden Grundeinstellungen konfigurieren:
- **Timeout**: Wartezeit für HTTP-Requests (Standard: 10 Sekunden)
- **Retries**: Anzahl der Wiederholungen bei Fehlern (Standard: 3)
- **Report-Verzeichnis**: Wo Reports gespeichert werden (Standard: ./)
- **Auto-Speichern**: Ob Reports automatisch gespeichert werden (Standard: ja)

### Schritt 3: Plattform-spezifische Einstellungen

#### Instagram
- Zielbenutzer (z.B. "cristiano")
- Maximale Anzahl zu scrapender Posts
- Kommentare auslesen (ja/nein)
- Likes auslesen (ja/nein)

#### Facebook
- Suchbegriff (Personenname)
- Optionaler Suchort
- Posts auslesen (ja/nein)
- Kommentare auslesen (ja/nein)

#### TikTok
- Zielbenutzer
- Maximale Anzahl zu scrapender Videos
- Kommentare auslesen (ja/nein)

#### Pinterest
- Suchbegriff
- Maximale Anzahl zu scrapender Pins
- Kommentare auslesen (ja/nein)

#### Tumblr
- Blog-Name
- Maximale Anzahl zu scrapender Posts
- Kommentare auslesen (ja/nein)

## Konfigurationsdateien

Nach dem Setup finden Sie die erstellten Konfigurationsdateien im `config/`-Verzeichnis:

```
config/
├── instagram_config.json
├── facebook_config.json
├── tiktok_config.json
├── pinterest_config.json
└── tumblr_config.json
```

### Format einer Konfigurationsdatei

```json
{
  "platform": "instagram",
  "created": "2025-11-16T14:01:11.033111",
  "settings": {
    "timeout": 10,
    "retries": 3,
    "save_reports": true,
    "report_dir": "./",
    "target_username": "cristiano",
    "max_posts": 30,
    "get_comments": true,
    "get_likes": true,
    "get_hashtags": true,
    "get_mentions": true,
    "generate_full_report": true
  },
  "output": {
    "format": "json",
    "filename_pattern": "{username}_FULL_REPORT.json"
  }
}
```

## Konfigurationen später bearbeiten

Sie können Konfigurationsdateien jederzeit bearbeiten:

1. Starten Sie `main.py`
2. Wählen Sie **[6] Konfiguration bearbeiten**
3. Wählen Sie die Plattform, deren Konfiguration Sie bearbeiten möchten
4. Die Datei öffnet sich im Standard-Editor

Oder bearbeiten Sie die JSON-Dateien direkt im `config/`-Verzeichnis mit einem Texteditor.

## Automatische Erstellung von Konfigurationen

Wenn Sie in der "Konfiguration bearbeiten"-Option eine Plattform wählen, für die noch keine Konfiguration vorhanden ist, wird automatisch eine Standard-Konfiguration erstellt.

## Fehlerbehandlung

- **Keine Plattformen ausgewählt**: Setup wird abgebrochen
- **Ungültige Eingaben**: Es werden Standardwerte verwendet
- **Fehlende Verzeichnisse**: Werden automatisch erstellt

## Beispiel: Neustart mit Setup

```bash
# Löschen Sie alle Konfigurationsdateien
cd config
rm *_config.json

# Beim nächsten Start wird automatisch das Setup gestartet
python main.py
```

## Tipps

- Alle Eingabefelder unterstützen Standardwerte - drücken Sie einfach Enter, um den Standardwert zu verwenden
- Die Konfigurationen sind im JSON-Format gespeichert und können mit jedem Texteditor bearbeitet werden
- Jede Plattform kann unabhängig konfiguriert werden
