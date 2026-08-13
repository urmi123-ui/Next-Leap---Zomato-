# AI-Powered Restaurant Recommendation System Implementation Plan

This document outlines the phase-wise implementation plan for the Zomato-inspired restaurant recommendation service, based on the requirements in `context.md` and the system design in `architecture.md`.

## Proposed Changes

### Phase 1: Project Setup & Data Ingestion
This phase focuses on bootstrapping the repository and building the offline data ingestion pipeline.

#### `requirements.txt` / `pyproject.toml`
Define core dependencies (e.g., `pandas`, `datasets`, `pydantic`, LLM SDKs like `groq`, `streamlit`).

#### `src/app/models/`
- Define data models (`Restaurant`, `UserPreferences`, `Recommendation`, `RecommendationResponse`) using `pydantic`.

#### `src/app/ingestion/`
- `loader.py`: Script to download the Hugging Face dataset.
- `normalizer.py`: Map dataset columns to our canonical `Restaurant` model.
- `pipeline.py`: Clean data (handle nulls, string normalization) and map estimated costs to `budget_band`.
- **Script**: Create `scripts/ingest.py` to run the pipeline and save the processed dataset locally (e.g., as a Parquet or SQLite file in `data/processed/`).

---

### Phase 2: Data Access & Filtering Engine
This phase implements the local data store access and deterministic filtering logic.

#### `src/app/data/repository.py`
- Implement `RestaurantRepository` to load the processed dataset into memory or query SQLite.
- Implement methods: `get_all()`, `filter()`.

#### `src/app/services/filter_service.py`
- Implement `FilterService` to apply deterministic rules (location, budget, cuisine, rating).
- Cap candidates (e.g., top 30 based on ratings/votes) to limit LLM tokens.

#### Tests
- Add unit tests for `SchemaNormalizer` and `FilterService` to ensure correct matching logic.

---

### Phase 3: LLM Integration & Orchestration
This phase handles the generative AI components for ranking and explaining recommendations.

#### `src/app/services/prompt_builder.py`
- Construct the system prompt enforcing grounding rules.
- Format the filtered candidate restaurants and user preferences into the context window.

#### `src/app/services/llm_client.py` & `response_parser.py`
- Implement a wrapper for the LLM API (e.g., Groq).
- Enforce JSON structured output for the recommendations and explanations.
- Implement `ResponseParser` to safely parse and validate the LLM's JSON response, mapping it to our internal models.

#### `src/app/services/orchestrator.py`
- Implement `RecommendRestaurantsUseCase` to coordinate: `filter` -> `prompt` -> `LLM` -> `parse` -> `merge`.

---

### Phase 4: Backend REST API Layer
This phase builds the REST API boundary using FastAPI, separating backend logic from the UI.

#### `requirements.txt`
- Add FastAPI and Uvicorn dependencies (`fastapi`, `uvicorn`, `requests`).

#### `src/app/api/endpoints.py`
- Set up FastAPI app instance.
- Implement `GET /api/v1/health` to check database loading status and LLM API setup.
- Implement `POST /api/v1/recommendations` to parse `UserPreferences` from request body and invoke `RecommendRestaurantsUseCase`.
- Implement `GET /api/v1/metadata/locations` and `GET /api/v1/metadata/cuisines` to return unique values for client-side selection.

#### `src/app/main_api.py` [NEW]
- Entrypoint to start the Uvicorn ASGI server hosting the FastAPI application.

---

### Phase 5: Frontend Presentation Layer (Streamlit HTTP Client)
This phase adapts the user interface to communicate over REST API boundaries.

#### `src/app/main.py`
- Modify the Streamlit application to act as a pure client.
- Replace direct imports of `RecommendRestaurantsUseCase` and repository with HTTP calls (using `requests`) to the backend FastAPI endpoints (e.g., fetching location/cuisine lists dynamically, calling the recommendations endpoint).
- Retrieve and render the API response.
- **CSS overrides [NEW]**: Implement explicit styling on dropdown popover items (`div[data-baseweb="popover"] li`) to resolve the dark-mode white-on-white text visibility bug. Override active/disabled submit button styles, targeting nested `<p>` and `<span>` tags to ensure button labels render correctly in white instead of inheriting default body-text grey.


---

## Verification Plan

### Automated Tests
- `pytest` for `FilterService` rules (e.g., ensuring budget bands filter correctly).
- Mock the `LLMClient` to test the `Orchestrator` flow without incurring API costs.
- Validate `ResponseParser` against mocked malformed LLM responses.
- **API Tests [NEW]**: Create `tests/test_api.py` using FastAPI's `TestClient` to verify `/api/v1/health` and mock recommendations responses.

### Manual Verification
- Run the ingestion script and inspect outputs.
- Start the FastAPI backend server (`uvicorn app.main_api:app --reload`).
- Start the Streamlit frontend client (`streamlit run src/app/main.py`).
- Verify correct integration and error responses when the backend is unreachable or returns validation errors.

