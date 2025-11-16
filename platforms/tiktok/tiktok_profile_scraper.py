#!/usr/bin/env python3
"""
TikTok Profil-Scraper (Minimalversion)
Extrahiert öffentliche Profildaten eines TikTok-Users
"""
import requests
import re

class TikTokProfileScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'de-DE,de;q=0.9',
        })

    def get_profile_data(self, username):
        """Holt öffentliche Profildaten"""
        url = f"https://www.tiktok.com/@{username}"
        response = self.session.get(url, timeout=10)
        if response.status_code != 200:
            print(f"[!] Fehler beim Laden des Profils ({response.status_code})")
            return None
        html = response.text
        # Extrahiere Follower, Likes, Bio, Name
        follower = re.search(r'"followerCount":(\d+)', html)
        likes = re.search(r'"heartCount":(\d+)', html)
        bio = re.search(r'"signature":"([^"]*)"', html)
        name = re.search(r'"nickname":"([^"]*)"', html)
        return {
            'username': username,
            'name': name.group(1) if name else 'N/A',
            'bio': bio.group(1) if bio else 'N/A',
            'follower_count': int(follower.group(1)) if follower else 0,
            'likes_count': int(likes.group(1)) if likes else 0,
            'profile_url': url
        }

if __name__ == '__main__':
    scraper = TikTokProfileScraper()
    username = input("TikTok Username: ").strip()
    data = scraper.get_profile_data(username)
    print(data)
