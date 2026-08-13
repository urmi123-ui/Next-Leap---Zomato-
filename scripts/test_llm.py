import sys
import os

# Add src to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app.models.domain import UserPreferences
from app.data.repository import RestaurantRepository
from app.services.orchestrator import RecommendRestaurantsUseCase

def main():
    print("Initializing components...")
    repo = RestaurantRepository()
    orchestrator = RecommendRestaurantsUseCase(repo)
    
    # Check if Groq client initialized
    if orchestrator.llm_client is None:
        print("Error: Groq client failed to initialize. Check your API key.")
        return
        
    print("Running recommendation query...")
    prefs = UserPreferences(
        location="Banashankari",
        budget="medium",
        cuisine="Mughlai",
        min_rating=4.0,
        additional_preferences="rooftop seating, romantic vibe",
        top_k=3
    )
    
    response = orchestrator.execute(prefs)
    
    print("\n--- LLM Summary ---")
    print(response.summary)
    
    print("\n--- Recommendations ---")
    for rec in response.recommendations:
        print(f"Rank {rec.rank}: {rec.restaurant.name} (Rating: {rec.restaurant.rating}, Cost: {rec.restaurant.estimated_cost})")
        print(f"Explanation: {rec.explanation}")
        print("-" * 40)

if __name__ == "__main__":
    main()
