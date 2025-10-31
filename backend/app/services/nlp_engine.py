import re

class SimpleNLP:
    """Lightweight NLP: intent extraction + improved sentiment-ish scoring."""
    
    POSITIVE = set(["love","enjoy","like","excited","interested","passionate","great","awesome","good","fond","really","very"])
    NEGATIVE = set(["hate","dislike","bored","boring","dont","don't","not","hard","difficult","confused","struggle","worried"])
    INTENSIFIERS = set(["really","very","extremely","super","absolutely","totally"])

    def normalize(self, text: str) -> str:
        if not isinstance(text, str):
            return ""
        return re.sub(r"[^a-z0-9 ]"," ", text.lower())

    def extract_keywords(self, text: str) -> set:
        text = self.normalize(text)
        return set([w for w in text.split() if len(w) > 2])

    def sentiment_score(self, text: str) -> float:
        t = self.normalize(text)
        words = t.split()
        pos = sum(1 for w in words if w in self.POSITIVE)
        neg = sum(1 for w in words if w in self.NEGATIVE)
        inten = sum(1 for w in words if w in self.INTENSIFIERS)
        
        if pos + neg == 0:
            return 0.0
        
        base = (pos - neg) / (pos + neg)
        # Boost if intensifiers present
        if inten > 0:
            base = base * (1 + (inten * 0.2))
        return max(-1.0, min(1.0, base))

    def extract_intent(self, text: str) -> dict:
        """Extract educational intent from response"""
        t = self.normalize(text)
        keywords = self.extract_keywords(text)
        
        # Technical intent
        tech_words = {"computer", "programming", "coding", "software", "technology", "data", "engineering"}
        # Creative intent
        creative_words = {"design", "art", "creative", "drawing", "music", "writing", "fashion"}
        # Business intent
        business_words = {"business", "marketing", "management", "entrepreneur", "sales", "commerce"}
        # Medical intent
        medical_words = {"medical", "doctor", "nurse", "health", "biology", "medicine", "patient"}
        
        intent = {
            "technical": len(keywords & tech_words),
            "creative": len(keywords & creative_words),
            "business": len(keywords & business_words),
            "medical": len(keywords & medical_words),
            "sentiment": self.sentiment_score(text)
        }
        
        return intent