#!/usr/bin/env python3
"""
TikTok Kommentare-Scraper (Minimalversion)
Extrahiert Kommentare von einem TikTok-Video
"""
import requests
import re

class TikTokCommentsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'de-DE,de;q=0.9',
        })

    def get_comments(self, video_url):
        """Holt öffentliche Kommentare (rudimentär)"""
        response = self.session.get(video_url, timeout=10)
        if response.status_code != 200:
            print(f"[!] Fehler beim Laden des Videos ({response.status_code})")
            return []
        html = response.text
        # Extrahiere Kommentare (rudimentär, da TikTok dynamisch ist)
        comments = re.findall(r'"comment":"([^"]+)"', html)
        usernames = re.findall(r'"uniqueId":"([^"]+)"', html)
        result = []
        for i, comment in enumerate(comments):
            result.append({
                'username': usernames[i] if i < len(usernames) else 'N/A',
                'text': comment
            })
        return result

if __name__ == '__main__':
    scraper = TikTokCommentsScraper()
    video_url = input("TikTok Video-URL: ").strip()
    comments = scraper.get_comments(video_url)
    print(comments)
