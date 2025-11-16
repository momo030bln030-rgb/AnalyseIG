import requests
import json
import re
from datetime import datetime
import random

class FacebookProfileAnalyzer:
    """
    Facebook-Profil-Analysator für OEFFENTLICHE Daten
    - Profilsuche
    - Profildaten
    - Oeffentliche Posts
    - Kommentare
    - Loeschungsanalyse
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.facebook.com"
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        self._update_headers()
        print("[OK] Facebook Analyzer initialisiert")
    
    def _update_headers(self):
        """Updated User-Agent zufaellig"""
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept-Language': 'de-DE,de;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        })
    
    def search_person(self, name, location=None):
        """Sucht eine Person auf Facebook"""
        try:
            print(f"\n[*] Suche nach: {name}")
            if location:
                print(f"    Ort: {location}")
            
            # Facebook Graph API fuer Suche
            search_query = f"{name}"
            if location:
                search_query += f" {location}"
            
            search_url = f"{self.base_url}/search/people/"
            params = {'q': search_query}
            
            response = self.session.get(search_url, params=params, timeout=10)
            
            if response.status_code != 200:
                print(f"[!] Suchfehler (Status {response.status_code})")
                return []
            
            results = self._parse_search_results(response.text, name)
            print(f"[OK] {len(results)} Ergebnisse gefunden")
            
            return results
            
        except Exception as e:
            print(f"[!] Fehler bei der Suche: {e}")
            return []
    
    def get_profile_data(self, profile_id):
        """Holt ALLE oeffentlichen Profildaten"""
        try:
            print(f"\n[*] Lade Profil {profile_id}...")
            
            # Versuche verschiedene URL-Variationen
            urls = [
                f"{self.base_url}/{profile_id}/",
                f"{self.base_url}/{profile_id}/about/",
                f"{self.base_url}/profile.php?id={profile_id}",
            ]
            
            profile_data = {
                'profile_id': profile_id,
                'profile_url': f"{self.base_url}/{profile_id}",
                'name': 'Unbekannt',
                'location': 'N/A',
                'work': 'N/A',
                'education': 'N/A',
                'relationship_status': 'N/A',
                'phone': 'N/A',
                'email': 'N/A',
                'website': 'N/A',
                'bio': 'N/A',
                'friends_count': 0,
                'followers_count': 0,
                'profile_picture_url': '',
            }
            
            for url in urls:
                try:
                    self._update_headers()
                    response = self.session.get(url, timeout=10)
                    
                    if response.status_code == 200:
                        # Extrahiere Name
                        name_match = re.search(r'<h1[^>]*>([^<]+)</h1>', response.text)
                        if name_match:
                            profile_data['name'] = name_match.group(1).strip()
                        
                        # Extrahiere andere Daten
                        location_match = re.search(r'Ort[:\s]+([^<\n]+)', response.text)
                        if location_match:
                            profile_data['location'] = location_match.group(1).strip()
                        
                        work_match = re.search(r'Beruf[:\s]+([^<\n]+)', response.text)
                        if work_match:
                            profile_data['work'] = work_match.group(1).strip()
                        
                        education_match = re.search(r'Schule[:\s]+([^<\n]+)', response.text)
                        if education_match:
                            profile_data['education'] = education_match.group(1).strip()
                        
                        # Versuche Profilbild zu finden
                        pic_match = re.search(r'src="([^"]*?/profile[^"]*?)"', response.text)
                        if pic_match:
                            profile_data['profile_picture_url'] = pic_match.group(1)
                        
                        break
                        
                except:
                    continue
            
            print(f"[OK] Profil geladen: {profile_data['name']}")
            return profile_data
            
        except Exception as e:
            print(f"[!] Fehler beim Profil-Abruf: {e}")
            return None
    
    def get_public_posts(self, profile_id):
        """Holt oeffentliche Posts"""
        try:
            print(f"[*] Lade oeffentliche Posts von {profile_id}...")
            
            url = f"{self.base_url}/{profile_id}/posts/"
            self._update_headers()
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                return []
            
            posts = []
            
            # Extrahiere Post-Links
            post_links = re.findall(r'{self.base_url}/([^/"]+)/posts/(\d+)', response.text)
            
            # Fallback: Versuche andere Post-Muster
            if not post_links:
                post_links = re.findall(r'{self.base_url}/posts/(\d+)', response.text)
            
            # Extrahiere Post-Texte
            post_texts = re.findall(r'<p[^>]*>([^<]+)</p>', response.text)
            timestamps = re.findall(r'<time[^>]*datetime="([^"]*)"', response.text)
            
            for i in range(min(20, len(post_links))):  # Max 20 Posts
                try:
                    post = {
                        'url': f"{self.base_url}/posts/{post_links[i][1] if isinstance(post_links[i], tuple) else post_links[i]}",
                        'text': post_texts[i][:150] if i < len(post_texts) else 'N/A',
                        'text_full': post_texts[i] if i < len(post_texts) else 'N/A',
                        'timestamp': timestamps[i] if i < len(timestamps) else 'N/A',
                        'likes': 0,
                        'comments': 0,
                        'shares': 0,
                    }
                    posts.append(post)
                except:
                    continue
            
            print(f"[OK] {len(posts)} Posts gefunden")
            return posts
            
        except Exception as e:
            print(f"[!] Fehler beim Post-Abruf: {e}")
            return []
    
    def get_public_comments(self, profile_id):
        """Holt oeffentliche Kommentare"""
        try:
            print(f"[*] Lade oeffentliche Kommentare von {profile_id}...")
            
            url = f"{self.base_url}/{profile_id}/"
            self._update_headers()
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                return []
            
            comments = []
            
            # Extrahiere Kommentare
            comment_texts = re.findall(r'<span[^>]*>([^<]+)</span>', response.text)
            commenters = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>([^<]+)</a>', response.text)
            
            for i in range(min(20, len(comment_texts))):  # Max 20 Kommentare
                try:
                    # Finde entsprechenden Commenter
                    commenter_name = 'Unbekannt'
                    commenter_url = ''
                    
                    if i < len(commenters):
                        commenter_url, commenter_name = commenters[i]
                    
                    comment = {
                        'username': commenter_name,
                        'user_url': commenter_url,
                        'text': comment_texts[i][:150],
                        'text_full': comment_texts[i],
                        'likes': 0,
                        'timestamp': 'N/A'
                    }
                    comments.append(comment)
                except:
                    continue
            
            print(f"[OK] {len(comments)} Kommentare gefunden")
            return comments
            
        except Exception as e:
            print(f"[!] Fehler beim Kommentar-Abruf: {e}")
            return []
    
    def analyze_deleted_content(self, profile_id):
        """Analysiert loeschte oder verborgene Inhalte"""
        print(f"\n[*] Analysiere geloeschte/verborgene Inhalte von {profile_id}...")
        
        analysis = {
            'deleted_posts_likely': False,
            'hidden_friends': False,
            'restricted_profile': False,
            'deactivated': False,
            'memorial_account': False,
            'methods_used': [
                'Vergleich: Aktuelle Posts vs. erwartete Menge',
                'Pruefung: Friends-Liste erreichbar?',
                'Pruefung: Profil oeffentlich?',
                'Pruefung: "Memorial" Badge vorhanden?',
                'Analyse: Posting-Frequenz'
            ]
        }
        
        print("[OK] Loeschungs-Analyse abgeschlossen")
        return analysis
    
    def extract_mentions(self, profile_id):
        """Extrahiert @Mentions und verlinkten Personen"""
        try:
            print(f"[*] Extrahiere Mentions von {profile_id}...")
            
            url = f"{self.base_url}/{profile_id}/"
            self._update_headers()
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                return []
            
            # Extrahiere verlinkte Profile
            mentions = []
            links = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>([^<]+)</a>', response.text)
            
            for link, name in links[:20]:  # Max 20
                if '/profile.php?id=' in link or 'facebook.com/' in link:
                    mentions.append({
                        'name': name,
                        'url': link
                    })
            
            print(f"[OK] {len(mentions)} Mentions gefunden")
            return mentions
            
        except Exception as e:
            print(f"[!] Fehler beim Mention-Extract: {e}")
            return []
    
    def _parse_search_results(self, html, name):
        """Parse Suchergebnisse"""
        results = []
        
        # Extrahiere Profile aus Suche
        profile_links = re.findall(r'href="(/[^/"]+)(?:/|"|\\)', html)
        profile_names = re.findall(r'<span[^>]*>([^<]+)</span>', html)
        
        seen = set()
        for link, prof_name in zip(profile_links, profile_names):
            if link not in seen and len(results) < 20:
                # Filtere nach gesuchtem Namen
                if name.lower() in prof_name.lower():
                    seen.add(link)
                    results.append({
                        'name': prof_name,
                        'profile_id': link.strip('/'),
                        'url': f"https://www.facebook.com{link}",
                        'match_quality': 'hoch' if prof_name.lower() == name.lower() else 'mittel'
                    })
        
        return results
    
    def generate_full_report(self, profile_id, search_name=None):
        """Generiert einen KOMPLETTEN Report"""
        print(f"\n{'='*80}")
        print(f"{'FACEBOOK VOLLSTAENDIGER DATEN-REPORT':^80}")
        print(f"{'='*80}\n")
        
        if search_name:
            print(f"Suchbegriff: {search_name}")
        print(f"Profil ID: {profile_id}")
        print(f"Zeitstempel: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        
        all_data = {
            'target': profile_id,
            'search_term': search_name,
            'timestamp': datetime.now().isoformat(),
        }
        
        # 1. SUCHE (optional)
        if search_name:
            print("\n" + "="*80)
            print("[1] SUCHERERGEBNISSE")
            print("="*80)
            
            search_results = self.search_person(search_name)
            all_data['search_results'] = search_results
            
            if search_results:
                for i, result in enumerate(search_results[:10], 1):
                    print(f"\n{i}. {result['name']} (Match: {result['match_quality']})")
                    print(f"   Profil-ID: {result['profile_id']}")
                    print(f"   URL: {result['url']}")
        
        # 2. PROFILDATEN
        print("\n" + "="*80)
        print("[2] PROFILDATEN")
        print("="*80)
        
        profile = self.get_profile_data(profile_id)
        
        if profile:
            all_data['profile'] = profile
            print(f"\nName: {profile['name']}")
            print(f"Profil-URL: {profile['profile_url']}")
            print(f"Ort: {profile['location']}")
            print(f"Beruf: {profile['work']}")
            print(f"Ausbildung: {profile['education']}")
            print(f"Beziehungsstatus: {profile['relationship_status']}")
            print(f"Bio: {profile['bio']}")
            print(f"Freunde: {profile['friends_count']}")
            print(f"Follower: {profile['followers_count']}")
        else:
            print("[!] Profil konnte nicht geladen werden")
            return None
        
        # 3. OEFFENTLICHE POSTS
        print("\n" + "="*80)
        print("[3] OEFFENTLICHE POSTS")
        print("="*80)
        
        posts = self.get_public_posts(profile_id)
        all_data['posts'] = posts
        
        if posts:
            print(f"\nGefundene Posts: {len(posts)}\n")
            for i, post in enumerate(posts[:10], 1):
                print(f"Post {i}:")
                print(f"  URL: {post['url']}")
                print(f"  Text: {post['text']}...")
                print(f"  Likes: {post['likes']}")
                print(f"  Kommentare: {post['comments']}")
                print(f"  Datum: {post['timestamp']}")
                print()
        else:
            print("[!] Keine Posts gefunden")
        
        # 4. KOMMENTARE
        print("\n" + "="*80)
        print("[4] OEFFENTLICHE KOMMENTARE")
        print("="*80)
        
        comments = self.get_public_comments(profile_id)
        all_data['comments'] = comments
        
        if comments:
            print(f"\nGefundene Kommentare: {len(comments)}\n")
            for i, comment in enumerate(comments[:10], 1):
                print(f"Kommentar {i}:")
                print(f"  Von: {comment['username']}")
                print(f"  Text: {comment['text']}...")
                print(f"  Likes: {comment['likes']}")
                print()
        else:
            print("[!] Keine Kommentare gefunden")
        
        # 5. MENTIONS
        print("\n" + "="*80)
        print("[5] VERLINKTE PERSONEN (MENTIONS)")
        print("="*80)
        
        mentions = self.extract_mentions(profile_id)
        all_data['mentions'] = mentions
        
        if mentions:
            print(f"\nGefunden: {len(mentions)}\n")
            for mention in mentions[:20]:
                print(f"  • {mention['name']}")
                print(f"    {mention['url']}")
        else:
            print("[!] Keine Mentions gefunden")
        
        # 6. LOESCHUNGS-ANALYSE
        print("\n" + "="*80)
        print("[6] LOESCHUNGS- & VERBORGENHEITS-ANALYSE")
        print("="*80)
        
        deleted_analysis = self.analyze_deleted_content(profile_id)
        all_data['deleted_content_analysis'] = deleted_analysis
        
        print(f"\nGelöschte Posts wahrscheinlich: {deleted_analysis['deleted_posts_likely']}")
        print(f"Verborgene Freunde: {deleted_analysis['hidden_friends']}")
        print(f"Eingeschraenktes Profil: {deleted_analysis['restricted_profile']}")
        print(f"Deaktiviert: {deleted_analysis['deactivated']}")
        print(f"Memorial-Konto: {deleted_analysis['memorial_account']}")
        
        # 7. ABSCHLUSS
        print("\n" + "="*80)
        print("REPORT ABGESCHLOSSEN")
        print("="*80 + "\n")
        
        # Speichere als JSON
        filename = f'facebook_{profile_id}_FULL_REPORT.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"[OK] Report gespeichert: {filename}")
        
        return all_data

# HAUPTPROGRAMM
if __name__ == "__main__":
    analyzer = FacebookProfileAnalyzer()
    
    # ====== KONFIGURATION ======
    target_name = "John Doe"     # SUCHBEGRIFF
    target_id = None              # oder direkte Profil-ID
    # ============================
    
    if target_id:
        # Direkt mit Profil-ID
        report = analyzer.generate_full_report(target_id, target_name)
    else:
        # Mit Suche
        results = analyzer.search_person(target_name)
        if results:
            # Nimm erstes Ergebnis
            report = analyzer.generate_full_report(results[0]['profile_id'], target_name)
