"""
Tests for FastAPI endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


class TestAPIEndpoints:
    """Test API endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns health check."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        assert "version" in data
    
    def test_get_strategies(self):
        """Test getting available strategies."""
        response = client.get("/api/strategies")
        assert response.status_code == 200
        data = response.json()
        assert "strategies" in data
        
        strategies = data["strategies"]
        strategy_names = [s["name"] for s in strategies]
        
        assert "exact" in strategy_names
        assert "fuzzy" in strategy_names
        assert "contextual" in strategy_names
    
    def test_extract_entities_without_api_key(self):
        """Test entity extraction fails without API key."""
        response = client.post(
            "/api/extract-entities",
            json={"text": "Test text"}
        )
        # Should fail if no API key is configured
        assert response.status_code in [400, 500]
