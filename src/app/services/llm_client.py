from groq import Groq
from app.config import settings

class GroqClient:
    def __init__(self):
        self.api_key = settings.llm_api_key
        self.model = settings.llm_model
        
        if not self.api_key or self.api_key == "your_groq_api_key_here":
            raise ValueError("LLM_API_KEY is not configured properly in environment variables.")
            
        self.client = Groq(api_key=self.api_key)

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        """
        Calls the Groq API and returns the generated text.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3, # low temp for more deterministic JSON and grounding
            max_tokens=1024,
            response_format={"type": "json_object"}
        )
        
        return response.choices[0].message.content
