import requests
import json
import re
from datetime import datetime

class InstagramInvestigator:
    """
    FUNKTIONSFÄHIGE Instagram-Profile Analyse mit öffentlichen APIs
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        print("[✓] Instagram Investigator initialisiert (No-Auth Version)")
        
    def get_profile_via_url(self, username):
        """
        Holt Profildaten direkt von Instagram (funktioniert für öffentliche Profile)
        """
        try:
            # Methode 1: Versuche Daten aus der HTML-Seite zu extrahieren
            url = f"https://www.instagram.com/{username}/"
            
            print(f"[*] Rufe Profil auf: {url}")
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                # Versuche JSON aus HTML zu extrahieren
                import re
                
                # Suche nach JSON patterns in der HTML
                patterns = [
                    r'<script type="application/ld\+json">(.*?)</script>',
                    r'"profile_pic_url":"([^"]+)"',
                    r'"edge_followed_by":\{"count":(\d+)',
                    r'"edge_follow":\{"count":(\d+)',
                    r'"edge_owner_to_timeline_media":\{"count":(\d+)',
                    r'"is_private":(\w+)',
                    r'"is_verified":(\w+)',
                    r'"full_name":"([^"]*)"',
                    r'"biography":"([^"]*)"',
                ]
                
                data = {
                    'username': username,
                    'status': 'partial'
                }
                
                # Extrahiere relevante Daten
                follower_match = re.search(r'"edge_followed_by":\{"count":(\d+)', response.text)
                if follower_match:
                    data['follower_count'] = int(follower_match.group(1))
                
                following_match = re.search(r'"edge_follow":\{"count":(\d+)', response.text)
                if following_match:
                    data['following_count'] = int(following_match.group(1))
                
                post_match = re.search(r'"edge_owner_to_timeline_media":\{"count":(\d+)', response.text)
                if post_match:
                    data['post_count'] = int(post_match.group(1))
                
                name_match = re.search(r'"full_name":"([^"]*)"', response.text)
                if name_match:
                    data['full_name'] = name_match.group(1)
                else:
                    data['full_name'] = 'N/A'
                
                bio_match = re.search(r'"biography":"([^"]*)"', response.text)
                if bio_match:
                    data['biography'] = bio_match.group(1)
                else:
                    data['biography'] = 'N/A'
                
                verified_match = re.search(r'"is_verified":(\w+)', response.text)
                data['is_verified'] = verified_match.group(1) == 'true' if verified_match else False
                
                private_match = re.search(r'"is_private":(\w+)', response.text)
                data['is_private'] = private_match.group(1) == 'true' if private_match else False
                
                # Website
                website_match = re.search(r'"external_url":"([^"]*)"', response.text)
                data['website'] = website_match.group(1) if website_match else 'Keine'
                
                # Profil Bild
                pic_match = re.search(r'"profile_pic_url":"([^"]*)"', response.text)
                data['profile_pic_url'] = pic_match.group(1) if pic_match else ''
                
                # User ID
                id_match = re.search(r'"id":"(\d+)"', response.text)
                data['user_id'] = id_match.group(1) if id_match else ''
                
                print(f"[✓] Daten gefunden: {data}")
                return data
            else:
                print(f"[!] Status Code: {response.status_code}")
                
        except Exception as e:
            print(f"[!] Fehler: {str(e)}")
        
        return None
    
    def get_profile_posts(self, username):
        """Holt die neuesten Posts"""
        try:
            url = f"https://www.instagram.com/{username}/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                posts = []
                
                # Finde alle Post IDs in der HTML
                post_ids = re.findall(r'"id":"(\d+)"', response.text)
                shortcodes = re.findall(r'"shortcode":"([A-Za-z0-9_-]+)"', response.text)
                captions = re.findall(r'"text":"([^"]*)"', response.text)
                timestamps = re.findall(r'"taken_at_timestamp":(\d+)', response.text)
                likes_data = re.findall(r'"edge_likedby":\{"count":(\d+)', response.text)
                comment_data = re.findall(r'"edge_media_to_comment":\{"count":(\d+)', response.text)
                
                # Kombiniere die Daten
                for i in range(min(12, len(shortcodes))):
                    post = {
                        'id': post_ids[i] if i < len(post_ids) else 'N/A',
                        'caption': captions[i][:80] if i < len(captions) else '',
                        'likes': int(likes_data[i]) if i < len(likes_data) else 0,
                        'comments': int(comment_data[i]) if i < len(comment_data) else 0,
                        'timestamp': int(timestamps[i]) if i < len(timestamps) else 0,
                        'shortcode': shortcodes[i] if i < len(shortcodes) else 'N/A'
                    }
                    posts.append(post)
                
                return posts
                
        except Exception as e:
            print(f"[!] Post-Fehler: {str(e)}")
        
        return []
    
    def get_follower_insights(self, username):
        """Analysiert Follower-Muster"""
        try:
            url = f"https://www.instagram.com/{username}/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                # Extrahiere Follower-Daten mit Regex
                follower_match = re.search(r'"edge_followed_by":\{"count":(\d+)', response.text)
                following_match = re.search(r'"edge_follow":\{"count":(\d+)', response.text)
                post_match = re.search(r'"edge_owner_to_timeline_media":\{"count":(\d+)', response.text)
                
                follower_count = int(follower_match.group(1)) if follower_match else 0
                following_count = int(following_match.group(1)) if following_match else 0
                post_count = int(post_match.group(1)) if post_match else 0
                
                ratio = round(follower_count / max(following_count, 1), 2)
                
                return {
                    'follower_count': follower_count,
                    'following_count': following_count,
                    'post_count': post_count,
                    'ratio': ratio,
                    'is_bot_likely': follower_count > 1000000 and post_count < 10
                }
        except Exception as e:
            print(f"[!] Insights-Fehler: {e}")
        
        return {}
    
    def generate_full_report(self, username):
        """Erstellt einen vollständigen Report"""
        print(f"\n{'='*70}")
        print(f"{'INSTAGRAM PROFILE INVESTIGATOR - FINAL REPORT':^70}")
        print(f"{'='*70}\n")
        print(f"Target: @{username}")
        print(f"Zeit: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        
        # SCHRITT 1: Profildaten
        print("[1] PROFIL INFORMATION WIRD GELADEN...")
        profile = self.get_profile_via_url(username)
        
        if not profile:
            print(f"[!] FEHLER: Profil @{username} konnte nicht geladen werden")
            print("    Mögliche Gründe:")
            print("    • Benutzer existiert nicht")
            print("    • Profil ist gelöscht oder deaktiviert")
            print("    • Instagram blockiert den Zugriff (IP-Ban)")
            return None
        
        print(f"[✓] Profil erfolgreich geladen!\n")
        
        print("+"*70)
        print(f"| PROFIL DETAILS")
        print("+"*70)
        print(f"  Benutzername: @{profile.get('username', 'N/A')}")
        print(f"  Name: {profile.get('full_name', 'N/A')}")
        bio = str(profile.get('biography', 'N/A'))[:150]
        print(f"  Bio: {bio}...")
        print(f"  Follower: {profile.get('follower_count', 0):,}")
        print(f"  Folgt: {profile.get('following_count', 0):,}")
        print(f"  Posts: {profile.get('post_count', 0):,}")
        print(f"  Verifiziert: {'✓ JA' if profile.get('is_verified') else '✗ NEIN'}")
        print(f"  Privat: {'✓ JA' if profile.get('is_private') else '✗ NEIN'}")
        print(f"  Website: {profile.get('website', 'Keine')}")
        print(f"  User ID: {profile.get('user_id', 'N/A')}")
        
        # SCHRITT 2: Follower Insights
        print(f"\n[2] FOLLOWER ANALYSE...")
        insights = self.get_follower_insights(username)
        
        if insights:
            print(f"[✓] Analyse abgeschlossen\n")
            print("+"*70)
            print(f"| FOLLOWER STATISTIK")
            print("+"*70)
            print(f"  Follower/Following Ratio: {insights.get('ratio', 'N/A')}")
            print(f"  Potentieller Bot: {'⚠️ WAHRSCHEINLICH' if insights.get('is_bot_likely') else '✓ Wahrscheinlich nicht'}")
        
        # SCHRITT 3: Posts
        print(f"\n[3] POSTS WERDEN GELADEN...")
        posts = self.get_profile_posts(username)
        
        if posts:
            print(f"[✓] {len(posts)} Posts gefunden\n")
            print("+"*70)
            print(f"| NEUESTE POSTS (Top {min(5, len(posts))})")
            print("+"*70)
            
            total_likes = 0
            total_comments = 0
            
            for i, post in enumerate(posts[:5], 1):
                print(f"\n  Post {i}:")
                caption = post.get('caption', '(Kein Text)')[:80]
                print(f"    Caption: {caption}...")
                print(f"    Likes: {post.get('likes', 0):,}")
                print(f"    Kommentare: {post.get('comments', 0)}")
                print(f"    Datum: {datetime.fromtimestamp(post.get('timestamp', 0)).strftime('%d.%m.%Y %H:%M')}")
                print(f"    Link: https://www.instagram.com/p/{post.get('shortcode')}")
                print(f"    Typ: {'Video' if post.get('is_video') else 'Foto'}")
                
                total_likes += post.get('likes', 0)
                total_comments += post.get('comments', 0)
            
            avg_likes = round(total_likes / len(posts[:5]), 0) if posts else 0
            avg_comments = round(total_comments / len(posts[:5]), 0) if posts else 0
            
            print(f"\n  Durchschnitte (Top 5):")
            print(f"    Ø Likes: {avg_likes:,}")
            print(f"    Ø Kommentare: {avg_comments}")
        else:
            print("  [!] Keine Posts gefunden (Privates Profil?)\n")
        
        # ABSCHLUSS
        print(f"\n{'='*70}")
        print(f"{'REPORT ABGESCHLOSSEN':^70}")
        print(f"{'='*70}\n")
        
        return {
            'profile': profile,
            'posts': posts,
            'insights': insights,
            'timestamp': datetime.now().isoformat()
        }

# HAUPTPROGRAMM
if __name__ == "__main__":
    # Erstelle Investigator
    investigator = InstagramInvestigator()
    
    # Target Username
    target = "nineeety.fivee"
    
    # Generiere Report
    report = investigator.generate_full_report(target)
    
    # Optional: Speichere JSON Report
    if report:
        with open(f'{target}_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        print(f"[✓] Report gespeichert: {target}_report.json")
