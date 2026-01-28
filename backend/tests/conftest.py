"""
Tests configuration
"""
import pytest
import sys
from pathlib import Path

# Add backend/app directory to Python path
backend_dir = Path(__file__).parent.parent
app_dir = backend_dir / "app"
sys.path.insert(0, str(app_dir))
