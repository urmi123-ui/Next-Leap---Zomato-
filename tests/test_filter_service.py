import pytest
from app.models.domain import Restaurant, UserPreferences
from app.services.filter_service import FilterService

def test_filter_exact_match():
    r1 = Restaurant(id="1", name="Pizza Place", location="Bangalore", cuisines=["Italian", "Pizza"], rating=4.5, estimated_cost=1000, budget_band="medium")
    r2 = Restaurant(id="2", name="Burger Joint", location="Delhi", cuisines=["American"], rating=4.0, estimated_cost=400, budget_band="low")
    
    prefs = UserPreferences(
        location="Bangalore",
        budget="medium",
        cuisine="Italian",
        min_rating=4.0,
        top_k=5
    )
    
    candidates, meta = FilterService.filter(prefs, [r1, r2])
    
    assert len(candidates) == 1
    assert candidates[0].id == "1"
    assert meta["total_matches_before_cap"] == 1

def test_filter_case_insensitivity_and_substring():
    r1 = Restaurant(id="1", name="Fancy Diner", location="New Delhi", cuisines=["NORTH INDIAN", "Chinese"], rating=4.2, estimated_cost=2000, budget_band="high")
    
    prefs = UserPreferences(
        location="delhi",
        budget="high",
        cuisine="indian",
        min_rating=4.0,
        top_k=5
    )
    
    candidates, meta = FilterService.filter(prefs, [r1])
    
    assert len(candidates) == 1
    assert candidates[0].id == "1"

def test_filter_rating_threshold():
    r1 = Restaurant(id="1", name="Okay Place", location="Mumbai", cuisines=["Cafe"], rating=3.5, estimated_cost=800, budget_band="medium")
    
    prefs = UserPreferences(
        location="Mumbai",
        budget="medium",
        cuisine="Cafe",
        min_rating=4.0, # higher than r1 rating
        top_k=5
    )
    
    candidates, _ = FilterService.filter(prefs, [r1])
    assert len(candidates) == 0

def test_filter_budget_band():
    r1 = Restaurant(id="1", name="Cheap Eats", location="Pune", cuisines=["Street Food"], rating=4.5, estimated_cost=200, budget_band="low")
    
    prefs = UserPreferences(
        location="Pune",
        budget="high", # looking for high budget
        cuisine="Street Food",
        min_rating=3.0,
        top_k=5
    )
    
    candidates, _ = FilterService.filter(prefs, [r1])
    assert len(candidates) == 0
