import pandas as pd
from typing import Literal

def assign_budget_band(cost: float) -> Literal["low", "medium", "high"]:
    """
    Map estimated cost to a budget band.
    Adjust thresholds based on dataset exploration.
    """
    if pd.isna(cost) or cost <= 500:
        return "low"
    elif cost <= 1500:
        return "medium"
    else:
        return "high"

class DataPipeline:
    @staticmethod
    def clean_and_prepare(df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans data (handles nulls, normalizes strings) and adds budget_band.
        """
        # Handle rating: parse string "4.1/5" to float, replace "NEW" or "-" with NaN
        if "rating" in df.columns:
            df["rating"] = df["rating"].astype(str).str.split("/").str[0].str.strip()
            df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0.0)
            
        # Handle estimated_cost: remove commas from string like "1,200"
        if "estimated_cost" in df.columns:
            if df["estimated_cost"].dtype == 'object':
                df["estimated_cost"] = df["estimated_cost"].astype(str).str.replace(",", "")
            df["estimated_cost"] = pd.to_numeric(df["estimated_cost"], errors="coerce")
            df["estimated_cost"] = df["estimated_cost"].fillna(df["estimated_cost"].median())
            
        if "cuisines" in df.columns:
            df["cuisines"] = df["cuisines"].fillna("Unknown")
            
        if "location" in df.columns:
            df["location"] = df["location"].fillna("Unknown")
            
        # String normalization
        if "location" in df.columns:
            df["location"] = df["location"].astype(str).str.strip().str.title()
            
        if "cuisines" in df.columns:
            # cuisines is usually a comma-separated string, convert to list of normalized strings
            df["cuisines"] = df["cuisines"].astype(str).apply(
                lambda x: [c.strip().title() for c in x.split(",")]
            )
            
        # Add budget_band
        if "estimated_cost" in df.columns:
            df["budget_band"] = df["estimated_cost"].apply(assign_budget_band)
            
        # Deduplicate restaurants on name and location to avoid listing duplicate outlets in recommendations
        if "name" in df.columns and "location" in df.columns:
            df = df.drop_duplicates(subset=["name", "location"])
            
        return df
