import requests
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup

class InstagramFullScraper:
    """
    Vollständiger Instagram-Scraper für öffentliche Daten
    - Profile
    - Posts
    - Kommentare
    - Likes
    - Erwähnungen
    - Hashtags
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'de-DE,de;q=0.9',
        })
        print("[OK] Instagram Full Scraper initialisiert")
        
    def get_profile_data(self, username):
        """Holt ALLE öffentlichen Profildaten"""
        try:
            print(f"\n[*] Lade Profil für @{username}...")
            url = f"https://www.instagram.com/{username}/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                print(f"[!] Fehler beim Laden des Profils (Status {response.status_code})")
                return None
            
            # Sichere Feldextraktion
            def safe_int(val):
                try:
                    return int(val) if val else 0
                except:
                    return 0
            
            def safe_bool(val):
                return 'true' in str(val).lower() if val else False
            
            follower = self._extract_field(response.text, r'"edge_followed_by":\{"count":(\d+)')
            following = self._extract_field(response.text, r'"edge_follow":\{"count":(\d+)')
            posts = self._extract_field(response.text, r'"edge_owner_to_timeline_media":\{"count":(\d+)')
            verified = self._extract_field(response.text, r'"is_verified":(\w+)')
            private = self._extract_field(response.text, r'"is_private":(\w+)')
            bio = self._extract_field(response.text, r'"biography":"([^"]*)"')
            name = self._extract_field(response.text, r'"full_name":"([^"]*)"')
            website = self._extract_field(response.text, r'"external_url":"([^"]*)"')
            
            data = {
                'username': username,
                'user_id': self._extract_user_id(response.text),
                'full_name': name or 'N/A',
                'biography': bio or 'N/A',
                'follower_count': safe_int(follower),
                'following_count': safe_int(following),
                'post_count': safe_int(posts),
                'is_verified': safe_bool(verified),
                'is_private': safe_bool(private),
                'website': website or 'Keine',
                'profile_pic_url': self._extract_field(response.text, r'"profile_pic_url":"([^"]*)"') or '',
            }
            
            print(f"[✓] Profil geladen: {data['username']} ({data['follower_count']:,} Follower)")
            return data
            
        except Exception as e:
            print(f"[!] Fehler beim Profil-Abruf: {e}")
            return None
    
    def get_posts(self, username):
        """Holt ALLE öffentlichen Posts mit Details"""
        try:
            print(f"[*] Lade Posts von @{username}...")
            url = f"https://www.instagram.com/{username}/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                return []
            
            posts = []
            
            # Extrahiere Post-Daten
            shortcodes = re.findall(r'"shortcode":"([A-Za-z0-9_-]+)"', response.text)
            captions_raw = re.findall(r'"text":"([^"]*(?:\\.[^"]*)*)"', response.text)
            timestamps = re.findall(r'"taken_at_timestamp":(\d+)', response.text)
            likes = re.findall(r'"edge_likedby":\{"count":(\d+)', response.text)
            comments = re.findall(r'"edge_media_to_comment":\{"count":(\d+)', response.text)
            is_video = re.findall(r'"is_video":(\w+)', response.text)
            
            for i in range(min(30, len(shortcodes))):  # Max 30 Posts
                try:
                    caption = captions_raw[i] if i < len(captions_raw) else ''
                    # Unescape JSON-Zeichen
                    caption = caption.replace('\\n', '\n').replace('\\"', '"')
                    
                    post = {
                        'shortcode': shortcodes[i],
                        'url': f'https://www.instagram.com/p/{shortcodes[i]}',
                        'caption': caption[:200],
                        'caption_full': caption,
                        'likes': int(likes[i]) if i < len(likes) else 0,
                        'comments_count': int(comments[i]) if i < len(comments) else 0,
                        'timestamp': int(timestamps[i]) if i < len(timestamps) else 0,
                        'date': datetime.fromtimestamp(int(timestamps[i])).strftime('%d.%m.%Y %H:%M') if i < len(timestamps) else 'N/A',
                        'is_video': is_video[i] == 'true' if i < len(is_video) else False,
                    }
                    posts.append(post)
                except:
                    continue
            
            print(f"[✓] {len(posts)} Posts gefunden")
            return posts
            
        except Exception as e:
            print(f"[!] Fehler beim Post-Abruf: {e}")
            return []
    
    def get_post_comments(self, shortcode):
        """Holt öffentliche Kommentare zu einem Post"""
        try:
            print(f"[*] Lade Kommentare für Post {shortcode}...")
            url = f"https://www.instagram.com/p/{shortcode}/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                return []
            
            comments = []
            
            # Extrahiere Kommentar-Daten
            usernames = re.findall(r'"username":"([^"]+)"', response.text)
            texts = re.findall(r'"text":"([^"]*)"', response.text)
            timestamps = re.findall(r'"created_at":(\d+)', response.text)
            likes_count = re.findall(r'"edge_liked_by":\{"count":(\d+)', response.text)
            
            for i in range(min(50, len(usernames))):  # Max 50 Kommentare
                try:
                    comment = {
                        'username': usernames[i],
                        'text': texts[i][:150],
                        'text_full': texts[i],
                        'likes': int(likes_count[i]) if i < len(likes_count) else 0,
                        'timestamp': int(timestamps[i]) if i < len(timestamps) else 0,
                        'date': datetime.fromtimestamp(int(timestamps[i])).strftime('%d.%m.%Y %H:%M') if i < len(timestamps) else 'N/A',
                    }
                    comments.append(comment)
                except:
                    continue
            
            print(f"[✓] {len(comments)} Kommentare gefunden")
            return comments
            
        except Exception as e:
            print(f"[!] Fehler beim Kommentar-Abruf: {e}")
            return []
    
    def get_likes_data(self, shortcode):
        """Holt Informationen über Likes (wer hat geliked)"""
        try:
            print(f"[*] Lade Like-Daten für Post {shortcode}...")
            url = f"https://www.instagram.com/p/{shortcode}/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                return {'count': 0, 'liked_by': []}
            
            # Extrahiere Like-Count
            likes_match = re.search(r'"edge_likedby":\{"count":(\d+)', response.text)
            likes_count = int(likes_match.group(1)) if likes_match else 0
            
            # Versuche, Like-Nutzer zu extrahieren
            likers = re.findall(r'"username":"([^"]+)"', response.text)[:20]
            
            return {
                'count': likes_count,
                'sample_likers': likers,
                'note': 'Instagram versteckt meisten Likes - nur Top-Nutzer sichtbar'
            }
            
        except Exception as e:
            print(f"[!] Fehler beim Like-Abruf: {e}")
            return {'count': 0, 'liked_by': []}
    
    def get_mentions_and_hashtags(self, username):
        """Extrahiert Erwähnungen und Hashtags aus Posts"""
        try:
            print(f"[*] Analysiere Hashtags und Erwähnungen von @{username}...")
            url = f"https://www.instagram.com/{username}/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                return {'hashtags': [], 'mentions': []}
            
            # Finde Hashtags
            hashtags = re.findall(r'#([a-zA-Z0-9_]+)', response.text)
            hashtags = list(dict.fromkeys(hashtags))[:50]  # Unique, max 50
            
            # Finde Mentions
            mentions = re.findall(r'@([a-zA-Z0-9_.]+)', response.text)
            mentions = [m for m in mentions if m != username]  # Exclud self
            mentions = list(dict.fromkeys(mentions))[:50]  # Unique, max 50
            
            return {
                'hashtags': hashtags,
                'mentions': mentions,
                'hashtag_count': len(hashtags),
                'mention_count': len(mentions)
            }
            
        except Exception as e:
            print(f"[!] Fehler beim Hashtag-Abruf: {e}")
            return {'hashtags': [], 'mentions': []}
    
    def get_engagement_stats(self, username):
        """Berechnet Engagement-Statistiken"""
        try:
            print(f"[*] Berechne Engagement-Statistiken...")
            profile = self.get_profile_data(username)
            posts = self.get_posts(username)
            
            if not posts:
                return {}
            
            total_likes = sum(p['likes'] for p in posts)
            total_comments = sum(p['comments_count'] for p in posts)
            
            avg_likes = round(total_likes / len(posts), 0) if posts else 0
            avg_comments = round(total_comments / len(posts), 1) if posts else 0
            
            engagement_rate = round((total_likes + total_comments) / (profile['follower_count'] * len(posts)) * 100, 2) if profile['follower_count'] > 0 else 0
            
            return {
                'total_posts_analyzed': len(posts),
                'total_likes': total_likes,
                'total_comments': total_comments,
                'average_likes_per_post': avg_likes,
                'average_comments_per_post': avg_comments,
                'engagement_rate': f"{engagement_rate}%",
                'most_liked_post': max(posts, key=lambda x: x['likes']) if posts else {},
                'most_commented_post': max(posts, key=lambda x: x['comments_count']) if posts else {}
            }
            
        except Exception as e:
            print(f"[!] Fehler bei Engagement-Berechnung: {e}")
            return {}
    
    def _extract_user_id(self, html):
        """Extrahiert User ID aus HTML"""
        match = re.search(r'"id":"(\d+)"', html)
        return match.group(1) if match else 'N/A'
    
    def _extract_field(self, html, pattern):
        """Generische Feld-Extraktion"""
        match = re.search(pattern, html)
        return match.group(1) if match else None
    
    def generate_full_report(self, username):
        """Generiert einen KOMPLETTEN Report mit allen Daten"""
        print(f"\n{'='*80}")
        print(f"{'INSTAGRAM VOLLSTÄNDIGER DATEN-REPORT':^80}")
        print(f"{'='*80}\n")
        print(f"Zielaccount: @{username}")
        print(f"Zeitstempel: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        
        all_data = {
            'target': username,
            'timestamp': datetime.now().isoformat(),
        }
        
        # 1. PROFILDATEN
        print("\n" + "="*80)
        print("1️⃣  PROFILDATEN")
        print("="*80)
        profile = self.get_profile_data(username)
        
        if profile:
            all_data['profile'] = profile
            print(f"Benutzername: @{profile['username']}")
            print(f"Name: {profile['full_name'] or 'N/A'}")
            print(f"Bio: {profile['biography'][:100]}..." if profile['biography'] else "Bio: N/A")
            print(f"Follower: {profile['follower_count']:,}")
            print(f"Folgt: {profile['following_count']:,}")
            print(f"Posts: {profile['post_count']:,}")
            print(f"Verifiziert: {'✓ JA' if profile['is_verified'] else '✗ NEIN'}")
            print(f"Privat: {'✓ JA' if profile['is_private'] else '✗ NEIN'}")
            print(f"Website: {profile['website']}")
            print(f"User ID: {profile['user_id']}")
        else:
            print("[!] Profil konnte nicht geladen werden")
            return None
        
        # 2. POSTS
        print("\n" + "="*80)
        print("2️⃣  ÖFFENTLICHE POSTS")
        print("="*80)
        posts = self.get_posts(username)
        all_data['posts'] = posts
        
        if posts:
            print(f"Gefundene Posts: {len(posts)}\n")
            for i, post in enumerate(posts[:10], 1):
                print(f"Post {i}:")
                print(f"  Link: {post['url']}")
                print(f"  Caption: {post['caption']}...")
                print(f"  Likes: {post['likes']:,}")
                print(f"  Kommentare: {post['comments_count']}")
                print(f"  Datum: {post['date']}")
                print(f"  Typ: {'Video' if post['is_video'] else 'Foto'}")
                print()
        else:
            print("[!] Keine Posts gefunden")
        
        # 3. KOMMENTARE (von ersten Post)
        print("\n" + "="*80)
        print("3️⃣  ÖFFENTLICHE KOMMENTARE")
        print("="*80)
        
        if posts:
            comments = self.get_post_comments(posts[0]['shortcode'])
            all_data['comments_sample'] = comments
            
            if comments:
                print(f"Kommentare von erstem Post ({posts[0]['shortcode']}):\n")
                for i, comment in enumerate(comments[:10], 1):
                    print(f"Kommentar {i}:")
                    print(f"  Von: @{comment['username']}")
                    print(f"  Text: {comment['text']}...")
                    print(f"  Likes: {comment['likes']}")
                    print(f"  Datum: {comment['date']}")
                    print()
            else:
                print("[!] Keine Kommentare gefunden")
        
        # 4. LIKES
        print("\n" + "="*80)
        print("4️⃣  LIKE-INFORMATIONEN")
        print("="*80)
        
        if posts:
            likes_data = self.get_likes_data(posts[0]['shortcode'])
            all_data['likes_info'] = likes_data
            
            print(f"Post: {posts[0]['shortcode']}")
            print(f"Gesamte Likes: {likes_data['count']:,}")
            print(f"Sample Likers: {', '.join([f'@{u}' for u in likes_data.get('sample_likers', [])])}")
            print(f"Note: {likes_data.get('note', '')}")
        
        # 5. HASHTAGS & MENTIONS
        print("\n" + "="*80)
        print("5️⃣  HASHTAGS & ERWÄHNUNGEN")
        print("="*80)
        
        tags_data = self.get_mentions_and_hashtags(username)
        all_data['tags_and_mentions'] = tags_data
        
        if tags_data['hashtags']:
            hashtags_str = ', '.join(f"#{tag}" for tag in tags_data['hashtags'][:20])
            print(f"Hashtags ({len(tags_data['hashtags'])}): {hashtags_str}")
        
        if tags_data['mentions']:
            mentions_str = ', '.join(f"@{m}" for m in tags_data['mentions'][:20])
            print(f"\nErwähnungen ({len(tags_data['mentions'])}): {mentions_str}")
        
        # 6. ENGAGEMENT-STATISTIKEN
        print("\n" + "="*80)
        print("6️⃣  ENGAGEMENT-STATISTIKEN")
        print("="*80)
        
        engagement = self.get_engagement_stats(username)
        all_data['engagement'] = engagement
        
        if engagement:
            print(f"Analysierte Posts: {engagement.get('total_posts_analyzed', 0)}")
            print(f"Gesamt Likes: {engagement.get('total_likes', 0):,}")
            print(f"Gesamt Kommentare: {engagement.get('total_comments', 0)}")
            print(f"Ø Likes pro Post: {engagement.get('average_likes_per_post', 0):,.0f}")
            print(f"Ø Kommentare pro Post: {engagement.get('average_comments_per_post', 0)}")
            print(f"Engagement Rate: {engagement.get('engagement_rate', 'N/A')}")
            
            if engagement.get('most_liked_post'):
                print(f"\nMeist-gelikter Post: {engagement['most_liked_post']['shortcode']} ({engagement['most_liked_post']['likes']:,} Likes)")
            
            if engagement.get('most_commented_post'):
                print(f"Meist-kommentierter Post: {engagement['most_commented_post']['shortcode']} ({engagement['most_commented_post']['comments_count']} Kommentare)")
        
        # 7. ABSCHLUSS & SPEICHERN
        print("\n" + "="*80)
        print("REPORT ABGESCHLOSSEN")
        print("="*80 + "\n")
        
        # Speichere als JSON
        filename = f'{username}_FULL_REPORT.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"[✓] Report gespeichert: {filename}")
        
        return all_data

import requests
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup

class InstagramFullScraper:
    """
    Vollständiger Instagram-Scraper für öffentliche Daten
    - Profile
    - Posts
    - Kommentare
    - Likes
    - Erwähnungen
    - Hashtags
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'de-DE,de;q=0.9',
        })
        print("[OK] Instagram Full Scraper initialisiert")
        
    def get_profile_data(self, username):
        """Holt ALLE öffentlichen Profildaten"""
        try:
            print(f"\n[*] Lade Profil für @{username}...")
            url = f"https://www.instagram.com/{username}/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                print(f"[!] Fehler beim Laden des Profils (Status {response.status_code})")
                return None
            
            # Sichere Feldextraktion
            def safe_int(val):
                try:
                    return int(val) if val else 0
                except:
                    return 0
            
            def safe_bool(val):
                return 'true' in str(val).lower() if val else False
            
            follower = self._extract_field(response.text, r'"edge_followed_by":\{"count":(\d+)')
            following = self._extract_field(response.text, r'"edge_follow":\{"count":(\d+)')
            posts = self._extract_field(response.text, r'"edge_owner_to_timeline_media":\{"count":(\d+)')
            verified = self._extract_field(response.text, r'"is_verified":(\w+)')
            private = self._extract_field(response.text, r'"is_private":(\w+)')
            bio = self._extract_field(response.text, r'"biography":"([^"]*)"')
            name = self._extract_field(response.text, r'"full_name":"([^"]*)"')
            website = self._extract_field(response.text, r'"external_url":"([^"]*)"')
            
            data = {
                'username': username,
                'user_id': self._extract_user_id(response.text),
                'full_name': name or 'N/A',
                'biography': bio or 'N/A',
                'follower_count': safe_int(follower),
                'following_count': safe_int(following),
                'post_count': safe_int(posts),
                'is_verified': safe_bool(verified),
                'is_private': safe_bool(private),
                'website': website or 'Keine',
                'profile_pic_url': self._extract_field(response.text, r'"profile_pic_url":"([^"]*)"') or '',
            }
            
            print(f"[✓] Profil geladen: {data['username']} ({data['follower_count']:,} Follower)")
            return data
            
        except Exception as e:
            print(f"[!] Fehler beim Profil-Abruf: {e}")
            return None

    # ... (rest of the class methods remain unchanged)

    # HAUPTPROGRAMM
    if __name__ == "__main__":
        scraper = InstagramFullScraper()
        
        # ====== KONFIGURATION ======
        target_username = "nineeety.fivee"  # HIER DEINEN WUNSCH-ACCOUNT EINGEBEN
        # ============================
        
        # Generiere vollständigen Report
        report = scraper.generate_full_report(target_username)
        
        # Zusätzliche Einzelnanalysen möglich:
        # posts = scraper.get_posts(target_username)
        # comments = scraper.get_post_comments(posts[0]['shortcode'])
        # engagement = scraper.get_engagement_stats(target_username)
