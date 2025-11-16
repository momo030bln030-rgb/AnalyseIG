#!/usr/bin/env python3
"""
Test-Skript für Setup-Assistent
Simuliert Benutzer-Eingaben für Setup
"""

import subprocess
import sys
import os

# Wechsle ins Hauptverzeichnis
os.chdir(r'c:\Users\MoMo-Bln\Downloads\Music\ig')

# Eingaben für Setup (ein zusätzliches Enter am Ende für die input()-Abfrage)
test_inputs = """j
j
j
n
n
10
3
./
j
cristiano
30
j
j
John Doe

j
j
example_user
20
j

"""

print("="*80)
print("SETUP-ASSISTENT TEST".center(80))
print("="*80 + "\n")
print("Starte main.py mit automatischen Test-Eingaben...\n")

# Starte main.py mit Eingaben
process = subprocess.Popen(
    [sys.executable, 'main.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

stdout, stderr = process.communicate(input=test_inputs)

print("OUTPUT:")
print("-" * 80)
print(stdout)

if stderr:
    print("\nERRORS:")
    print("-" * 80)
    print(stderr)

print("\n" + "="*80)
print("TEST ABGESCHLOSSEN".center(80))
print("="*80)

if __name__ == '__main__':
    # Prüfe, ob Configs erstellt wurden (neuer Unterordner)
    config_dir = r'c:\Users\MoMo-Bln\Downloads\Music\ig\Social Media Analyse Tool J+C\config'
    if os.path.exists(config_dir):
        configs = [f for f in os.listdir(config_dir) if f.endswith('_config.json')]
        print(f"\n[OK] {len(configs)} Konfigurationsdatei(en) erstellt:")
        for config in configs:
            print(f"  [+] {config}")
    else:
        print("\n[!] Config-Verzeichnis nicht gefunden")
