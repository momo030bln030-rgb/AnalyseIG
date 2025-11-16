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
INSTAGRAM_DIR = os.path.join(MAIN_DIR, 'instagram')
FACEBOOK_DIR = os.path.join(MAIN_DIR, 'facebook')
THREADS_DIR = os.path.join(MAIN_DIR, 'threads')
CONFIG_DIR = os.path.join(MAIN_DIR, 'config')
LIB_DIR = os.path.join(MAIN_DIR, 'lib')

# Ensure lib ist im sys.path
if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)

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
        print("[3] Threads")
        print("[4] TikTok")
        print("[5] Konfiguration bearbeiten")
        print("[6] Beenden")
        print("\n" + "-"*80)
        
        choice = input("Wähle eine Option (1-6): ").strip()
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
        print("THREADS TOOLS".center(80))
        print("="*80)
        print("\n[1] Threads Scraper")
        print("[2] Zurück")
        print("\n" + "-"*80)
        
        choice = input("Wähle ein Tool (1-2): ").strip()
        return choice
    
    def config_menu(self):
        """Konfigurationsmenu"""
        print("\n" + "="*80)
        print("KONFIGURATION".center(80))
        print("="*80)
        print("\n[1] Instagram-Konfiguration anpassen")
        print("[2] Facebook-Konfiguration anpassen")
        print("[3] Threads-Konfiguration anpassen")
        print("[4] TikTok-Konfiguration anpassen")
        print("[5] Config-Datei anzeigen")
        print("[6] Zurück")
        print("\n" + "-"*80)
        
        choice = input("Wähle eine Option (1-6): ").strip()
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
        """Führt Threads-Tool aus"""
        if tool_num == '1':
            script_path = os.path.join(THREADS_DIR, 'threads_scraper.py')
            
            if not os.path.exists(script_path):
                print(f"[!] Datei nicht gefunden: {script_path}")
                print("[i] Threads-Scraper wird noch nicht bereitgestellt")
                return
            
            print(f"\n[*] Starte Threads Scraper...")
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
        elif platform == 'threads':
            config_data['settings'].update({
                'target_username': 'example_user',
                'max_posts': 20
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
                # Threads
                while True:
                    sub_choice = self.threads_menu()
                    if sub_choice == '2':
                        break
                    else:
                        self.run_threads_tool(sub_choice)
            
            elif choice == '4':
                # TikTok - Placeholder
                print("\n[i] TikTok-Scraper wird noch entwickelt...")
            
            elif choice == '5':
                # Konfiguration
                while True:
                    config_choice = self.config_menu()
                    if config_choice == '6':
                        break
                    elif config_choice == '5':
                        self.show_config()
                    elif config_choice in ['1', '2', '3', '4']:
                        platforms = {
                            '1': 'instagram',
                            '2': 'facebook',
                            '3': 'threads',
                            '4': 'tiktok'
                        }
                        self.edit_config(platforms[config_choice])
                    else:
                        print("[!] Ungültige Auswahl")
            
            elif choice == '6':
                # Beenden
                print("\n[*] Programm beendet.")
                self.running = False
            
            else:
                print("[!] Ungültige Auswahl")

def main():
    """Hauptfunktion"""
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
