"""
Matching Strategy Factory

Implements Factory Pattern for creating matching strategies.
"""
from typing import Dict, Any

try:
    from .matching_strategies import (
        MatchingStrategy,
        ExactMatchingStrategy,
        FuzzyMatchingStrategy,
        ContextualMatchingStrategy
    )
except ImportError:
    from matching_strategies import (
        MatchingStrategy,
        ExactMatchingStrategy,
        FuzzyMatchingStrategy,
        ContextualMatchingStrategy
    )


class MatchingStrategyFactory:
    """Factory for creating matching strategy instances."""
    
    @staticmethod
    def create_strategy(strategy_type: str, **kwargs) -> MatchingStrategy:
        """
        Create a matching strategy based on type.
        
        Args:
            strategy_type: Type of strategy ('exact', 'fuzzy', 'contextual')
            **kwargs: Additional parameters for strategy initialization
            
        Returns:
            MatchingStrategy instance
            
        Raises:
            ValueError: If strategy_type is not recognized
        """
        strategies = {
            'exact': ExactMatchingStrategy,
            'fuzzy': FuzzyMatchingStrategy,
            'contextual': ContextualMatchingStrategy
        }
        
        strategy_class = strategies.get(strategy_type.lower())
        
        if strategy_class is None:
            raise ValueError(
                f"Unknown strategy type: {strategy_type}. "
                f"Available types: {', '.join(strategies.keys())}"
            )
        
        # Initialize strategy with appropriate parameters
        if strategy_type.lower() == 'exact':
            return strategy_class()
        elif strategy_type.lower() == 'fuzzy':
            threshold = kwargs.get('threshold', 80.0)
            return strategy_class(threshold=threshold)
        elif strategy_type.lower() == 'contextual':
            context_window = kwargs.get('context_window', 3)
            threshold = kwargs.get('threshold', 70.0)
            return strategy_class(context_window=context_window, threshold=threshold)
    
    @staticmethod
    def get_all_strategies(**kwargs) -> Dict[str, MatchingStrategy]:
        """
        Get all available strategies.
        
        Args:
            **kwargs: Parameters for strategy initialization
            
        Returns:
            Dictionary mapping strategy names to instances
        """
        return {
            'exact': MatchingStrategyFactory.create_strategy('exact'),
            'fuzzy': MatchingStrategyFactory.create_strategy('fuzzy', **kwargs),
            'contextual': MatchingStrategyFactory.create_strategy('contextual', **kwargs)
        }
