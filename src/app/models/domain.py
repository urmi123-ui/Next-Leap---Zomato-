from typing import List, Literal, Optional
from pydantic import BaseModel, Field

BudgetBand = Literal["low", "medium", "high"]

class Restaurant(BaseModel):
    id: str
    name: str
    location: str
    cuisines: List[str]
    rating: float
    estimated_cost: float
    budget_band: BudgetBand
    metadata: Optional[dict] = Field(default_factory=dict)

class UserPreferences(BaseModel):
    location: str
    budget: BudgetBand
    cuisine: str
    min_rating: float = Field(ge=0.0, le=5.0)
    additional_preferences: Optional[str] = None
    top_k: int = 5

class Recommendation(BaseModel):
    restaurant: Restaurant
    rank: int
    explanation: str

class RecommendationResponse(BaseModel):
    summary: Optional[str] = None
    recommendations: List[Recommendation]
