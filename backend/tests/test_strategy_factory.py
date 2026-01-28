"""
Tests for strategy factory
"""
import pytest
from app.strategy_factory import MatchingStrategyFactory
from app.matching_strategies import (
    ExactMatchingStrategy,
    FuzzyMatchingStrategy,
    ContextualMatchingStrategy
)


class TestMatchingStrategyFactory:
    """Test matching strategy factory."""
    
    def test_create_exact_strategy(self):
        """Test creating exact matching strategy."""
        strategy = MatchingStrategyFactory.create_strategy('exact')
        assert isinstance(strategy, ExactMatchingStrategy)
    
    def test_create_fuzzy_strategy(self):
        """Test creating fuzzy matching strategy."""
        strategy = MatchingStrategyFactory.create_strategy('fuzzy', threshold=85.0)
        assert isinstance(strategy, FuzzyMatchingStrategy)
        assert strategy.threshold == 85.0
    
    def test_create_fuzzy_strategy_default(self):
        """Test creating fuzzy strategy with default threshold."""
        strategy = MatchingStrategyFactory.create_strategy('fuzzy')
        assert isinstance(strategy, FuzzyMatchingStrategy)
        assert strategy.threshold == 80.0
    
    def test_create_contextual_strategy(self):
        """Test creating contextual matching strategy."""
        strategy = MatchingStrategyFactory.create_strategy(
            'contextual',
            threshold=75.0,
            context_window=5
        )
        assert isinstance(strategy, ContextualMatchingStrategy)
        assert strategy.threshold == 75.0
        assert strategy.context_window == 5
    
    def test_create_unknown_strategy(self):
        """Test that unknown strategy raises ValueError."""
        with pytest.raises(ValueError, match="Unknown strategy type"):
            MatchingStrategyFactory.create_strategy('unknown')
    
    def test_get_all_strategies(self):
        """Test getting all available strategies."""
        strategies = MatchingStrategyFactory.get_all_strategies()
        
        assert 'exact' in strategies
        assert 'fuzzy' in strategies
        assert 'contextual' in strategies
        
        assert isinstance(strategies['exact'], ExactMatchingStrategy)
        assert isinstance(strategies['fuzzy'], FuzzyMatchingStrategy)
        assert isinstance(strategies['contextual'], ContextualMatchingStrategy)
    
    def test_case_insensitive_strategy_type(self):
        """Test that strategy type is case-insensitive."""
        strategy1 = MatchingStrategyFactory.create_strategy('EXACT')
        strategy2 = MatchingStrategyFactory.create_strategy('Exact')
        strategy3 = MatchingStrategyFactory.create_strategy('exact')
        
        assert isinstance(strategy1, ExactMatchingStrategy)
        assert isinstance(strategy2, ExactMatchingStrategy)
        assert isinstance(strategy3, ExactMatchingStrategy)
