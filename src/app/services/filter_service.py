from typing import List, Dict, Any, Tuple
from app.models.domain import Restaurant, UserPreferences
from app.config import settings

class FilterService:
    MAX_CANDIDATES = settings.max_candidates

    @staticmethod
    def filter(preferences: UserPreferences, restaurants: List[Restaurant]) -> Tuple[List[Restaurant], Dict[str, Any]]:
        """
        Applies deterministic filters based on user preferences.
        Returns a tuple of (filtered_candidates, metadata_dict)
        """
        filtered = []
        
        # Pre-process location and cuisine for case-insensitive matching
        pref_location = preferences.location.strip().lower()
        pref_cuisine = preferences.cuisine.strip().lower()
        
        for r in restaurants:
            # Filter by location (exact or substring)
            if pref_location not in r.location.lower():
                continue
                
            # Filter by budget band
            if r.budget_band != preferences.budget:
                continue
                
            # Filter by min rating
            if r.rating < preferences.min_rating:
                continue
                
            # Filter by cuisine
            # User cuisine just needs to be one of the restaurant's cuisines
            has_cuisine = any(pref_cuisine in c.lower() for c in r.cuisines)
            if not has_cuisine:
                continue
                
            filtered.append(r)
            
        total_before_cap = len(filtered)
        
        # Sort by rating descending to ensure the LLM gets the highest quality matches first
        filtered.sort(key=lambda x: x.rating, reverse=True)
        
        # Cap candidates to avoid blowing up the LLM token context limit
        capped_candidates = filtered[:FilterService.MAX_CANDIDATES]
        
        metadata = {
            "total_matches_before_cap": total_before_cap,
            "candidates_sent_to_llm": len(capped_candidates),
            "filters_applied": {
                "location": preferences.location,
                "budget": preferences.budget,
                "cuisine": preferences.cuisine,
                "min_rating": preferences.min_rating
            }
        }
        
        return capped_candidates, metadata
