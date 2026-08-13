import json
import re
from typing import Dict, Any

class ResponseParser:
    @staticmethod
    def parse(raw_response: str) -> Dict[str, Any]:
        """
        Parses the raw JSON string from the LLM into a dictionary.
        Attempts to extract JSON if it was accidentally wrapped in markdown.
        """
        raw_response = raw_response.strip()
        
        # Fallback regex extraction if model wraps in markdown despite instructions
        if raw_response.startswith("```"):
            match = re.search(r"```(?:json)?\s*(.*?)\s*```", raw_response, re.DOTALL)
            if match:
                raw_response = match.group(1).strip()
                
        try:
            parsed = json.loads(raw_response)
            return parsed
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM response: {raw_response}")
            # Fallback to an empty schema
            return {
                "summary": "We couldn't generate a personalized summary at this time.",
                "recommendations": []
            }
