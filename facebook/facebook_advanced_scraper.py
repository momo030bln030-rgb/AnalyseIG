"""
Facebook Advanced Profile Scraper mit Umgehungstechniken
- Request Delays & Rate Limiting
- User-Agent Rotation
- Proxy Support
- Archive.org Integration
- Reverse Image Search
from datetime import datetime
from bs4 import BeautifulSoup
import time
import random
import urllib.parse

class AdvancedFacebookScraper:
    """
    Erweiterte Facebook-Scraping mit Umgehungstechniken
    """
    
    def __init__(self, use_delays=True, proxy=None):
        self.session = requests.Session()
        self.use_delays = use_delays
        self.base_url = "https://www.facebook.com"
        self.proxy = proxy if proxy else {}
        
        # Rotating User-Agents
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
        ]
        
        self._update_headers()
        print("[OK] Advanced Facebook Scraper mit Umgehungstechniken initialisiert")
    
    def _update_headers(self):
        """Aktualisiere Header mit zufälligem User-Agent"""
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'de-DE,de;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Cache-Control': 'max-age=0'
        })
    
    def _delay(self, min_sec=2, max_sec=5):
        """Füge zufällige Verzögerung ein"""
        if self.use_delays:
            delay = random.uniform(min_sec, max_sec)
            print(f"[WAIT] Warte {delay:.1f} Sekunden...")
            time.sleep(delay)
    
    def get_from_archive_org(self, profile_id, snapshots=5):
        """
        Hole gelöschte/archivierte Inhalte von Archive.org (Wayback Machine)
        """
        try:
            print(f"\n[*] Suche in Archive.org nach: {profile_id}")
            
            url = f"{self.base_url}/{profile_id}"
            
            # Hole Snapshot-Liste
            api_url = f"https://archive.org/wayback/available?url={url}&output=json"
            response = self.session.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                snapshots_list = data.get('archived_snapshots', {}).get('snapshots', [])
                
                    timestamp = snapshot.get('timestamp', '')
                    url_snapshot = f"https://web.archive.org/web/{timestamp}/{url}"
                    
                    archived_data['snapshots'].append({
                        'date': f"{timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]} {timestamp[8:10]}:{timestamp[10:12]}",
                        'url': url_snapshot,
                        'timestamp': timestamp
                    })
                
                print(f"[OK] {len(snapshots_list)} Archive-Snapshots gefunden")
                return archived_data
                
        except Exception as e:
            print(f"[!] Archive.org Fehler: {e}")
        
        return {'found_snapshots': 0, 'snapshots': []}
    
    def get_from_google_cache(self, profile_id):
        """
        Hole Daten aus Google Cache
        """
        try:
            print(f"\n[*] Suche Google Cache für: {profile_id}")
            
            url = f"{self.base_url}/{profile_id}"
            cache_url = f"http://webcache.googleusercontent.com/cache:{url}"
            
            self._update_headers()
            response = self.session.get(cache_url, timeout=10, proxies=self.proxy)
            
            if response.status_code == 200:
                print("[OK] Google Cache gefunden")
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                cached_data = {
                    'found': True,
                    'cache_date': 'Unbekannt',
                    'content_preview': response.text[:500],
                    'note': 'Gecachter Inhalt - möglicherweise veraltet'
                }
                
                return cached_data
            else:
                print(f"[!] Google Cache nicht verfügbar (Status {response.status_code})")
                return {'found': False}
                
        except Exception as e:
            print(f"[!] Google Cache Fehler: {e}")
            return {'found': False}
    
    def reverse_image_search(self, image_url):
        """
        Suche ein Profilbild auf anderen Plattformen
        (Google Images, TinEye)
        """
        try:
            print(f"\n[*] Reverse Image Search fuer: {image_url}")
            
            results = {
                'google_images': f"https://www.google.com/searchbyimage?image_url={urllib.parse.quote(image_url)}",
                'tineye': f"https://tineye.com/search?url={urllib.parse.quote(image_url)}",
                'yandex': f"https://yandex.com/images/search?rpt=imageview&url={urllib.parse.quote(image_url)}",
                'note': 'Oeffne diese Links im Browser um Duplikate zu finden'
            }
            
            print("[OK] Reverse Image Search Links generiert")
            return results
            
        except Exception as e:
            print(f"[!] Reverse Image Search Fehler: {e}")
            return {}
    
    def search_with_filters(self, name, location=None, workplace=None, school=None):
        """
        Suche mit erweiterten Filtern
        """
        try:
            print(f"\n[*] Erweiterte Suche...")
            print(f"    Name: {name}")
            if location:
                print(f"    Lokation: {location}")
            if workplace:
                print(f"    Arbeit: {workplace}")
            if school:
                print(f"    Schule: {school}")
            
            # Konstruiere Such-URL
            search_params = {'q': name}
            if location:
                search_params['location'] = location
            if workplace:
                search_params['workplace'] = workplace
            if school:
                search_params['school'] = school
            
            search_url = f"{self.base_url}/search/people/?{'&'.join([f'{k}={v}' for k,v in search_params.items()])}"
            
            self._update_headers()
            response = self.session.get(search_url, timeout=10, proxies=self.proxy)
            self._delay()
            
            if response.status_code == 200:
                print("[OK] Suche durchgeführt")
                return self._parse_search_results(response.text)
            else:
                print(f"[!] Suchfehler (Status {response.status_code})")
                return []
                
        except Exception as e:
            print(f"[!] Suchfehler: {e}")
            return []
    
    def _parse_search_results(self, html):
        """Parse Suchergebnisse"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            
            # Finde Profil-Links
            links = soup.find_all('a', href=re.compile(r'^/[a-z0-9.]+'))
            
            for link in links:
                profile_id = link.get('href').strip('/').split('?')[0]
                name = link.get_text(strip=True)
                
                if profile_id and name:
                    results.append({
                        'name': name,
                        'profile_id': profile_id,
                        'url': f"{self.base_url}/{profile_id}",
                        'method': 'advanced_search'
                    })
            
            return results[:20]  # Max 20
            
        except Exception as e:
            print(f"[!] Parse Fehler: {e}")
            return []
    
    def analyze_profile_advanced(self, profile_id):
        """
        Erweiterte Profil-Analyse mit allen Techniken
        """
        try:
            print(f"\n[*] Erweiterte Profil-Analyse für: {profile_id}")
            
            report = {
                'profile_id': profile_id,
                'url': f"{self.base_url}/{profile_id}",
                'analysis_methods': []
            }
            
            # 1. Normale HTML-Extraktion
            print("\n[1/4] HTML-Extraktion...")
            self._update_headers()
            response = self.session.get(f"{self.base_url}/{profile_id}", timeout=10, proxies=self.proxy)
            self._delay()
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('title')
                if title:
                    report['name'] = title.get_text().replace(' | Facebook', '').strip()
                report['analysis_methods'].append('HTML-Extraktion')
            
            # 2. Google Cache
            print("[2/4] Google Cache...")
            cache_data = self.get_from_google_cache(profile_id)
            report['google_cache'] = cache_data
            if cache_data.get('found'):
                report['analysis_methods'].append('Google Cache')
            
            # 3. Archive.org
            print("[3/4] Archive.org...")
            archive_data = self.get_from_archive_org(profile_id, snapshots=3)
            report['archive_org'] = archive_data
            if archive_data.get('found_snapshots', 0) > 0:
                report['analysis_methods'].append('Archive.org')
            
            # 4. Reverse Image Search
            print("[4/4] Reverse Image Search...")
            # Placeholder für Profil-Bild
            report['reverse_image_search'] = self.reverse_image_search(f"{self.base_url}/{profile_id}/picture/")
            report['analysis_methods'].append('Reverse Image Search (Links)')
            
            print(f"\n[OK] Erweiterte Analyse abgeschlossen")
            return report
            
        except Exception as e:
            print(f"[!] Analysefehler: {e}")
            return {'profile_id': profile_id, 'error': str(e)}
    
    def generate_comprehensive_report(self, profile_identifier, search_filters=None):
        """
        Generiere einen UMFASSENDEN Report mit ALLEN Methoden
        """
        print(f"\n{'='*80}")
        print(f"{'FACEBOOK ADVANCED ANALYZER - UMFASSENDER REPORT':^80}")
        print(f"{'='*80}\n")
        print(f"Profil: {profile_identifier}")
        print(f"Zeitstempel: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        print(f"Verzögerungen aktiviert: {self.use_delays}\n")
        
        report = {
            'target': profile_identifier,
            'timestamp': datetime.now().isoformat(),
            'methods_available': []
        }
        
        # Erweiterte Suche mit Filtern
        if search_filters:
            print("\n" + "="*80)
            print("[SUCHE] ERWEITERTE PROFIL-SUCHE")
            print("="*80)
            
            search_results = self.search_with_filters(
                search_filters.get('name', ''),
                location=search_filters.get('location'),
                workplace=search_filters.get('workplace'),
                school=search_filters.get('school')
            )
            
            report['search_results'] = search_results
            report['methods_available'].append('Advanced Search with Filters')
            
            if search_results:
                profile_identifier = search_results[0]['profile_id']
                print(f"\n[GEWÄHLT] {search_results[0]['name']} ({profile_identifier})")
        
        # Erweiterte Profil-Analyse
        print("\n" + "="*80)
        print("[PROFIL-ANALYSE] MIT ALLEN VERFUEGBAREN METHODEN")
        print("="*80)
        
        advanced_data = self.analyze_profile_advanced(profile_identifier)
        report['advanced_analysis'] = advanced_data
        report['methods_available'].extend(advanced_data.get('analysis_methods', []))
        
        # Ausgabe
        print(f"\nName: {advanced_data.get('name', 'N/A')}")
        print(f"Profil-ID: {advanced_data.get('profile_id', 'N/A')}")
        
        if advanced_data.get('archive_org', {}).get('found_snapshots', 0) > 0:
            print(f"\nArchivierte Versionen ({advanced_data['archive_org']['found_snapshots']}):")
            for snapshot in advanced_data['archive_org']['snapshots'][:5]:
                print(f"  - {snapshot['date']}: {snapshot['url']}")
        
        print(f"\nReverse Image Search Links:")
        for service, link in advanced_data.get('reverse_image_search', {}).items():
            if service != 'note':
                print(f"  - {service}: {link}")
        
        # Speichern
        filename = f'facebook_{profile_identifier}_ADVANCED_REPORT.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n{'='*80}")
        print(f"[OK] Report gespeichert: {filename}")
        print(f"Genutzte Methoden: {', '.join(report['methods_available'])}")
        print(f"{'='*80}\n")
        
        return report

# ============================================================================
# HAUPTPROGRAMM
# ============================================================================

if __name__ == "__main__":
    # Initialisiere Scraper MIT Verzögerungen (respektful scraping)
    scraper = AdvancedFacebookScraper(use_delays=True, proxy={})
    
    print("\n" + "="*80)
    print("FACEBOOK ADVANCED PROFILE SCRAPER")
    print("="*80)
    
    # OPTION 1: Einfache Profil-Analyse
    print("\n[MODUS 1] Einfache Profil-Analyse mit allen Methoden")
    print("-"*80)
    profile = "cristiano"  # HIER PROFIL EINGEBEN
    report = scraper.generate_comprehensive_report(profile)
    
    # OPTION 2: Suche mit Filtern
    print("\n[MODUS 2] Erweiterte Suche mit Filtern")
    print("-"*80)
    
    search_filters = {
        'name': 'Max Mueller',  # Name
        'location': 'Berlin',    # Optional
        'workplace': None,       # Optional
        'school': None           # Optional
    }
    # Decomment um zu nutzen:
    # report = scraper.generate_comprehensive_report("", search_filters=search_filters)
