import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.api.endpoints import app
from app.models.domain import Restaurant, UserPreferences, RecommendationResponse

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    json_data = response.json()
    assert "status" in json_data
    assert "database_loaded" in json_data
    assert "llm_client_ready" in json_data

def test_metadata_endpoints():
    response = client.get("/api/v1/metadata/locations")
    assert response.status_code == 200
    locations = response.json()
    assert isinstance(locations, list)
    
    response = client.get("/api/v1/metadata/cuisines")
    assert response.status_code == 200
    cuisines = response.json()
    assert isinstance(cuisines, list)

@patch('app.api.endpoints.recommend_use_case.llm_client')
def test_recommendations_endpoint_success(mock_llm_client):
    mock_llm_client.complete.return_value = '{"summary": "Test summary", "recommendations": [{"restaurant_id": "1", "rank": 1, "explanation": "Perfect match"}]}'
    
    r1 = Restaurant(id="1", name="Pizza Place", location="Bangalore", cuisines=["Italian"], rating=4.5, estimated_cost=1000, budget_band="medium")
    
    with patch('app.api.endpoints.repository.get_all', return_value=[r1]):
        payload = {
            "location": "Bangalore",
            "budget": "medium",
            "cuisine": "Italian",
            "min_rating": 4.0,
            "additional_preferences": "nice cozy place",
            "top_k": 2
        }
        
        response = client.post("/api/v1/recommendations", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["summary"] == "Test summary"
        assert len(data["recommendations"]) == 1
        assert data["recommendations"][0]["restaurant"]["name"] == "Pizza Place"
        assert data["recommendations"][0]["explanation"] == "Perfect match"

def test_recommendations_endpoint_validation_error():
    payload = {
        "location": "Bangalore"
    }
    response = client.post("/api/v1/recommendations", json=payload)
    assert response.status_code == 422
