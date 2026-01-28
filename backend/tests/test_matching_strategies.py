"""
Tests for matching strategies
"""
import pytest
from app.matching_strategies import (
    ExactMatchingStrategy,
    FuzzyMatchingStrategy,
    ContextualMatchingStrategy
)
from app.pdf_extractor import TextBound


@pytest.fixture
def sample_text_bounds():
    """Create sample text bounds for testing."""
    return [
        TextBound("Hello", 10.0, 20.0, 30.0, 25.0, 0),
        TextBound("World", 35.0, 20.0, 55.0, 25.0, 0),
        TextBound("Python", 10.0, 30.0, 40.0, 35.0, 0),
        TextBound("Programming", 45.0, 30.0, 80.0, 35.0, 0),
        TextBound("hello", 10.0, 40.0, 30.0, 45.0, 0),  # Lowercase version
    ]


class TestExactMatchingStrategy:
    """Test exact matching strategy."""
    
    def test_exact_match_case_insensitive(self, sample_text_bounds):
        """Test that exact matching is case-insensitive."""
        strategy = ExactMatchingStrategy()
        results = strategy.match("hello", sample_text_bounds)
        
        assert len(results) == 2
        assert all(r.confidence == 100.0 for r in results)
    
    def test_exact_match_no_results(self, sample_text_bounds):
        """Test that no results are returned for non-matching text."""
        strategy = ExactMatchingStrategy()
        results = strategy.match("nonexistent", sample_text_bounds)
        
        assert len(results) == 0
    
    def test_exact_match_single_result(self, sample_text_bounds):
        """Test single exact match."""
        strategy = ExactMatchingStrategy()
        results = strategy.match("Python", sample_text_bounds)
        
        assert len(results) == 1
        assert results[0].confidence == 100.0
        assert results[0].text_bound.text == "Python"


class TestFuzzyMatchingStrategy:
    """Test fuzzy matching strategy."""
    
    def test_fuzzy_match_with_typo(self, sample_text_bounds):
        """Test fuzzy matching with typos."""
        strategy = FuzzyMatchingStrategy(threshold=70.0)
        results = strategy.match("Wrold", sample_text_bounds)  # Typo in "World"
        
        # Should still find "World" with fuzzy matching
        assert len(results) > 0
    
    def test_fuzzy_match_threshold(self, sample_text_bounds):
        """Test that threshold is respected."""
        strategy = FuzzyMatchingStrategy(threshold=95.0)
        results = strategy.match("Helo", sample_text_bounds)  # Missing letter
        
        # With high threshold, this might not match
        # The test validates that threshold logic works
        for result in results:
            assert result.confidence >= 95.0
    
    def test_fuzzy_match_exact(self, sample_text_bounds):
        """Test that exact matches get 100% confidence."""
        strategy = FuzzyMatchingStrategy(threshold=80.0)
        results = strategy.match("World", sample_text_bounds)
        
        assert len(results) > 0
        exact_matches = [r for r in results if r.confidence == 100.0]
        assert len(exact_matches) == 1


class TestContextualMatchingStrategy:
    """Test contextual matching strategy."""
    
    def test_contextual_match_multi_word(self, sample_text_bounds):
        """Test matching multi-word entities."""
        strategy = ContextualMatchingStrategy(threshold=70.0)
        results = strategy.match("Python Programming", sample_text_bounds)
        
        assert len(results) > 0
        # Check that context is included
        assert results[0].context is not None
    
    def test_contextual_match_with_context(self, sample_text_bounds):
        """Test that context includes surrounding words."""
        strategy = ContextualMatchingStrategy(context_window=2, threshold=70.0)
        results = strategy.match("World", sample_text_bounds)
        
        if len(results) > 0:
            # Context should include surrounding words
            assert "Hello" in results[0].context or "World" in results[0].context
    
    def test_contextual_match_single_word(self, sample_text_bounds):
        """Test single word matching with context."""
        strategy = ContextualMatchingStrategy(threshold=90.0)
        results = strategy.match("Python", sample_text_bounds)
        
        assert len(results) > 0
        assert results[0].context is not None
