#!/usr/bin/env python3
"""
================================================================================
ANALYSE IG - Hauptmenü
Instagram, Facebook, Threads & TikTok Scraper mit Konfiguration
================================================================================
"""

import os
import sys
import json
import runpy
from datetime import datetime

# Verzeichnis-Struktur
MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
PLATFORMS_DIR = os.path.join(MAIN_DIR, 'platforms')
INSTAGRAM_DIR = os.path.join(PLATFORMS_DIR, 'instagram')
FACEBOOK_DIR = os.path.join(PLATFORMS_DIR, 'facebook')
THREADS_DIR = os.path.join(PLATFORMS_DIR, 'tiktok')
PINTEREST_DIR = os.path.join(PLATFORMS_DIR, 'pinterest')
TUMBLR_DIR = os.path.join(PLATFORMS_DIR, 'tumblr')
CONFIG_DIR = os.path.join(MAIN_DIR, 'config')
LIB_DIR = os.path.join(MAIN_DIR, 'lib')

# Ensure lib ist im sys.path
if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)

class SetupWizard:
    """Setup-Assistent für Erstkonfiguration"""
    
    def __init__(self):
        print("\n" + "="*80)
        print("WILLKOMMEN BEI ANALYSE IG - SETUP-ASSISTENT".center(80))
        print("="*80 + "\n")
        print("Es wurden keine Konfigurationen gefunden.")
        print("Lass uns die wichtigsten Einstellungen konfigurieren!\n")
    
    def run_setup(self):
        """Führt den Setup-Assistenten aus"""
        print("="*80)
        print("SCHRITT 1: PLATTFORMEN AUSWÄHLEN".center(80))
        print("="*80)
        print("\nWelche Plattformen möchtest du nutzen? (Mehrfachauswahl möglich)\n")
        
        platforms = {
            '1': 'instagram',
            '2': 'facebook',
            '3': 'tiktok',
            '4': 'pinterest',
            '5': 'tumblr'
        }
        
        selected_platforms = []
        
        for key, platform in platforms.items():
            choice = input(f"Möchtest du {platform.upper()} nutzen? (j/n): ").strip().lower()
            if choice in ['j', 'ja', 'yes', 'y']:
                selected_platforms.append(platform)
                print(f"[+] {platform.upper()} ausgewählt\n")
            else:
                print(f"[-] {platform.upper()} übersprungen\n")
        
        if not selected_platforms:
            print("[!] Du hast keine Plattformen ausgewählt. Setup abgebrochen.")
            return False
        
        print("\n" + "="*80)
        print("SCHRITT 2: ALLGEMEINE EINSTELLUNGEN".center(80))
        print("="*80 + "\n")
        
        timeout = input("Timeout für Requests (Standard: 10 Sekunden): ").strip() or "10"
        retries = input("Anzahl Wiederholungen bei Fehler (Standard: 3): ").strip() or "3"
        report_dir = input("Verzeichnis für Reports (Standard: ./): ").strip() or "./"
        save_reports = input("Reports automatisch speichern? (j/n, Standard: j): ").strip().lower() or "j"
        
        general_config = {
            'timeout': int(timeout),
            'retries': int(retries),
            'save_reports': save_reports in ['j', 'ja', 'yes', 'y'],
            'report_dir': report_dir
        }
        
        # Erstelle Konfigurationen für ausgewählte Plattformen
        print("\n" + "="*80)
        print("SCHRITT 3: PLATTFORM-SPEZIFISCHE EINSTELLUNGEN".center(80))
        print("="*80 + "\n")
        
        for platform in selected_platforms:
            self.setup_platform(platform, general_config)
        
        print("\n" + "="*80)
        print("[OK] SETUP ABGESCHLOSSEN!".center(80))
        print("="*80)
        print(f"\nEs wurden Konfigurationen für {len(selected_platforms)} Plattform(en) erstellt:")
        for platform in selected_platforms:
            print(f"  [+] {platform.upper()}")
        print("\nDu kannst diese jederzeit über das Konfigurationsmenü anpassen.\n")
        
        return True
    
    def setup_platform(self, platform, general_config):
        """Setup für einzelne Plattform"""
        print(f"\n{'='*80}")
        print(f"{platform.upper()} KONFIGURATION".center(80))
        print(f"{'='*80}\n")
        
        config_data = {
            'platform': platform,
            'created': datetime.now().isoformat(),
            'settings': general_config.copy()
        }
        
        if platform == 'instagram':
            print("Instagram-spezifische Einstellungen:")
            username = input("  Zielbenutzer (Standard: cristiano): ").strip() or "cristiano"
            max_posts = input("  Maximale Posts zum Scrapen (Standard: 30): ").strip() or "30"
            get_comments = input("  Kommentare auslesen? (j/n, Standard: j): ").strip().lower() or "j"
            get_likes = input("  Likes auslesen? (j/n, Standard: j): ").strip().lower() or "j"
            
            config_data['settings'].update({
                'target_username': username,
                'max_posts': int(max_posts),
                'get_comments': get_comments in ['j', 'ja', 'yes', 'y'],
                'get_likes': get_likes in ['j', 'ja', 'yes', 'y'],
                'get_hashtags': True,
                'get_mentions': True,
                'generate_full_report': True
            })
        
        elif platform == 'facebook':
            print("Facebook-spezifische Einstellungen:")
            search_name = input("  Personenname zum Suchen (Standard: John Doe): ").strip() or "John Doe"
            search_location = input("  Ort (optional, leer lassen zum Überspringen): ").strip() or None
            get_posts = input("  Posts auslesen? (j/n, Standard: j): ").strip().lower() or "j"
            get_comments = input("  Kommentare auslesen? (j/n, Standard: j): ").strip().lower() or "j"
            
            config_data['settings'].update({
                'search_name': search_name,
                'search_location': search_location,
                'get_posts': get_posts in ['j', 'ja', 'yes', 'y'],
                'get_comments': get_comments in ['j', 'ja', 'yes', 'y'],
                'get_deleted_analysis': True,
                'max_search_results': 20,
                'max_posts': 20,
                'max_comments': 20,
                'generate_full_report': True
            })
        
        elif platform == 'tiktok':
            print("TikTok-spezifische Einstellungen:")
            username = input("  Zielbenutzer (Standard: example_user): ").strip() or "example_user"
            max_videos = input("  Maximale Videos zum Scrapen (Standard: 20): ").strip() or "20"
            get_comments = input("  Kommentare auslesen? (j/n, Standard: j): ").strip().lower() or "j"
            
            config_data['settings'].update({
                'target_username': username,
                'max_videos': int(max_videos),
                'get_comments': get_comments in ['j', 'ja', 'yes', 'y'],
                'get_likes': True,
                'get_shares': True,
                'generate_full_report': True
            })
        
        elif platform == 'pinterest':
            print("Pinterest-spezifische Einstellungen:")
            search_query = input("  Suchbegriff (Standard: design): ").strip() or "design"
            max_pins = input("  Maximale Pins zum Scrapen (Standard: 20): ").strip() or "20"
            get_comments = input("  Kommentare auslesen? (j/n, Standard: j): ").strip().lower() or "j"
            
            config_data['settings'].update({
                'search_query': search_query,
                'max_pins': int(max_pins),
                'get_comments': get_comments in ['j', 'ja', 'yes', 'y'],
                'get_likes': True,
                'get_board_info': True,
                'generate_full_report': True
            })
        
        elif platform == 'tumblr':
            print("Tumblr-spezifische Einstellungen:")
            blog_name = input("  Blog-Name (Standard: example_blog): ").strip() or "example_blog"
            max_posts = input("  Maximale Posts zum Scrapen (Standard: 20): ").strip() or "20"
            get_comments = input("  Kommentare auslesen? (j/n, Standard: j): ").strip().lower() or "j"
            
            config_data['settings'].update({
                'blog_name': blog_name,
                'max_posts': int(max_posts),
                'get_comments': get_comments in ['j', 'ja', 'yes', 'y'],
                'get_likes': True,
                'get_reblogs': True,
                'generate_full_report': True
            })
        
        config_data['output'] = {
            'format': 'json',
            'filename_pattern': self._get_filename_pattern(platform)
        }
        
        # Speichere Konfiguration
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
        
        config_file = os.path.join(CONFIG_DIR, f'{platform}_config.json')
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Konfiguration für {platform.upper()} gespeichert\n")
    
    def _get_filename_pattern(self, platform):
        """Gibt das Dateinamen-Pattern für die Plattform zurück"""
        patterns = {
            'instagram': '{username}_FULL_REPORT.json',
            'facebook': 'facebook_{profile_id}_FULL_REPORT.json',
            'tiktok': '{username}_tiktok_FULL_REPORT.json',
            'pinterest': '{query}_pinterest_FULL_REPORT.json',
            'tumblr': '{blog_name}_tumblr_FULL_REPORT.json'
        }
        return patterns.get(platform, '{username}_FULL_REPORT.json')


class MainMenu:
    """Hauptmenü für alle Plattformen"""
    
    def __init__(self):
        self.running = True
        print("\n" + "="*80)
        print("ANALYSE IG - Hauptmenü".center(80))
        print("="*80 + "\n")
    
    def show_menu(self):
        """Zeigt das Hauptmenü"""
        print("\n" + "="*80)
        print("PLATTFORM AUSWAHL".center(80))
        print("="*80)
        print("\n[1] Instagram")
        print("[2] Facebook")
        print("[3] TikTok")
        print("[4] Pinterest")
        print("[5] Tumblr")
        print("[6] Konfiguration bearbeiten")
        print("[7] Beenden")
        print("\n" + "-"*80)
        
        choice = input("Wähle eine Option (1-7): ").strip()
        return choice
    
    def instagram_menu(self):
        """Instagram-Submenu"""
        print("\n" + "="*80)
        print("INSTAGRAM TOOLS".center(80))
        print("="*80)
        print("\n[1] Vollständiger Profil-Report (ig_complete.py)")
        print("[2] Schneller Scraper (ig.py)")
        print("[3] Arbeitender Scraper (ig_working.py)")
        print("[4] Voller Scraper (ig_full_scraper.py)")
        print("[5] Mit Tracing ausführen")
        print("[6] Zurück")
        print("\n" + "-"*80)
        
        choice = input("Wähle ein Tool (1-6): ").strip()
        return choice
    
    def facebook_menu(self):
        """Facebook-Submenu"""
        print("\n" + "="*80)
        print("FACEBOOK TOOLS".center(80))
        print("="*80)
        print("\n[1] Profil-Analysator (facebook_analyzer.py)")
        print("[2] Erweiterter Scraper (facebook_advanced_scraper.py)")
        print("[3] Mit Tracing ausführen")
        print("[4] Zurück")
        print("\n" + "-"*80)
        
        choice = input("Wähle ein Tool (1-4): ").strip()
        return choice
    
    def threads_menu(self):
        """Threads-Submenu"""
        print("\n" + "="*80)
        print("TIKTOK TOOLS".center(80))
        print("="*80)
        print("\n[1] TikTok Scraper")
        print("[2] Mit Tracing ausführen")
        print("[3] Zurück")
        print("\n" + "-"*80)
        
        choice = input("Wähle ein Tool (1-3): ").strip()
        return choice
    
    def config_menu(self):
        """Konfigurationsmenu"""
        print("\n" + "="*80)
        print("KONFIGURATION".center(80))
        print("="*80)
        print("\n[1] Instagram-Konfiguration anpassen")
        print("[2] Facebook-Konfiguration anpassen")
        print("[3] TikTok-Konfiguration anpassen")
        print("[4] Pinterest-Konfiguration anpassen")
        print("[5] Tumblr-Konfiguration anpassen")
        print("[6] Config-Dateien anzeigen")
        print("[7] Zurück")
        print("\n" + "-"*80)
        
        choice = input("Wähle eine Option (1-7): ").strip()
        return choice
    
    def run_instagram_tool(self, tool_num, use_tracing=False):
        """Führt Instagram-Tool aus"""
        tools = {
            '1': 'ig_complete.py',
            '2': 'ig.py',
            '3': 'ig_working.py',
            '4': 'ig_full_scraper.py'
        }
        
        if tool_num not in tools:
            print("[!] Ungültige Auswahl")
            return
        
        script = tools[tool_num]
        script_path = os.path.join(INSTAGRAM_DIR, script)
        
        if not os.path.exists(script_path):
            print(f"[!] Datei nicht gefunden: {script_path}")
            return
        
        if use_tracing:
            self.run_with_tracing(script_path, 'instagram')
        else:
            print(f"\n[*] Starte {script}...")
            try:
                runpy.run_path(script_path, run_name='__main__')
            except Exception as e:
                print(f"[!] Fehler: {e}")
    
    def run_facebook_tool(self, tool_num, use_tracing=False):
        """Führt Facebook-Tool aus"""
        tools = {
            '1': 'facebook_analyzer.py',
            '2': 'facebook_advanced_scraper.py'
        }
        
        if tool_num not in tools:
            print("[!] Ungültige Auswahl")
            return
        
        script = tools[tool_num]
        script_path = os.path.join(FACEBOOK_DIR, script)
        
        if not os.path.exists(script_path):
            print(f"[!] Datei nicht gefunden: {script_path}")
            return
        
        if use_tracing:
            self.run_with_tracing(script_path, 'facebook')
        else:
            print(f"\n[*] Starte {script}...")
            try:
                runpy.run_path(script_path, run_name='__main__')
            except Exception as e:
                print(f"[!] Fehler: {e}")
    
    def run_threads_tool(self, tool_num):
        """Führt TikTok-Tool aus"""
        if tool_num == '1':
            script_path = os.path.join(THREADS_DIR, 'tiktok_scraper.py')
            
            if not os.path.exists(script_path):
                print(f"[!] Datei nicht gefunden: {script_path}")
                print("[i] TikTok-Scraper wird noch nicht bereitgestellt")
                return
            
            print(f"\n[*] Starte TikTok Scraper...")
            try:
                runpy.run_path(script_path, run_name='__main__')
            except Exception as e:
                print(f"[!] Fehler: {e}")
    
    def pinterest_menu(self):
        """Pinterest-Submenu"""
        print("\n" + "="*80)
        print("PINTEREST TOOLS".center(80))
        print("="*80)
        print("\n[1] Pinterest Scraper")
        print("[2] Mit Tracing ausführen")
        print("[3] Zurück")
        print("\n" + "-"*80)
        
        choice = input("Wähle ein Tool (1-3): ").strip()
        return choice
    
    def tumblr_menu(self):
        """Tumblr-Submenu"""
        print("\n" + "="*80)
        print("TUMBLR TOOLS".center(80))
        print("="*80)
        print("\n[1] Tumblr Scraper")
        print("[2] Mit Tracing ausführen")
        print("[3] Zurück")
        print("\n" + "-"*80)
        
        choice = input("Wähle ein Tool (1-3): ").strip()
        return choice
    
    def run_pinterest_tool(self, tool_num, use_tracing=False):
        """Führt Pinterest-Tool aus"""
        tools = {
            '1': 'pinterest_scraper.py'
        }
        
        if tool_num not in tools:
            print("[!] Ungültige Auswahl")
            return
        
        script = tools[tool_num]
        script_path = os.path.join(PINTEREST_DIR, script)
        
        if not os.path.exists(script_path):
            print(f"[!] Datei nicht gefunden: {script_path}")
            print("[i] Pinterest-Scraper wird noch nicht bereitgestellt")
            return
        
        if use_tracing:
            self.run_with_tracing(script_path, 'pinterest')
        else:
            print(f"\n[*] Starte {script}...")
            try:
                runpy.run_path(script_path, run_name='__main__')
            except Exception as e:
                print(f"[!] Fehler: {e}")
    
    def run_tumblr_tool(self, tool_num, use_tracing=False):
        """Führt Tumblr-Tool aus"""
        tools = {
            '1': 'tumblr_scraper.py'
        }
        
        if tool_num not in tools:
            print("[!] Ungültige Auswahl")
            return
        
        script = tools[tool_num]
        script_path = os.path.join(TUMBLR_DIR, script)
        
        if not os.path.exists(script_path):
            print(f"[!] Datei nicht gefunden: {script_path}")
            print("[i] Tumblr-Scraper wird noch nicht bereitgestellt")
            return
        
        if use_tracing:
            self.run_with_tracing(script_path, 'tumblr')
        else:
            print(f"\n[*] Starte {script}...")
            try:
                runpy.run_path(script_path, run_name='__main__')
            except Exception as e:
                print(f"[!] Fehler: {e}")
    
    def run_with_tracing(self, script_path, service_name):
        """Führt Script mit OpenTelemetry Tracing aus"""
        run_traced_path = os.path.join(LIB_DIR, 'run_traced.py')
        
        if not os.path.exists(run_traced_path):
            print("[!] run_traced.py nicht gefunden")
            return
        
        print(f"\n[*] Starte {os.path.basename(script_path)} mit Tracing...")
        try:
            # Übergebe Argumente an run_traced.py
            sys.argv = ['run_traced.py', script_path, service_name]
            runpy.run_path(run_traced_path, run_name='__main__')
        except Exception as e:
            print(f"[!] Fehler: {e}")
    
    def edit_config(self, platform):
        """Öffnet Konfigurationsdatei zum Bearbeiten"""
        config_file = os.path.join(CONFIG_DIR, f'{platform}_config.json')
        
        if not os.path.exists(config_file):
            print(f"[i] Konfigurationsdatei nicht vorhanden: {config_file}")
            print(f"[*] Erstelle Standard-Konfiguration...")
            self.create_default_config(platform)
            return
        
        print(f"\n[*] Öffne: {config_file}")
        print("[i] Bearbeite die Datei und speichere sie.")
        
        try:
            if os.name == 'nt':
                os.startfile(config_file, 'edit')
            else:
                os.system(f'nano {config_file}')
        except Exception as e:
            print(f"[!] Fehler beim Öffnen: {e}")
    
    def show_config(self):
        """Zeigt alle verfügbaren Konfigurationen"""
        print("\n" + "="*80)
        print("VERFÜGBARE KONFIGURATIONEN".center(80))
        print("="*80)
        
        if not os.path.exists(CONFIG_DIR):
            print("\n[i] config/ Verzeichnis nicht vorhanden")
            return
        
        configs = [f for f in os.listdir(CONFIG_DIR) if f.endswith('.json')]
        
        if not configs:
            print("\n[i] Keine Konfigurationsdateien vorhanden")
            return
        
        for i, config in enumerate(configs, 1):
            config_path = os.path.join(CONFIG_DIR, config)
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"\n[{i}] {config}")
                    print(f"    Größe: {len(data)} Einträge")
            except Exception as e:
                print(f"\n[{i}] {config} - [Fehler beim Lesen: {e}]")
    
    def create_default_config(self, platform):
        """Erstellt Standard-Konfiguration"""
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
        
        config_data = {
            'platform': platform,
            'created': datetime.now().isoformat(),
            'settings': {
                'timeout': 10,
                'retries': 3,
                'save_reports': True,
                'report_dir': './'
            }
        }
        
        if platform == 'instagram':
            config_data['settings'].update({
                'target_username': 'cristiano',
                'max_posts': 30,
                'get_comments': True,
                'get_likes': True
            })
        elif platform == 'facebook':
            config_data['settings'].update({
                'search_name': 'John Doe',
                'search_location': None,
                'get_posts': True,
                'get_comments': True
            })
        elif platform == 'tiktok':
            config_data['settings'].update({
                'target_username': 'example_user',
                'max_videos': 20,
                'get_comments': True,
                'get_likes': True
            })
        elif platform == 'pinterest':
            config_data['settings'].update({
                'search_query': 'example',
                'max_pins': 20,
                'get_comments': True,
                'get_likes': True
            })
        elif platform == 'tumblr':
            config_data['settings'].update({
                'blog_name': 'example_blog',
                'max_posts': 20,
                'get_comments': True,
                'get_likes': True
            })
        
        config_file = os.path.join(CONFIG_DIR, f'{platform}_config.json')
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Konfiguration erstellt: {config_file}")
    
    def run(self):
        """Hauptprogrammschleife"""
        while self.running:
            choice = self.show_menu()
            
            if choice == '1':
                # Instagram
                while True:
                    sub_choice = self.instagram_menu()
                    if sub_choice == '6':
                        break
                    elif sub_choice == '5':
                        # Mit Tracing
                        print("\nWelches Tool möchtest du mit Tracing ausführen?")
                        print("[1] ig_complete.py")
                        print("[2] ig.py")
                        print("[3] ig_working.py")
                        print("[4] ig_full_scraper.py")
                        tool_choice = input("Wahl (1-4): ").strip()
                        self.run_instagram_tool(tool_choice, use_tracing=True)
                    else:
                        self.run_instagram_tool(sub_choice)
            
            elif choice == '2':
                # Facebook
                while True:
                    sub_choice = self.facebook_menu()
                    if sub_choice == '4':
                        break
                    elif sub_choice == '3':
                        # Mit Tracing
                        print("\nWelches Tool möchtest du mit Tracing ausführen?")
                        print("[1] facebook_analyzer.py")
                        print("[2] facebook_advanced_scraper.py")
                        tool_choice = input("Wahl (1-2): ").strip()
                        self.run_facebook_tool(tool_choice, use_tracing=True)
                    else:
                        self.run_facebook_tool(sub_choice)
            
            elif choice == '3':
                # TikTok
                while True:
                    sub_choice = self.threads_menu()
                    if sub_choice == '3':
                        break
                    elif sub_choice == '2':
                        # Mit Tracing
                        print("\nWelches Tool möchtest du mit Tracing ausführen?")
                        print("[1] tiktok_scraper.py")
                        tool_choice = input("Wahl (1-1): ").strip()
                        # TODO: Implement tracing for TikTok
                        print("[i] Tracing für TikTok wird noch entwickelt")
                    else:
                        self.run_threads_tool(sub_choice)
            
            elif choice == '4':
                # Pinterest
                while True:
                    sub_choice = self.pinterest_menu()
                    if sub_choice == '3':
                        break
                    elif sub_choice == '2':
                        # Mit Tracing
                        print("[i] Tracing für Pinterest wird noch entwickelt")
                    else:
                        self.run_pinterest_tool(sub_choice)
            
            elif choice == '5':
                # Tumblr
                while True:
                    sub_choice = self.tumblr_menu()
                    if sub_choice == '3':
                        break
                    elif sub_choice == '2':
                        # Mit Tracing
                        print("[i] Tracing für Tumblr wird noch entwickelt")
                    else:
                        self.run_tumblr_tool(sub_choice)
            
            elif choice == '6':
                # Konfiguration
                while True:
                    config_choice = self.config_menu()
                    if config_choice == '7':
                        break
                    elif config_choice == '6':
                        self.show_config()
                    elif config_choice in ['1', '2', '3', '4', '5']:
                        platforms = {
                            '1': 'instagram',
                            '2': 'facebook',
                            '3': 'tiktok',
                            '4': 'pinterest',
                            '5': 'tumblr'
                        }
                        self.edit_config(platforms[config_choice])
                    else:
                        print("[!] Ungültige Auswahl")
            
            elif choice == '7':
                # Beenden
                print("\n[*] Programm beendet.")
                self.running = False
            
            else:
                print("[!] Ungültige Auswahl")

def has_any_config():
    """Prüft, ob mindestens eine Konfiguration vorhanden ist"""
    if not os.path.exists(CONFIG_DIR):
        return False
    
    configs = [f for f in os.listdir(CONFIG_DIR) if f.endswith('_config.json')]
    return len(configs) > 0


def main():
    """Hauptfunktion"""
    # Prüfe, ob Konfigurationen vorhanden sind
    if not has_any_config():
        wizard = SetupWizard()
        if not wizard.run_setup():
            print("\n[!] Setup abgebrochen. Das Programm wird beendet.")
            return
        print("\n[*] Drücke Enter um zum Hauptmenü zu gelangen...")
        input()
    
    menu = MainMenu()
    menu.run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Programm durch Benutzer unterbrochen.")
    except Exception as e:
        print(f"\n[!] Fehler: {e}")
        import traceback
        traceback.print_exc()
