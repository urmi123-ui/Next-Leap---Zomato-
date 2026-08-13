from typing import List, Dict, Any
from app.models.domain import UserPreferences, Restaurant, Recommendation, RecommendationResponse
from app.data.repository import RestaurantRepository
from app.services.filter_service import FilterService
from app.services.prompt_builder import PromptBuilder
from app.services.llm_client import GroqClient
from app.services.response_parser import ResponseParser

class RecommendRestaurantsUseCase:
    def __init__(self, repository: RestaurantRepository):
        self.repository = repository
        # Only initialize the LLM client if we are actually executing, 
        # allowing for graceful handling if API keys aren't set yet during tests.
        try:
            self.llm_client = GroqClient()
        except Exception as e:
            print(f"Warning: Failed to initialize GroqClient: {e}")
            self.llm_client = None

    def execute(self, preferences: UserPreferences) -> RecommendationResponse:
        # 1. Load data and Filter
        all_restaurants = self.repository.get_all()
        candidates, meta = FilterService.filter(preferences, all_restaurants)
        
        # 2. Check if we have candidates
        if not candidates:
            return RecommendationResponse(
                summary="No restaurants match your strict criteria. Try lowering the minimum rating or changing the budget.",
                recommendations=[]
            )
            
        # 3. If no LLM available, fallback to rating sort
        if self.llm_client is None:
            return self._build_fallback_response(candidates, preferences.top_k)
            
        # 4. Prompt Building
        sys_prompt = PromptBuilder.build_system_prompt()
        user_prompt = PromptBuilder.build_user_prompt(preferences, candidates)
        
        # 5. Call LLM
        try:
            raw_response = self.llm_client.complete(sys_prompt, user_prompt)
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return self._build_fallback_response(candidates, preferences.top_k)
            
        # 6. Parse Response
        parsed = ResponseParser.parse(raw_response)
        
        # 7. Merge and Rank
        return self._merge_results(parsed, candidates, preferences.top_k)

    def _merge_results(self, parsed: Dict[str, Any], candidates: List[Restaurant], top_k: int) -> RecommendationResponse:
        # Create a map for O(1) lookup
        candidate_map = {c.id: c for c in candidates}
        
        recommendations = []
        parsed_recs = parsed.get("recommendations", [])
        
        for item in parsed_recs:
            r_id = str(item.get("restaurant_id", ""))
            if r_id in candidate_map:
                rank = item.get("rank", len(recommendations) + 1)
                explanation = item.get("explanation", "Matches your preferences.")
                
                recommendations.append(
                    Recommendation(
                        restaurant=candidate_map[r_id],
                        rank=rank,
                        explanation=explanation
                    )
                )
                
                if len(recommendations) >= top_k:
                    break
                    
        # If LLM failed to return enough valid IDs, fallback fill the rest
        if len(recommendations) == 0:
            return self._build_fallback_response(candidates, top_k)
            
        summary = parsed.get("summary", "Here are your personalized recommendations.")
        return RecommendationResponse(summary=summary, recommendations=recommendations)

    def _build_fallback_response(self, candidates: List[Restaurant], top_k: int) -> RecommendationResponse:
        """Fallback method when LLM is unavailable or fails."""
        recommendations = []
        for i, c in enumerate(candidates[:top_k]):
            recommendations.append(
                Recommendation(
                    restaurant=c,
                    rank=i + 1,
                    explanation="Recommended based on high overall ratings and your criteria."
                )
            )
        return RecommendationResponse(
            summary="Here are the top-rated restaurants matching your criteria.",
            recommendations=recommendations
        )
