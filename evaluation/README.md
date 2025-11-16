# Evaluation Framework

Dieses kleine Framework führt die vorhandenen Scraper-Skripte mehrfach aus, sammelt Laufzeit-Informationen und prüft, ob JSON-Reports erstellt wurden.

Usage:

1. Passe `evaluation/config_sample.json` an (Scripts, Iterationen).
2. Installiere Tracing-Abhängigkeiten (optional):

```powershell
pip install -r ../requirements.txt
```

3. Führe die Evaluation aus:

```powershell
python evaluate.py evaluation/config_sample.json
```

Output: Eine Datei `evaluation_report_<timestamp>.json` im `report_dir` (siehe Config).

Begrenzungen:
- Diese Evaluation ist leichtgewichtig; sie überprüft hauptsächlich, ob Report-Dateien erstellt wurden
- Für tiefergehende Messungen (genauere Extraktions-Qualität) kannst du eigene Metriken in `parse_report`
