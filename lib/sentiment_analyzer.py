#!/usr/bin/env python3
"""
Sentiment Analysis Module
Analysiert die emotionale Tonalität von Kommentaren (Deutsch & Englisch)
"""

import re
from typing import Dict, List, Tuple

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

try:
    from nltk.sentiment import SentimentIntensityAnalyzer
    import nltk
    try:
        nltk.data.find('sentiment/vader_lexicon')
    except LookupError:
        nltk.download('vader_lexicon', quiet=True)
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False


class SentimentAnalyzer:
    """Analysiert Sentiment in Kommentaren mit mehreren Methoden"""
    
    def __init__(self):
        """Initialisiert den Sentiment-Analyzer"""
        self.german_positive_words = {
            'gut', 'super', 'toll', 'klasse', 'großartig', 'fantastisch', 'wunderbar',
            'hervorragend', 'ausgezeichnet', 'perfekt', 'schön', 'liebe', 'lieben',
            'mag', 'magst', 'awesome', 'amazing', 'great', 'excellent', 'wonderful',
            'fantastic', 'brilliant', 'love', 'lovely', 'beautiful', 'gorgeous',
            'stunning', 'incredible', 'fabulous', 'perfect', 'best', 'nice', 'cool'
        }
        
        self.german_negative_words = {
            'schlecht', 'furchtbar', 'schrecklich', 'hässlich', 'eklig', 'widerlich',
            'hass', 'hasse', 'dumm', 'blöd', 'idiot', 'doof', 'unfähig', 'loser',
            'terrible', 'horrible', 'awful', 'bad', 'ugly', 'hate', 'stupid', 'dumb',
            'idiotic', 'disgusting', 'gross', 'sucks', 'worst', 'disappointing'
        }
        
        self.intensifiers = {
            'sehr', 'so', 'wirklich', 'extrem', 'absolut', 'total', 'mega',
            'super', 'really', 'very', 'extremely', 'absolutely', 'totally'
        }
        
        # VADER-Analyzer laden wenn verfügbar
        if VADER_AVAILABLE:
            self.vader = SentimentIntensityAnalyzer()
        else:
            self.vader = None
    
    def analyze(self, text: str) -> Dict:
        """
        Analysiert den Sentiment eines Kommentars
        
        Returns:
            {
                'polarity': float (-1.0 to 1.0),
                'sentiment': str ('positive', 'negative', 'neutral'),
                'score': float (0.0 to 1.0),
                'confidence': float (0.0 to 1.0),
                'emotion': str ('happy', 'angry', 'sad', 'neutral'),
                'explanation': str,
                'method': str
            }
        """
        if not text or len(text.strip()) == 0:
            return self._neutral_result('Empty text')
        
        # Versuche VADER zuerst (beste Methode)
        if self.vader:
            return self._analyze_vader(text)
        
        # Fallback: TextBlob
        if TEXTBLOB_AVAILABLE:
            return self._analyze_textblob(text)
        
        # Fallback: Custom-Methode
        return self._analyze_custom(text)
    
    def _analyze_vader(self, text: str) -> Dict:
        """VADER SentimentIntensityAnalyzer (beste Methode)"""
        try:
            scores = self.vader.polarity_scores(text)
            compound = scores['compound']  # -1.0 bis 1.0
            
            # Bestimme Sentiment basierend auf compound Score
            if compound >= 0.05:
                sentiment = 'positive'
            elif compound <= -0.05:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            # Bestimme Emotion basierend auf Text
            emotion = self._detect_emotion(text)
            
            # Confidence basierend auf den einzelnen Scores
            confidence = max(scores['pos'], scores['neg'], scores['neu'])
            
            return {
                'polarity': round(compound, 3),
                'sentiment': sentiment,
                'score': round(abs(compound), 3),
                'confidence': round(confidence, 3),
                'emotion': emotion,
                'explanation': f"Sentiment: {sentiment} | Compound Score: {compound:.2f}",
                'method': 'VADER'
            }
        except Exception as e:
            return self._neutral_result(f'VADER error: {e}')
    
    def _analyze_textblob(self, text: str) -> Dict:
        """TextBlob Sentiment Analysis"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1.0 bis 1.0
            subjectivity = blob.sentiment.subjectivity  # 0.0 bis 1.0
            
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            emotion = self._detect_emotion(text)
            confidence = 1.0 - subjectivity  # Objektivität als Confidence
            
            return {
                'polarity': round(polarity, 3),
                'sentiment': sentiment,
                'score': round(abs(polarity), 3),
                'confidence': round(confidence, 3),
                'emotion': emotion,
                'explanation': f"Sentiment: {sentiment} | Polarity: {polarity:.2f} | Subjectivity: {subjectivity:.2f}",
                'method': 'TextBlob'
            }
        except Exception as e:
            return self._neutral_result(f'TextBlob error: {e}')
    
    def _analyze_custom(self, text: str) -> Dict:
        """Einfache Custom-Methode (Fallback)"""
        text_lower = text.lower()
        
        # Zähle positive und negative Wörter
        positive_count = sum(1 for word in self.german_positive_words if word in text_lower)
        negative_count = sum(1 for word in self.german_negative_words if word in text_lower)
        
        # Prüfe auf Intensivierungen
        has_intensifier = any(word in text_lower for word in self.intensifiers)
        if has_intensifier:
            positive_count *= 1.5
            negative_count *= 1.5
        
        # Berechne Polarity
        total = positive_count + negative_count
        if total == 0:
            polarity = 0.0
            sentiment = 'neutral'
            confidence = 0.3
        else:
            polarity = (positive_count - negative_count) / total
            if polarity > 0.3:
                sentiment = 'positive'
            elif polarity < -0.3:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            confidence = min(abs(polarity), 1.0)
        
        emotion = self._detect_emotion(text)
        
        return {
            'polarity': round(polarity, 3),
            'sentiment': sentiment,
            'score': round(abs(polarity), 3),
            'confidence': round(confidence, 3),
            'emotion': emotion,
            'explanation': f"Keyword-basiert: {positive_count} positive, {negative_count} negative Wörter",
            'method': 'Custom (Keyword)'
        }
    
    def _detect_emotion(self, text: str) -> str:
        """Erkennt primäre Emotion im Text"""
        text_lower = text.lower()
        
        emotion_keywords = {
            'happy': ['😊', '😄', '😃', 'happy', 'glücklich', 'fröhlich', 'freude', 'wunderbar', ':)', 'lol', 'haha'],
            'angry': ['😠', '😡', 'angry', 'böse', 'wütend', 'zorn', 'aggressiv', '😤', 'grrr', 'scheiß', 'fuck'],
            'sad': ['😢', '😭', 'sad', 'traurig', 'unglücklich', 'depressiv', '🥺', 'leider', 'schlimm'],
            'confused': ['😕', 'confused', 'verwirrt', 'was', 'huh', '?', 'versteh ich nicht'],
            'surprised': ['😮', 'surprised', 'überrascht', 'wow', 'omg', 'unglaublich', '😲'],
        }
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return emotion
        
        return 'neutral'
    
    def _neutral_result(self, explanation: str = 'Unable to analyze') -> Dict:
        """Gibt neutrales Ergebnis zurück"""
        return {
            'polarity': 0.0,
            'sentiment': 'neutral',
            'score': 0.0,
            'confidence': 0.0,
            'emotion': 'neutral',
            'explanation': explanation,
            'method': 'Neutral (Default)'
        }
    
    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """Analysiert mehrere Kommentare auf einmal"""
        results = []
        for text in texts:
            results.append(self.analyze(text))
        return results
    
    def get_summary_stats(self, analyses: List[Dict]) -> Dict:
        """Gibt Zusammenfassung der Sentiment-Analyse"""
        if not analyses:
            return {}
        
        positive = len([a for a in analyses if a['sentiment'] == 'positive'])
        negative = len([a for a in analyses if a['sentiment'] == 'negative'])
        neutral = len([a for a in analyses if a['sentiment'] == 'neutral'])
        
        avg_polarity = sum(a['polarity'] for a in analyses) / len(analyses) if analyses else 0
        avg_score = sum(a['score'] for a in analyses) / len(analyses) if analyses else 0
        
        emotion_counts = {}
        for a in analyses:
            emotion = a['emotion']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        most_common_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else 'neutral'
        
        return {
            'total_comments': len(analyses),
            'positive_count': positive,
            'negative_count': negative,
            'neutral_count': neutral,
            'positive_percentage': round(positive / len(analyses) * 100, 1) if analyses else 0,
            'negative_percentage': round(negative / len(analyses) * 100, 1) if analyses else 0,
            'neutral_percentage': round(neutral / len(analyses) * 100, 1) if analyses else 0,
            'average_polarity': round(avg_polarity, 3),
            'average_score': round(avg_score, 3),
            'most_common_emotion': most_common_emotion,
            'emotion_distribution': emotion_counts
        }


def analyze_comments_sentiment(comments: List[Dict]) -> List[Dict]:
    """
    Hilfsfunktion zum Analysieren von Kommentaren aus ig_complete.py
    
    Args:
        comments: Liste von Kommentar-Dicts mit 'text_full' Key
    
    Returns:
        Erweiterte Kommentar-Liste mit Sentiment-Daten
    """
    analyzer = SentimentAnalyzer()
    
    for comment in comments:
        if 'text_full' in comment:
            sentiment_data = analyzer.analyze(comment['text_full'])
            comment['sentiment'] = sentiment_data['sentiment']
            comment['sentiment_score'] = sentiment_data['score']
            comment['sentiment_polarity'] = sentiment_data['polarity']
            comment['emotion'] = sentiment_data['emotion']
            comment['sentiment_confidence'] = sentiment_data['confidence']
            comment['sentiment_method'] = sentiment_data['method']
    
    return comments


if __name__ == '__main__':
    # Test
    analyzer = SentimentAnalyzer()
    
    test_comments = [
        "Das ist wunderbar! Ich liebe es 😊",
        "Furchtbar, absolut schrecklich!",
        "Das ist okay, nichts Besonderes",
        "Amazing work! Love this! 🎉",
        "Hasse das! Worst thing ever 😠"
    ]
    
    print("="*80)
    print("SENTIMENT ANALYSIS TEST")
    print("="*80)
    
    analyses = analyzer.batch_analyze(test_comments)
    
    for comment, analysis in zip(test_comments, analyses):
        print(f"\nText: {comment}")
        print(f"  Sentiment: {analysis['sentiment']} (Score: {analysis['score']})")
        print(f"  Polarity: {analysis['polarity']}")
        print(f"  Emotion: {analysis['emotion']}")
        print(f"  Method: {analysis['method']}")
    
    stats = analyzer.get_summary_stats(analyses)
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    print(f"Positive: {stats['positive_count']} ({stats['positive_percentage']}%)")
    print(f"Negative: {stats['negative_count']} ({stats['negative_percentage']}%)")
    print(f"Neutral: {stats['neutral_count']} ({stats['neutral_percentage']}%)")
    print(f"Average Polarity: {stats['average_polarity']}")
    print(f"Most Common Emotion: {stats['most_common_emotion']}")
