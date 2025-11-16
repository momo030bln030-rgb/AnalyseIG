import requests
import json
import time
import re
from datetime import datetime
import os
from bs4 import BeautifulSoup

class InstagramPrivateInvestigator:
    def __init__(self, username, password):
        self.session = requests.Session()
        self.username = username
        self.base_url = "https://www.instagram.com"
        self.user_id = None
        # Setze einen realistischen User-Agent
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        print("[*] Instagram Investigator initialisiert")
        
    def get_public_profile_data(self, target_username):
        """Holt öffentliche Profildaten mit erweiterten Methoden"""
        try:
            print(f"[*] Hole Profildaten für @{target_username}...")
            
            # Versuche mehrere Methoden
            methods = [
                self._method_web_scraping,
                self._method_graphql_api,
                self._method_instagram_api
            ]
            
            for method in methods:
                try:
                    data = method(target_username)
                    if data:
                        return data
                except:
                    continue
            
            # Fallback
            return {
                'username': target_username,
                'full_name': 'N/A',
                'biography': 'N/A',
                'follower_count': 0,
                'following_count': 0,
                'post_count': 0,
                'profile_pic_url': '',
                'is_private': False,
                'is_verified': False,
                'website': 'N/A',
                'user_id': ''
            }
            
        except Exception as e:
            print(f"[!] Fehler beim Abrufen: {e}")
            return None
    
    def _method_web_scraping(self, target_username):
        """Webseiten-Scraping Methode"""
        url = f"{self.base_url}/{target_username}/"
        response = self.session.get(url, timeout=10)
        
        if response.status_code == 404:
            return None
        
        if response.status_code != 200:
            return None
        
        # Extrahiere mit Regex
        patterns = {
            'follower_count': r'"follower_count":"?(\d+)"?',
            'following_count': r'"following_count":"?(\d+)"?',
            'post_count': r'"edge_owner_to_timeline_media":\{"count":(\d+)',
            'full_name': r'"full_name":"([^"]+)"',
            'biography': r'"biography":"([^"]*)"'
        }
        
        data = {'username': target_username}
        for key, pattern in patterns.items():
            match = re.search(pattern, response.text)
            if match:
                data[key] = match.group(1)
        
        return data if len(data) > 1 else None
    
    def _method_graphql_api(self, target_username):
        """GraphQL API Methode"""
        url = f"{self.base_url}/graphql/query/"
        
        query = f'''
        query {{
            user(name: "{target_username}") {{
                id
                username
                full_name
                biography
                edge_followed_by {{
                    count
                }}
                edge_follow {{
                    count
                }}
                edge_owner_to_timeline_media {{
                    count
                }}
                profile_pic_url
                is_verified
                is_private
                external_url
            }}
        }}
        '''
        
        try:
            response = self.session.post(url, json={'query': query}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                user = data.get('data', {}).get('user', {})
                return self._extract_profile_info(user)
        except:
            pass
        
        return None
    
    def _method_instagram_api(self, target_username):
        """Alternative Instagram API Methode"""
        # Versuche über API ohne Login
        url = f"{self.base_url}/api/v1/users/web_profile_info/"
        params = {'username': target_username}
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                user_data = response.json().get('data', {}).get('user', {})
                return self._extract_profile_info(user_data)
        except:
            pass
        
        return None

    def _extract_profile_info(self, user_data):
        """Extrahiert wichtige Profilinformationen aus JSON"""
        try:
            return {
                'username': user_data.get('username', ''),
                'full_name': user_data.get('full_name', ''),
                'biography': user_data.get('biography', ''),
                'follower_count': user_data.get('edge_followed_by', {}).get('count', 0),
                'following_count': user_data.get('edge_follow', {}).get('count', 0),
                'post_count': user_data.get('edge_owner_to_timeline_media', {}).get('count', 0),
                'profile_pic_url': user_data.get('profile_pic_url_hd', user_data.get('profile_pic_url', '')),
                'is_private': user_data.get('is_private', False),
                'is_verified': user_data.get('is_verified', False),
                'website': user_data.get('external_url', ''),
                'user_id': user_data.get('id', '')
            }
        except:
            return user_data
        
    def get_recent_posts_info(self, target_username):
        """Versucht Informationen zu den neuesten Posts zu bekommen"""
        try:
            print(f"[*] Hole Post-Informationen für @{target_username}...")
            
            url = f"{self.base_url}/{target_username}/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                return []
            
            posts_info = []
            
            # Versuche Posts aus HTML zu extrahieren
            match = re.search(r'"edges":\s*(\[.*?\])', response.text)
            if match:
                try:
                    edges = json.loads(match.group(1))
                    for edge in edges[:12]:  # Erste 12 Posts
                        if 'node' in edge:
                            node = edge['node']
                            posts_info.append({
                                'id': node.get('id', ''),
                                'caption': node.get('edge_media_to_caption', {}).get('edges', [{}])[0].get('node', {}).get('text', ''),
                                'likes': node.get('edge_likedby', {}).get('count', 0),
                                'comments': node.get('edge_media_to_comment', {}).get('count', 0),
                                'timestamp': node.get('taken_at_timestamp', 0),
                                'media_type': node.get('__typename', 'GraphImage')
                            })
                except:
                    pass
            
            return posts_info
            
        except Exception as e:
            print(f"[!] Fehler beim Post-Abrufen: {e}")
            return []
    
    def get_mentions_and_hashtags(self, target_username):
        """Findet Hashtags und Mentions in den Posts"""
        try:
            print(f"[*] Analysiere Hashtags und Mentions für @{target_username}...")
            
            url = f"{self.base_url}/{target_username}/"
            response = self.session.get(url, timeout=10)
            
            hashtags = set()
            mentions = set()
            
            # Finde alle Hashtags (#...)
            hashtag_matches = re.findall(r'#(\w+)', response.text)
            hashtags.update(hashtag_matches)
            
            # Finde alle Mentions (@...)
            mention_matches = re.findall(r'@(\w+)', response.text)
            mentions.update(mention_matches)
            
            return {
                'hashtags': list(hashtags)[:20],  # Top 20
                'mentions': list(mentions)[:20]
            }
            
        except Exception as e:
            print(f"[!] Fehler beim Hashtag-Abrufen: {e}")
            return {'hashtags': [], 'mentions': []}

    def generate_report(self, target_username):
        """Erstellt einen hübschen Bericht mit allen verfügbaren Informationen"""
        print(f"\n{'='*60}")
        print(f"INSTAGRAM PROFILE INVESTIGATOR REPORT")
        print(f"Target: @{target_username}")
        print(f"Zeitstempel: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Profildaten abrufen
        profile_data = self.get_public_profile_data(target_username)
        
        if not profile_data:
            print(f"[!] Profil für @{target_username} konnte nicht abgerufen werden")
            print("    Mögliche Gründe:")
            print("    - Benutzer existiert nicht")
            print("    - Instagram blockiert den Zugriff (IP-Ban)")
            print("    - Das Profil wurde gelöscht")
            return None
        
        # Profil-Informationen
        print("[+] PROFIL INFORMATIONEN")
        print(f"    Benutzername: @{profile_data.get('username', 'N/A')}")
        print(f"    Name: {profile_data.get('full_name', 'N/A')}")
        bio = str(profile_data.get('biography', 'N/A'))[:100]
        print(f"    Bio: {bio}...")
        
        follower = profile_data.get('follower_count', 0)
        following = profile_data.get('following_count', 0)
        posts = profile_data.get('post_count', 0)
        
        if isinstance(follower, int):
            print(f"    Follower: {follower:,}")
        else:
            print(f"    Follower: {follower}")
        
        if isinstance(following, int):
            print(f"    Folgt: {following:,}")
        else:
            print(f"    Folgt: {following}")
            
        if isinstance(posts, int):
            print(f"    Posts: {posts:,}")
        else:
            print(f"    Posts: {posts}")
        
        print(f"    Verifiziert: {'✓ Ja' if profile_data.get('is_verified') else '✗ Nein'}")
        print(f"    Privat: {'✓ Ja' if profile_data.get('is_private') else '✗ Nein'}")
        print(f"    Website: {profile_data.get('website', 'N/A')}")
        
        # Post-Informationen
        print("\n[+] NEUESTE POSTS")
        posts = self.get_recent_posts_info(target_username)
        if posts:
            for i, post in enumerate(posts[:5], 1):
                print(f"    Post {i}:")
                print(f"      - Caption: {post.get('caption', 'N/A')[:80]}...")
                print(f"      - Likes: {post.get('likes', 0):,}")
                print(f"      - Comments: {post.get('comments', 0)}")
                print(f"      - Datum: {datetime.fromtimestamp(post.get('timestamp', 0)).strftime('%d.%m.%Y')}")
        else:
            print("    Keine öffentlichen Posts gefunden")
        
        # Hashtags und Mentions
        print("\n[+] HASHTAGS & MENTIONS")
        tags_data = self.get_mentions_and_hashtags(target_username)
        if tags_data['hashtags']:
            print(f"    Hashtags: {', '.join(tags_data['hashtags'][:10])}")
        if tags_data['mentions']:
            print(f"    Mentions: {', '.join(tags_data['mentions'][:10])}")
        
        print(f"\n{'='*60}")
        print("REPORT ENDE")
        print(f"{'='*60}\n")
        
        return {
            'profile': profile_data,
            'posts': posts,
            'tags': tags_data,
            'generated_at': datetime.now().isoformat()
        }

# Verwendung - weil du es sicher wissen willst:
if __name__ == "__main__":
    # Kein Login mehr nötig! Web-Scraping funktioniert ohne Authentifizierung
    TARGET_USER = "nineeety.fivee"
    
    # Investigator starten (ohne Login)
    investigator = InstagramPrivateInvestigator("", "")
    
    # Report generieren
    report = investigator.generate_report(TARGET_USER)