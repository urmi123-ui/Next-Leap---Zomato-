from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
import os
from app.models.domain import UserPreferences, RecommendationResponse
from app.data.repository import RestaurantRepository
from app.services.orchestrator import RecommendRestaurantsUseCase
from app.config import settings

app = FastAPI(
    title="Zomato AI Recommendation System API",
    description="Backend API for filtering and ranking restaurant recommendations using Groq LLM.",
    version="1.0.0"
)

# Initialize data store and orchestrator
try:
    repository = RestaurantRepository()
    recommend_use_case = RecommendRestaurantsUseCase(repository)
except Exception as e:
    print(f"Initialization Error: {e}")
    repository = None
    recommend_use_case = None

@app.get("/api/v1/health")
def health_check():
    db_loaded = False
    if repository is not None and repository._df is not None:
        db_loaded = not repository._df.empty
        
    llm_ready = False
    if settings.llm_api_key and settings.llm_api_key != "your_groq_api_key_here":
        if recommend_use_case is not None and recommend_use_case.llm_client is not None:
            llm_ready = True
            
    is_healthy = db_loaded and llm_ready
    status_str = "healthy" if is_healthy else "unhealthy"
    
    return {
        "status": status_str,
        "database_loaded": db_loaded,
        "llm_client_ready": llm_ready
    }

@app.post("/api/v1/recommendations", response_model=RecommendationResponse)
def get_recommendations(preferences: UserPreferences):
    if recommend_use_case is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Recommendation backend is currently uninitialized or failed to start."
        )
    try:
        response = recommend_use_case.execute(preferences)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        )

@app.get("/api/v1/metadata/locations")
def get_locations():
    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Repository is uninitialized."
        )
    return repository.get_unique_locations()

@app.get("/api/v1/metadata/cuisines")
def get_cuisines():
    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Repository is uninitialized."
        )
    return repository.get_unique_cuisines()

# Serve static files for premium frontend
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
