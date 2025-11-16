#!/usr/bin/env python3
"""
OSINT Tools für Instagram & Social Media
Erweiterte Scraping, Analyse und Export-Funktionalität
"""

import requests
import json
import re
import csv
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import quote

# Importiere Sentiment Analyzer
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

try:
    from sentiment_analyzer import SentimentAnalyzer, analyze_comments_sentiment
    SENTIMENT_AVAILABLE = True
except ImportError:
    SENTIMENT_AVAILABLE = False


class InstagramOSINT:
    """OSINT-Tools für Instagram mit erweiterten Funktionen"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'de-DE,de;q=0.9',
        })
        self.sentiment_analyzer = SentimentAnalyzer() if SENTIMENT_AVAILABLE else None
        print("[OK] Instagram OSINT Tools initialisiert")
    
    def scrape_comments_deep(self, username: str, post_limit: int = 10) -> List[Dict]:
        """
        Tiefes Scraping von Kommentaren (mehrere Posts)
        
        Args:
            username: Instagram Benutzername
            post_limit: Maximale Anzahl Posts zum Scrapen
        
        Returns:
            Liste aller Kommentare mit Metadata
        """
        print(f"\n[*] Starte tiefes Kommentar-Scraping für @{username}...")
        
        all_comments = []
        
        try:
            url = f"https://www.instagram.com/{username}/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                print(f"[!] Profil nicht erreichbar")
                return []
            
            # Extrahiere Posts
            shortcodes = re.findall(r'"shortcode":"([A-Za-z0-9_-]+)"', response.text)
            shortcodes = shortcodes[:post_limit]
            
            print(f"[*] Gefunden: {len(shortcodes)} Posts")
            
            for i, shortcode in enumerate(shortcodes, 1):
                print(f"[*] Scrape Post {i}/{len(shortcodes)}...")
                
                try:
                    post_url = f"https://www.instagram.com/p/{shortcode}/"
                    post_response = self.session.get(post_url, timeout=10)
                    
                    if post_response.status_code != 200:
                        continue
                    
                    # Extrahiere Kommentare
                    usernames = re.findall(r'"username":"([^"]+)"', post_response.text)
                    texts = re.findall(r'"text":"([^"]*)"', post_response.text)
                    timestamps = re.findall(r'"created_at":(\d+)', post_response.text)
                    likes = re.findall(r'"edge_liked_by":\{"count":(\d+)', post_response.text)
                    
                    for j in range(min(50, len(usernames))):
                        try:
                            comment = {
                                'post_id': shortcode,
                                'post_url': post_url,
                                'username': usernames[j],
                                'text': texts[j] if j < len(texts) else '',
                                'likes': int(likes[j]) if j < len(likes) else 0,
                                'timestamp': int(timestamps[j]) if j < len(timestamps) else 0,
                                'date': datetime.fromtimestamp(int(timestamps[j])).isoformat() if j < len(timestamps) else 'N/A',
                            }
                            
                            # Sentiment-Analyse falls verfügbar
                            if self.sentiment_analyzer and texts[j]:
                                sentiment = self.sentiment_analyzer.analyze(texts[j])
                                comment['sentiment'] = sentiment['sentiment']
                                comment['sentiment_score'] = sentiment['score']
                                comment['sentiment_polarity'] = sentiment['polarity']
                                comment['emotion'] = sentiment['emotion']
                            
                            all_comments.append(comment)
                        except:
                            continue
                    
                    print(f"    [+] {min(50, len(usernames))} Kommentare gefunden")
                    
                except Exception as e:
                    print(f"    [!] Fehler: {e}")
                    continue
        
        except Exception as e:
            print(f"[!] Fehler beim Scraping: {e}")
        
        print(f"\n[OK] Insgesamt {len(all_comments)} Kommentare gescraped")
        return all_comments
    
    def filter_comments(self, comments: List[Dict], filters: Dict) -> List[Dict]:
        """
        Filtert Kommentare nach verschiedenen Kriterien
        
        Args:
            comments: Liste von Kommentaren
            filters: {
                'min_likes': int,
                'max_likes': int,
                'username': str (regex),
                'text_contains': str (regex),
                'sentiment': str ('positive', 'negative', 'neutral'),
                'min_sentiment_score': float,
                'emotion': str
            }
        """
        filtered = comments
        
        if 'min_likes' in filters:
            filtered = [c for c in filtered if c.get('likes', 0) >= filters['min_likes']]
        
        if 'max_likes' in filters:
            filtered = [c for c in filtered if c.get('likes', 0) <= filters['max_likes']]
        
        if 'username' in filters:
            pattern = re.compile(filters['username'], re.IGNORECASE)
            filtered = [c for c in filtered if pattern.search(c['username'])]
        
        if 'text_contains' in filters:
            pattern = re.compile(filters['text_contains'], re.IGNORECASE)
            filtered = [c for c in filtered if pattern.search(c['text'])]
        
        if 'sentiment' in filters and SENTIMENT_AVAILABLE:
            filtered = [c for c in filtered if c.get('sentiment') == filters['sentiment']]
        
        if 'min_sentiment_score' in filters and SENTIMENT_AVAILABLE:
            filtered = [c for c in filtered if c.get('sentiment_score', 0) >= filters['min_sentiment_score']]
        
        if 'emotion' in filters and SENTIMENT_AVAILABLE:
            filtered = [c for c in filtered if c.get('emotion') == filters['emotion']]
        
        return filtered
    
    def export_comments_csv(self, comments: List[Dict], filename: str) -> bool:
        """Exportiert Kommentare als CSV"""
        try:
            if not comments:
                print("[!] Keine Kommentare zum Exportieren")
                return False
            
            keys = comments[0].keys()
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(comments)
            
            print(f"[OK] Exportiert nach: {filename}")
            return True
        except Exception as e:
            print(f"[!] Export-Fehler: {e}")
            return False
    
    def export_comments_excel(self, comments: List[Dict], filename: str) -> bool:
        """Exportiert Kommentare als Excel"""
        try:
            if not comments:
                print("[!] Keine Kommentare zum Exportieren")
                return False
            
            df = pd.DataFrame(comments)
            df.to_excel(filename, index=False, engine='openpyxl')
            
            print(f"[OK] Exportiert nach: {filename}")
            return True
        except Exception as e:
            print(f"[!] Excel-Export-Fehler: {e}")
            return False
    
    def export_comments_json(self, comments: List[Dict], filename: str) -> bool:
        """Exportiert Kommentare als JSON"""
        try:
            if not comments:
                print("[!] Keine Kommentare zum Exportieren")
                return False
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(comments, f, indent=2, ensure_ascii=False)
            
            print(f"[OK] Exportiert nach: {filename}")
            return True
        except Exception as e:
            print(f"[!] JSON-Export-Fehler: {e}")
            return False
    
    def analyze_comment_patterns(self, comments: List[Dict]) -> Dict:
        """
        Analysiert Muster in Kommentaren
        
        Returns:
            {
                'total': int,
                'unique_users': int,
                'avg_likes': float,
                'top_commenters': List[Dict],
                'most_liked_comments': List[Dict],
                'sentiment_distribution': Dict (if available),
                'common_words': List[str]
            }
        """
        if not comments:
            return {}
        
        result = {
            'total': len(comments),
            'unique_users': len(set(c['username'] for c in comments)),
            'avg_likes': round(sum(c['likes'] for c in comments) / len(comments), 1),
            'max_likes': max(c['likes'] for c in comments),
            'min_likes': min(c['likes'] for c in comments),
        }
        
        # Top Kommentierer
        user_comment_counts = {}
        for c in comments:
            user = c['username']
            user_comment_counts[user] = user_comment_counts.get(user, 0) + 1
        
        top_commenters = sorted(
            [{'username': u, 'count': c} for u, c in user_comment_counts.items()],
            key=lambda x: x['count'],
            reverse=True
        )[:10]
        result['top_commenters'] = top_commenters
        
        # Meistgelikte Kommentare
        most_liked = sorted(comments, key=lambda x: x['likes'], reverse=True)[:5]
        result['most_liked_comments'] = [
            {
                'username': c['username'],
                'text': c['text'][:100],
                'likes': c['likes']
            } for c in most_liked
        ]
        
        # Sentiment-Verteilung
        if SENTIMENT_AVAILABLE:
            sentiments = {}
            for c in comments:
                sent = c.get('sentiment', 'unknown')
                sentiments[sent] = sentiments.get(sent, 0) + 1
            result['sentiment_distribution'] = sentiments
        
        # Häufige Wörter
        all_text = ' '.join(c['text'].lower() for c in comments)
        words = re.findall(r'\b\w+\b', all_text)
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Nur Wörter länger als 3 Zeichen
                word_freq[word] = word_freq.get(word, 0) + 1
        
        common_words = sorted(
            [(w, c) for w, c in word_freq.items()],
            key=lambda x: x[1],
            reverse=True
        )[:20]
        result['common_words'] = common_words
        
        return result
    
    def detect_spam_comments(self, comments: List[Dict]) -> List[Dict]:
        """
        Versucht, Spam-Kommentare zu identifizieren
        
        Returns:
            Liste potentieller Spam-Kommentare
        """
        spam_indicators = {
            'links': r'http[s]?://|www\.|\.com|\.de',
            'all_caps': r'^[A-Z\s!?]{10,}$',
            'repeated': r'(.)\1{3,}',  # aaaa, !!!!
            'gibberish': r'[a-z0-9]{15,}'  # Lange Zeichenfolgen ohne Leerzeichen
        }
        
        spam_list = []
        
        for comment in comments:
            text = comment['text']
            spam_score = 0
            
            if re.search(spam_indicators['links'], text):
                spam_score += 2
            
            if re.search(spam_indicators['all_caps'], text):
                spam_score += 1
            
            if re.search(spam_indicators['repeated'], text):
                spam_score += 1
            
            if re.search(spam_indicators['gibberish'], text):
                spam_score += 1
            
            if spam_score >= 2:
                comment['spam_score'] = spam_score
                spam_list.append(comment)
        
        return spam_list
    
    def reverse_search_username(self, username: str) -> Dict:
        """
        Reverse OSINT für Instagram-Benutzer
        Generiert Links zu verschiedenen Reverse-Search-Tools
        """
        return {
            'instagram_direct': f"https://www.instagram.com/{username}/",
            'google_images': f"https://www.google.com/search?q={quote(username)}&tbm=isch",
            'reverse_search_google': f"https://images.google.com/searchbyimage?q={quote(username)}",
            'tineye': f"https://www.tineye.com/search?q={quote(username)}",
            'yandex': f"https://yandex.com/images/search?text={quote(username)}",
            'bing': f"https://www.bing.com/images/search?q={quote(username)}",
            'whois': f"https://whois.com/whois/{username}",
            'site_search': f"https://www.google.com/search?q=site:instagram.com {quote(username)}",
            'pipl': f"https://pipl.com/search/?q={quote(username)}",
            'spokeo': f"https://www.spokeo.com/search?query={quote(username)}"
        }


def main():
    """Interactive OSINT Tools Menu"""
    
    print("\n" + "="*80)
    print("INSTAGRAM OSINT TOOLS".center(80))
    print("="*80 + "\n")
    
    osint = InstagramOSINT()
    
    while True:
        print("\n[1] Tiefe Kommentar-Analyse")
        print("[2] Kommentare filtern")
        print("[3] Kommentare exportieren")
        print("[4] Spam-Erkennung")
        print("[5] Reverse Username Search")
        print("[6] Beenden")
        
        choice = input("\nWähle Option (1-6): ").strip()
        
        if choice == '1':
            username = input("Instagram-Username: ").strip()
            post_limit = int(input("Maximale Posts (Default: 10): ").strip() or "10")
            
            comments = osint.scrape_comments_deep(username, post_limit)
            
            # Analyse
            if comments:
                patterns = osint.analyze_comment_patterns(comments)
                print("\n" + "="*80)
                print("ANALYSE-ERGEBNISSE")
                print("="*80)
                print(f"Kommentare: {patterns['total']}")
                print(f"Unique Users: {patterns['unique_users']}")
                print(f"Ø Likes: {patterns['avg_likes']}")
                
                if 'sentiment_distribution' in patterns:
                    print(f"Sentiments: {patterns['sentiment_distribution']}")
                
                print(f"\nTop Kommentierer:")
                for u in patterns['top_commenters'][:5]:
                    print(f"  - {u['username']}: {u['count']} Kommentare")
        
        elif choice == '2':
            print("Filter-Optionen:")
            print("  min_likes, max_likes, username, text_contains, sentiment, emotion")
            print("  (z.B.: min_likes=10 username=test)")
            
            filter_input = input("Filter (komma-getrennt): ").strip()
            # Parse filters - simplified
            filters = {}
            print("[i] Filter-Parsing noch nicht implementiert")
        
        elif choice == '3':
            print("[i] Bitte zuerst Kommentare scrapen (Option 1)")
        
        elif choice == '4':
            print("[i] Bitte zuerst Kommentare scrapen (Option 1)")
        
        elif choice == '5':
            username = input("Instagram-Username: ").strip()
            links = osint.reverse_search_username(username)
            
            print("\n" + "="*80)
            print("REVERSE SEARCH LINKS")
            print("="*80)
            for service, url in links.items():
                print(f"{service}: {url}")
        
        elif choice == '6':
            print("[*] OSINT Tools beendet")
            break
        
        else:
            print("[!] Ungültige Auswahl")


if __name__ == '__main__':
    main()
