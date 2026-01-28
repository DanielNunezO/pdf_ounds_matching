"""
Matching Strategies Module

Implements Strategy Pattern for different text matching algorithms.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from rapidfuzz import fuzz, process
from .pdf_extractor import TextBound


class MatchResult:
    """Represents a match result with confidence score."""
    
    def __init__(self, text_bound: TextBound, confidence: float, context: Optional[str] = None):
        """
        Initialize match result.
        
        Args:
            text_bound: The matched text with bounds
            confidence: Confidence score (0-100)
            context: Optional context information
        """
        self.text_bound = text_bound
        self.confidence = confidence
        self.context = context
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            "match": self.text_bound.to_dict(),
            "confidence": self.confidence
        }
        if self.context:
            result["context"] = self.context
        return result


class MatchingStrategy(ABC):
    """Abstract base class for matching strategies."""
    
    @abstractmethod
    def match(self, entity: str, text_bounds: List[TextBound]) -> List[MatchResult]:
        """
        Find matches for an entity in the extracted text bounds.
        
        Args:
            entity: The entity text to match
            text_bounds: List of text bounds from PDF
            
        Returns:
            List of MatchResult objects
        """
        pass


class ExactMatchingStrategy(MatchingStrategy):
    """Exact string matching strategy."""
    
    def match(self, entity: str, text_bounds: List[TextBound]) -> List[MatchResult]:
        """
        Find exact matches for the entity.
        
        Args:
            entity: The entity text to match
            text_bounds: List of text bounds from PDF
            
        Returns:
            List of MatchResult objects with 100% confidence for exact matches
        """
        results = []
        entity_lower = entity.lower()
        
        for text_bound in text_bounds:
            if text_bound.text.lower() == entity_lower:
                results.append(MatchResult(text_bound, 100.0))
        
        return results


class FuzzyMatchingStrategy(MatchingStrategy):
    """Fuzzy string matching strategy using Levenshtein distance."""
    
    def __init__(self, threshold: float = 80.0):
        """
        Initialize fuzzy matching strategy.
        
        Args:
            threshold: Minimum confidence score to consider a match (0-100)
        """
        self.threshold = threshold
    
    def match(self, entity: str, text_bounds: List[TextBound]) -> List[MatchResult]:
        """
        Find fuzzy matches for the entity.
        
        Args:
            entity: The entity text to match
            text_bounds: List of text bounds from PDF
            
        Returns:
            List of MatchResult objects with confidence scores
        """
        results = []
        
        for text_bound in text_bounds:
            # Calculate similarity ratio
            confidence = fuzz.ratio(entity.lower(), text_bound.text.lower())
            
            if confidence >= self.threshold:
                results.append(MatchResult(text_bound, confidence))
        
        return results


class ContextualMatchingStrategy(MatchingStrategy):
    """Contextual matching strategy considering surrounding text."""
    
    def __init__(self, context_window: int = 3, threshold: float = 70.0):
        """
        Initialize contextual matching strategy.
        
        Args:
            context_window: Number of words before/after to consider as context
            threshold: Minimum confidence score to consider a match (0-100)
        """
        self.context_window = context_window
        self.threshold = threshold
    
    def match(self, entity: str, text_bounds: List[TextBound]) -> List[MatchResult]:
        """
        Find matches considering context.
        
        Args:
            entity: The entity text to match
            text_bounds: List of text bounds from PDF
            
        Returns:
            List of MatchResult objects with context information
        """
        results = []
        entity_words = entity.lower().split()
        
        # Group text bounds by page for context
        page_groups = {}
        for idx, text_bound in enumerate(text_bounds):
            page = text_bound.page
            if page not in page_groups:
                page_groups[page] = []
            page_groups[page].append((idx, text_bound))
        
        # Search for multi-word entities
        for page, bounds_list in page_groups.items():
            for i in range(len(bounds_list) - len(entity_words) + 1):
                # Get consecutive words
                window_words = [bounds_list[i + j][1].text.lower() for j in range(len(entity_words))]
                window_text = " ".join(window_words)
                
                # Calculate similarity
                confidence = fuzz.ratio(entity.lower(), window_text)
                
                if confidence >= self.threshold:
                    # Get context
                    context_start = max(0, i - self.context_window)
                    context_end = min(len(bounds_list), i + len(entity_words) + self.context_window)
                    context_words = [bounds_list[j][1].text for j in range(context_start, context_end)]
                    context = " ".join(context_words)
                    
                    # Create merged bound for multi-word entity
                    first_bound = bounds_list[i][1]
                    last_bound = bounds_list[i + len(entity_words) - 1][1]
                    
                    merged_bound = TextBound(
                        text=window_text,
                        x0=first_bound.x0,
                        y0=first_bound.y0,
                        x1=last_bound.x1,
                        y1=last_bound.y1,
                        page=page
                    )
                    
                    results.append(MatchResult(merged_bound, confidence, context))
        
        return results
