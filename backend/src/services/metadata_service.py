from typing import Dict, Any, Optional
from datetime import datetime
from ..utils import get_logger
from ..models import BookContent


class MetadataService:
    """
    Service to extract and manage metadata for book content.
    """
    def __init__(self):
        self.logger = get_logger(__name__)

    def extract_metadata(self, content: str, title: str = None) -> Dict[str, Any]:
        """
        Extract metadata from content and title.
        """
        metadata = {
            "title": title,
            "word_count": len(content.split()),
            "character_count": len(content),
            "paragraph_count": len([p for p in content.split('\n\n') if p.strip()]),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "read_time_estimate": self._estimate_read_time(content),
            "tags": self._extract_tags(content),
            "entities": self._extract_entities(content),
            "complexity_score": self._calculate_complexity(content)
        }

        return metadata

    def _estimate_read_time(self, content: str, words_per_minute: int = 200) -> int:
        """
        Estimate read time in minutes based on word count.
        """
        word_count = len(content.split())
        read_time = max(1, word_count // words_per_minute)  # At least 1 minute
        return read_time

    def _extract_tags(self, content: str) -> list:
        """
        Extract tags from content (simple keyword extraction).
        """
        # Simple tag extraction - in a real implementation, this would use NLP
        import re

        # Find capitalized words that might be important terms
        words = content.split()
        potential_tags = set()
        for word in words:
            # Remove punctuation and check if capitalized
            clean_word = re.sub(r'[^\w\s]', '', word)
            if clean_word and clean_word[0].isupper() and len(clean_word) > 3:
                potential_tags.add(clean_word.lower())

        # Common technical terms in AI/robotics context
        technical_terms = [
            'ai', 'artificial', 'intelligence', 'robot', 'robotics', 'ros', 'python',
            'machine', 'learning', 'neural', 'network', 'algorithm', 'data', 'model',
            'training', 'inference', 'perception', 'planning', 'control', 'sensor',
            'actuator', 'humanoid', 'navigation', 'vision', 'language', 'action'
        ]

        tags = [tag for tag in technical_terms if tag in content.lower()]
        tags.extend(list(potential_tags)[:5])  # Add up to 5 potential tags

        return list(set(tags))

    def _extract_entities(self, content: str) -> list:
        """
        Extract named entities from content.
        """
        # Simple entity extraction - in a real implementation, this would use NLP
        import re

        entities = []

        # Look for common patterns
        # Email patterns
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        entities.extend(emails)

        # URL patterns
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
        entities.extend(urls)

        # Version numbers
        versions = re.findall(r'v?\d+\.\d+(?:\.\d+)?', content)
        entities.extend(versions)

        return list(set(entities))

    def _calculate_complexity(self, content: str) -> float:
        """
        Calculate a simple complexity score based on various factors.
        """
        if not content:
            return 0.0

        word_count = len(content.split())
        if word_count == 0:
            return 0.0

        # Calculate average word length
        words = content.split()
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0

        # Calculate sentence complexity (average words per sentence)
        sentences = [s for s in content.split('.') if s.strip()]
        avg_sentence_length = word_count / len(sentences) if sentences else 0

        # Normalize scores to 0-1 range
        length_score = min(avg_word_length / 10, 1.0)  # Max word length of 10
        sentence_score = min(avg_sentence_length / 30, 1.0)  # Max sentence length of 30 words

        # Weighted complexity score
        complexity = (0.4 * length_score) + (0.6 * sentence_score)
        return min(complexity, 1.0)  # Cap at 1.0

    async def update_content_metadata(self, content: BookContent) -> BookContent:
        """
        Update metadata for existing content.
        """
        metadata = self.extract_metadata(content.content, content.title)

        # Update content properties based on metadata
        content.word_count = metadata["word_count"]

        # In a real implementation, we'd update the database
        # For now, just return the content
        return content