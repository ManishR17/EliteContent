"""Utility functions shared across services"""
import re
from typing import List


def count_words(text: str) -> int:
    """Count words in text"""
    return len(text.split())


def calculate_readability(text: str) -> float:
    """
    Calculate Flesch Reading Ease score
    Higher score = easier to read (0-100)
    """
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    
    if len(words) == 0 or len(sentences) == 0:
        return 0.0
    
    # Remove empty sentences
    sentences = [s for s in sentences if s.strip()]
    
    # Count syllables (simplified)
    syllables = sum(_count_syllables(word) for word in words)
    
    # Flesch Reading Ease formula
    words_per_sentence = len(words) / len(sentences)
    syllables_per_word = syllables / len(words)
    
    score = 206.835 - 1.015 * words_per_sentence - 84.6 * syllables_per_word
    
    # Clamp between 0-100
    return max(0.0, min(100.0, score))


def _count_syllables(word: str) -> int:
    """Count syllables in a word (simplified)"""
    word = word.lower()
    vowels = 'aeiouy'
    syllable_count = 0
    previous_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not previous_was_vowel:
            syllable_count += 1
        previous_was_vowel = is_vowel
    
    # Adjust for silent 'e'
    if word.endswith('e'):
        syllable_count -= 1
    
    # Ensure at least 1 syllable
    return max(1, syllable_count)


def extract_hashtags(text: str) -> List[str]:
    """Extract hashtags from text"""
    return re.findall(r'#\w+', text)


def count_characters(text: str, include_spaces: bool = True) -> int:
    """Count characters in text"""
    if include_spaces:
        return len(text)
    return len(text.replace(' ', ''))


def truncate_to_limit(text: str, limit: int, suffix: str = "...") -> str:
    """Truncate text to character limit"""
    if len(text) <= limit:
        return text
    return text[:limit - len(suffix)] + suffix


def generate_seo_score(text: str, keywords: List[str]) -> int:
    """
    Calculate basic SEO score based on keyword presence
    Returns score 0-100
    """
    if not keywords:
        return 50
    
    text_lower = text.lower()
    keyword_count = sum(1 for kw in keywords if kw.lower() in text_lower)
    
    # Calculate percentage
    score = int((keyword_count / len(keywords)) * 100)
    return min(100, score)


def estimate_spam_score(text: str) -> float:
    """
    Estimate spam score for emails (0-100, lower is better)
    Based on spam triggers
    """
    spam_triggers = [
        'free', 'click here', 'limited time', 'act now', 'urgent',
        'winner', 'congratulations', 'cash', 'prize', '$$$',
        'guarantee', 'no risk', '100%', 'amazing', 'incredible'
    ]
    
    text_lower = text.lower()
    trigger_count = sum(1 for trigger in spam_triggers if trigger in text_lower)
    
    # Calculate score
    score = min(100, trigger_count * 15)
    
    # Penalize excessive caps
    if len([c for c in text if c.isupper()]) / max(len(text), 1) > 0.3:
        score += 20
    
    # Penalize excessive exclamation marks
    score += min(30, text.count('!') * 5)
    
    return min(100.0, float(score))


def get_platform_character_limit(platform: str) -> int:
    """Get character limits for different platforms"""
    limits = {
        'twitter': 280,
        'linkedin': 3000,
        'instagram': 2200,
        'facebook': 63206
    }
    return limits.get(platform.lower(), 1000)
