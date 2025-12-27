import re
from typing import Dict, List, Tuple
from markdown import markdown
from bs4 import BeautifulSoup


class ContentParser:
    """
    Service to parse and extract structured information from content.
    """
    def __init__(self):
        pass

    def parse_markdown_headers(self, content: str) -> List[Dict[str, str]]:
        """
        Parse markdown content to extract headers and their content.
        """
        lines = content.split('\n')
        headers = []
        current_header = None
        current_content = []

        for line in lines:
            # Check for markdown headers (##, ###, etc.)
            header_match = re.match(r'^(#+)\s+(.+)', line)
            if header_match:
                # If we have a previous header, save it
                if current_header:
                    headers.append({
                        'level': len(current_header['marker']),
                        'title': current_header['title'],
                        'content': '\n'.join(current_content).strip()
                    })

                # Start new header
                current_header = {
                    'marker': header_match.group(1),
                    'title': header_match.group(2)
                }
                current_content = []
            else:
                current_content.append(line)

        # Don't forget the last header
        if current_header:
            headers.append({
                'level': len(current_header['marker']),
                'title': current_header['title'],
                'content': '\n'.join(current_content).strip()
            })

        return headers

    def extract_sections(self, content: str) -> List[Dict[str, str]]:
        """
        Extract sections from content based on headers.
        """
        headers = self.parse_markdown_headers(content)
        sections = []

        for header in headers:
            section = {
                'title': header['title'],
                'content': header['content'],
                'level': header['level']
            }
            sections.append(section)

        return sections

    def clean_content(self, content: str) -> str:
        """
        Clean content by removing markdown syntax and normalizing text.
        """
        # Convert markdown to HTML
        html = markdown(content)

        # Parse HTML and extract text
        soup = BeautifulSoup(html, 'html.parser')
        clean_text = soup.get_text()

        # Normalize whitespace
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()

        return clean_text

    def extract_metadata(self, content: str) -> Dict[str, str]:
        """
        Extract metadata from content (like frontmatter if present).
        """
        metadata = {}

        # Look for YAML frontmatter
        frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.search(frontmatter_pattern, content, re.DOTALL | re.MULTILINE)

        if match:
            frontmatter = match.group(1)
            # Parse simple key-value pairs
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()

        return metadata

    def count_words(self, content: str) -> int:
        """
        Count words in content.
        """
        clean_content = self.clean_content(content)
        return len(clean_content.split())