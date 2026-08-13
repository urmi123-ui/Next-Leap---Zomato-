import json
from typing import List
from app.models.domain import Restaurant, UserPreferences

class PromptBuilder:
    @staticmethod
    def build_system_prompt() -> str:
        return (
            "You are an expert, friendly AI restaurant advisor inspired by Zomato.\n"
            "Your task is to recommend restaurants based strictly on the provided candidate list.\n"
            "Rules:\n"
            "1. ONLY recommend restaurants from the provided JSON list.\n"
            "2. Rank the top restaurants based on how well they match the user's preferences.\n"
            "3. Do NOT invent or hallucinate any restaurants not in the list.\n"
            "4. Provide a short, personalized explanation for why each restaurant fits.\n"
            "5. You MUST output ONLY valid JSON in the requested format, with no markdown code blocks wrapping it."
        )

    @staticmethod
    def build_user_prompt(preferences: UserPreferences, candidates: List[Restaurant]) -> str:
        candidates_json = json.dumps([c.model_dump() for c in candidates], indent=2)
        
        pref_desc = f"Location: {preferences.location}\nBudget: {preferences.budget}\nCuisine: {preferences.cuisine}\nMinimum Rating: {preferences.min_rating}\n"
        if preferences.additional_preferences:
            pref_desc += f"Additional Preferences: {preferences.additional_preferences}\n"
            
        return (
            f"User Preferences:\n{pref_desc}\n\n"
            f"Candidate Restaurants:\n{candidates_json}\n\n"
            "Please analyze the Candidate Restaurants and select up to the top "
            f"{preferences.top_k} matches for the User Preferences. "
            "Output your response strictly in the following JSON format:\n"
            "{\n"
            '  "summary": "Brief 1-sentence overview of your recommendations",\n'
            '  "recommendations": [\n'
            "    {\n"
            '      "restaurant_id": "id_from_candidate",\n'
            '      "rank": 1,\n'
            '      "explanation": "Why this is a great fit."\n'
            "    }\n"
            "  ]\n"
            "}"
        )
