import pytest
import pandas as pd
from app.ingestion.normalizer import SchemaNormalizer

def test_schema_normalizer():
    # Mock data based on what the real HF dataset provides
    raw_data = {
        "name": ["Test Rest"],
        "location": ["Test Locality"],
        "cuisines": ["Italian, Chinese"],
        "rate": ["4.5/5"],
        "approx_cost(for two people)": ["1,200"]
    }
    
    df = pd.DataFrame(raw_data)
    
    normalized_df = SchemaNormalizer.normalize(df)
    
    assert "name" in normalized_df.columns
    assert "location" in normalized_df.columns
    assert "cuisines" in normalized_df.columns
    assert "rating" in normalized_df.columns
    assert "estimated_cost" in normalized_df.columns
    assert "id" in normalized_df.columns
