from __future__ import annotations

from dataclasses import dataclass
from markdown_it import MarkdownIt


@dataclass
class TOCItem:
    level: int
    text: str
    anchor: str


def extract_toc(text: str) -> list[TOCItem]:
    """Extract table of contents from markdown text.
    
    Parses headings and generates anchor IDs for navigation.
    """
    md = MarkdownIt("commonmark")
    tokens = md.parse(text)
    
    toc_items: list[TOCItem] = []
    
    for i, token in enumerate(tokens):
        if token.type == "heading_open":
            level = int(token.tag[1])  # h1 -> 1, h2 -> 2, etc.
            
            # Get the text content from the next token
            if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
                heading_text = tokens[i + 1].content
                
                # Generate anchor from heading text (simple slug)
                anchor = heading_text.lower().replace(" ", "-").replace("'", "")
                # Remove special characters except hyphens
                anchor = "".join(c for c in anchor if c.isalnum() or c == "-")
                
                toc_items.append(TOCItem(level=level, text=heading_text, anchor=anchor))
    
    return toc_items
