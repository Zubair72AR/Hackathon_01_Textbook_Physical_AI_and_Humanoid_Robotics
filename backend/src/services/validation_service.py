from typing import Dict, List, Any
from ..utils import get_logger
from ..exceptions import ValidationError


class ValidationService:
    """
    Service to validate content and ensure it meets quality standards.
    """
    def __init__(self):
        self.logger = get_logger(__name__)

    def validate_content(self, content: str, content_type: str = "markdown") -> Dict[str, Any]:
        """
        Validate content based on type and quality standards.
        """
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "quality_score": 100
        }

        # Check if content is empty
        if not content or len(content.strip()) == 0:
            validation_result["is_valid"] = False
            validation_result["errors"].append("Content cannot be empty")
            validation_result["quality_score"] = 0
            return validation_result

        # Check content length
        if len(content) < 50:  # Minimum 50 characters for meaningful content
            validation_result["warnings"].append("Content is very short (< 50 characters)")
            validation_result["quality_score"] -= 20

        # Check for basic structure (headers, paragraphs, etc.)
        if content_type == "markdown":
            self._validate_markdown(content, validation_result)

        # Check for basic quality metrics
        self._check_quality_metrics(content, validation_result)

        return validation_result

    def _validate_markdown(self, content: str, result: Dict[str, Any]):
        """
        Validate markdown-specific content.
        """
        import re

        # Check for headers
        headers = re.findall(r'^(#+)\s+(.+)$', content, re.MULTILINE)
        if not headers:
            result["warnings"].append("No headers found in markdown content")

        # Check for links
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        if not links:
            result["warnings"].append("No links found in content")

        # Check for code blocks
        code_blocks = re.findall(r'```.*?```', content, re.DOTALL)
        if not code_blocks:
            result["warnings"].append("No code blocks found in content")

    def _check_quality_metrics(self, content: str, result: Dict[str, Any]):
        """
        Check general quality metrics for content.
        """
        # Check for readability
        word_count = len(content.split())
        if word_count < 100:
            result["warnings"].append(f"Content has low word count ({word_count} words)")

        # Check for special characters ratio (might indicate poor quality)
        special_chars = sum(1 for c in content if not c.isalnum() and not c.isspace())
        special_ratio = special_chars / len(content) if content else 0
        if special_ratio > 0.3:  # More than 30% special characters
            result["warnings"].append("High ratio of special characters might indicate poor quality")

        # Adjust quality score based on warnings
        result["quality_score"] -= len(result["warnings"]) * 10
        result["quality_score"] = max(0, result["quality_score"])  # Ensure non-negative

    def validate_book_structure(self, content_id: str, module_id: str, chapter_id: str, section_id: str) -> Dict[str, Any]:
        """
        Validate the book structure for a piece of content.
        """
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": []
        }

        # In a real implementation, this would check if the IDs exist in the database
        # For now, we'll just return a basic validation
        if not all([content_id, module_id, chapter_id, section_id]):
            validation_result["is_valid"] = False
            validation_result["errors"].append("All IDs must be provided")

        return validation_result