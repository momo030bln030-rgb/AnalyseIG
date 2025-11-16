import sys
import os
import subprocess
import json

INSTAGRAM_SCRIPTS = [
    'ig.py',
    'ig_complete.py',
    'ig_working.py',
    'ig_full_scraper.py'
]
FACEBOOK_SCRIPTS = [
    'facebook_analyzer.py',
    'facebook_advanced_scraper.py'
]
THREADS_SCRIPTS = [
    'threads_scraper.py'
]

PLATFORMS = {
    'instagram': INSTAGRAM_SCRIPTS,
    'facebook': FACEBOOK_SCRIPTS,
    'threads': THREADS_SCRIPTS
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def select_platform():
    print("\nWelche Plattform möchtest du analysieren?")
    print("1: Instagram")
    print("2: Facebook")
    print("3: Threads")
    print("4: Evaluation-Config erstellen")
    print("0: Beenden")
    choice = input("Auswahl: ").strip()
    return choice


def run_script(platform, script):
    script_path = os.path.join(BASE_DIR, platform, script)
    if not os.path.exists(script_path):
        print(f"[!] Script nicht gefunden: {script_path}")
        return
    print(f"[RUN] Starte {script_path} ...")
    subprocess.run([sys.executable, script_path])


def create_evaluation_config():
    config = {
        "workspace": "..",
        "report_dir": "..",
        "iterations": 1,
        "targets": [
            {"label": "Instagram Complete", "script": "instagram/ig_complete.py", "args": []},
            {"label": "Facebook Analyzer", "script": "facebook/facebook_analyzer.py", "args": []},
            {"label": "Threads Scraper", "script": "threads/threads_scraper.py", "args": []}
        ]
    }
    filename = os.path.join(BASE_DIR, "evaluation", "config_sample.json")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"[OK] Evaluation-Config gespeichert: {filename}")


def main():
    while True:
        choice = select_platform()
        if choice == "1":
            print("\nInstagram-Skripte:")
            for i, script in enumerate(INSTAGRAM_SCRIPTS, 1):
                print(f"{i}: {script}")
            idx = input("Skript auswählen (Nummer): ").strip()
            if idx.isdigit() and 1 <= int(idx) <= len(INSTAGRAM_SCRIPTS):
                run_script("instagram", INSTAGRAM_SCRIPTS[int(idx)-1])
        elif choice == "2":
            print("\nFacebook-Skripte:")
            for i, script in enumerate(FACEBOOK_SCRIPTS, 1):
                print(f"{i}: {script}")
            idx = input("Skript auswählen (Nummer): ").strip()
            if idx.isdigit() and 1 <= int(idx) <= len(FACEBOOK_SCRIPTS):
                run_script("facebook", FACEBOOK_SCRIPTS[int(idx)-1])
        elif choice == "3":
            print("\nThreads-Skripte:")
            for i, script in enumerate(THREADS_SCRIPTS, 1):
                print(f"{i}: {script}")
            idx = input("Skript auswählen (Nummer): ").strip()
            if idx.isdigit() and 1 <= int(idx) <= len(THREADS_SCRIPTS):
                run_script("threads", THREADS_SCRIPTS[int(idx)-1])
        elif choice == "4":
            create_evaluation_config()
        elif choice == "0":
            print("Beende...")
            break
        else:
            print("Ungültige Auswahl!")

if __name__ == "__main__":
    main()
