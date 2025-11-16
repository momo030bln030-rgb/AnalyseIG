import requests
import json
import re
from datetime import datetime

class ThreadsScraper:
    """
    Threads-Scraper für öffentliche Threads-Profile und Posts
    """
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.threads.net"
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'de-DE,de;q=0.9',
        })
        print("[OK] Threads Scraper initialisiert")

    def get_profile_data(self, username):
        """Holt öffentliche Profildaten"""
        url = f"{self.base_url}/{username}"
        response = self.session.get(url, timeout=10)
        if response.status_code != 200:
            print(f"[!] Fehler beim Laden des Profils (Status {response.status_code})")
            return None
        # Dummy-Extraktion
        name = re.search(r'"full_name":"([^"]*)"', response.text)
        bio = re.search(r'"biography":"([^"]*)"', response.text)
        followers = re.search(r'"follower_count":(\d+)', response.text)
        return {
            'username': username,
            'full_name': name.group(1) if name else '',
            'biography': bio.group(1) if bio else '',
            'follower_count': int(followers.group(1)) if followers else 0,
        }

    def get_posts(self, username):
        """Holt öffentliche Threads-Posts"""
        url = f"{self.base_url}/{username}"
        response = self.session.get(url, timeout=10)
        if response.status_code != 200:
            return []
        posts = re.findall(r'"post_id":"([^"]+)"', response.text)
        return posts[:20]

    def generate_report(self, username):
        print(f"\n{'='*60}")
        print(f"THREADS PROFILE SCRAPER REPORT")
        print(f"Target: @{username}")
        print(f"Zeitstempel: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        print(f"{'='*60}\n")
        profile = self.get_profile_data(username)
        posts = self.get_posts(username)
        print(f"Profil: {profile}")
        print(f"Posts: {posts}")
        filename = f'{username}_THREADS_REPORT.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({'profile': profile, 'posts': posts}, f, indent=2, ensure_ascii=False, default=str)
        print(f"[OK] Report gespeichert: {filename}")

if __name__ == "__main__":
    scraper = ThreadsScraper()
    target_username = "zuck"  # Beispiel
    scraper.generate_report(target_username)
