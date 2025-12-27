from typing import List
import re


class ChunkingService:
    def __init__(self):
        pass

    def section_aware_chunk(self, text: str, max_chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """
        Chunk text based on semantic boundaries like sections, paragraphs, etc.
        """
        # First, try to split by common section markers
        sections = self._split_by_sections(text)

        chunks = []
        for section in sections:
            if len(section) <= max_chunk_size:
                chunks.append(section)
            else:
                # If section is too large, split by paragraphs
                paragraphs = self._split_by_paragraphs(section, max_chunk_size, overlap)
                chunks.extend(paragraphs)

        return chunks

    def _split_by_sections(self, text: str) -> List[str]:
        """
        Split text by common section markers (headers, etc.)
        """
        # Split by markdown headers (##, ###, etc.) or other section markers
        # This regex looks for markdown-style headers
        section_pattern = r'(\n#{2,6}\s.*?\n|\n\s*\n\s*Chapter\s+\d+|\n\s*\n\s*Section\s+\d+\.\d+)'

        # Split the text and keep the separators
        parts = re.split(f'({section_pattern})', text)

        sections = []
        current_section = ""

        for part in parts:
            if re.match(section_pattern, part.strip()):
                # This is a section header
                if current_section.strip():
                    sections.append(current_section.strip())
                current_section = part
            else:
                current_section += part

        if current_section.strip():
            sections.append(current_section.strip())

        # Combine small sections with the next one to avoid tiny chunks
        combined_sections = []
        i = 0
        while i < len(sections):
            section = sections[i]
            # If this section is small and there's a next section, combine them
            if (len(section) < 200 and i + 1 < len(sections) and
                len(sections[i + 1]) + len(section) < 1500):
                combined_sections.append(section + "\n" + sections[i + 1])
                i += 2  # Skip next section since we combined it
            else:
                combined_sections.append(section)
                i += 1

        return combined_sections

    def _split_by_paragraphs(self, text: str, max_chunk_size: int, overlap: int) -> List[str]:
        """
        Split text by paragraphs if it's too large for a single chunk.
        """
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:
            # If adding this paragraph would exceed the chunk size
            if len(current_chunk) + len(paragraph) > max_chunk_size:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())

                # If the paragraph itself is larger than max_chunk_size,
                # we need to split it further
                if len(paragraph) > max_chunk_size:
                    sub_chunks = self._split_large_paragraph(paragraph, max_chunk_size, overlap)
                    chunks.extend(sub_chunks)
                    current_chunk = ""
                else:
                    current_chunk = paragraph
            else:
                current_chunk += "\n\n" + paragraph

        # Add the last chunk if it exists
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def _split_large_paragraph(self, paragraph: str, max_chunk_size: int, overlap: int) -> List[str]:
        """
        Split a large paragraph into smaller chunks.
        """
        sentences = re.split(r'(?<=[.!?])\s+', paragraph)
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) > max_chunk_size:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())

                # Start a new chunk, potentially with overlap from the previous chunk
                if overlap > 0 and current_chunk:
                    # Get the last part of the previous chunk for overlap
                    overlap_text = current_chunk[-overlap:]
                    current_chunk = overlap_text + " " + sentence
                else:
                    current_chunk = sentence
            else:
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks