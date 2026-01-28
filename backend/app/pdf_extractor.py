"""
PDF Text Extraction Module

This module handles PDF text extraction with position information.
"""
from typing import List, Dict, Any
import pdfplumber
from dataclasses import dataclass


@dataclass
class TextBound:
    """Represents text with its bounding box coordinates."""
    text: str
    x0: float
    y0: float
    x1: float
    y1: float
    page: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "text": self.text,
            "x0": self.x0,
            "y0": self.y0,
            "x1": self.x1,
            "y1": self.y1,
            "page": self.page
        }


class PDFExtractor:
    """Extract text and position information from PDF files."""
    
    def __init__(self, pdf_path: str):
        """
        Initialize PDF extractor.
        
        Args:
            pdf_path: Path to the PDF file
        """
        self.pdf_path = pdf_path
    
    def extract_text_with_bounds(self) -> List[TextBound]:
        """
        Extract text with bounding box information from PDF.
        
        Returns:
            List of TextBound objects containing text and position info
        """
        text_bounds = []
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                words = page.extract_words()
                
                for word in words:
                    text_bound = TextBound(
                        text=word['text'],
                        x0=word['x0'],
                        y0=word['top'],
                        x1=word['x1'],
                        y1=word['bottom'],
                        page=page_num
                    )
                    text_bounds.append(text_bound)
        
        return text_bounds
    
    def extract_full_text(self) -> str:
        """
        Extract all text from PDF without position information.
        
        Returns:
            Full text content of the PDF
        """
        full_text = []
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text.append(text)
        
        return "\n".join(full_text)
