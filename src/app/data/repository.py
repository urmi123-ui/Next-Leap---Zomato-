import os
import pandas as pd
from typing import List, Optional
from app.models.domain import Restaurant, UserPreferences
from app.config import settings

class RestaurantRepository:
    def __init__(self, data_path: Optional[str] = None):
        if data_path is None:
            # Default to settings.data_path resolved relative to the repository root
            proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
            data_path = os.path.abspath(os.path.join(proj_root, settings.data_path))
        self.data_path = data_path
        self._df: Optional[pd.DataFrame] = None
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.data_path):
            self._df = pd.read_parquet(self.data_path)
        else:
            print(f"Warning: Data file not found at {self.data_path}")
            self._df = pd.DataFrame()

    def get_all(self) -> List[Restaurant]:
        """
        Returns all restaurants in the dataset as Restaurant models.
        """
        if self._df is None or self._df.empty:
            return []
        
        # Convert DataFrame to list of Restaurant objects
        restaurants = []
        for _, row in self._df.iterrows():
            restaurants.append(self._row_to_restaurant(row))
        return restaurants

    def get_unique_locations(self) -> List[str]:
        """Returns sorted list of unique locations."""
        if self._df is None or self._df.empty or "location" not in self._df.columns:
            return []
        # Ensure we decode bytes if any
        locations = self._df["location"].dropna().unique()
        cleaned = []
        for loc in locations:
            if isinstance(loc, bytes):
                cleaned.append(loc.decode("utf-8"))
            else:
                cleaned.append(str(loc))
        return sorted(list(set(cleaned)))

    def get_unique_cuisines(self) -> List[str]:
        """Returns sorted list of unique individual cuisines."""
        if self._df is None or self._df.empty or "cuisines" not in self._df.columns:
            return []
        
        # We need to extract all individual cuisines
        all_cuisines = set()
        for val in self._df["cuisines"].dropna():
            # If it's a list or numpy array
            if isinstance(val, (list, bytes, str)):
                if isinstance(val, bytes):
                    val = val.decode("utf-8")
                if isinstance(val, str):
                    val = val.strip("[]'\" ")
                    items = [i.strip().strip("'\"") for i in val.split(",")]
                else:
                    items = val
                for item in items:
                    if item:
                        all_cuisines.add(item)
        return sorted(list(all_cuisines))

    def _row_to_restaurant(self, row: pd.Series) -> Restaurant:
        """Helper to convert a pandas row to a Restaurant Pydantic model."""
        def clean_str(val) -> str:
            if isinstance(val, bytes):
                return val.decode("utf-8")
            return str(val)

        cuisines = row.get("cuisines", [])
        if isinstance(cuisines, bytes):
            cuisines = cuisines.decode("utf-8")
            
        if isinstance(cuisines, str):
            # Parse string representation of list like '["North Indian", "Mughlai"]' or 'Italian, Chinese'
            cuisines = cuisines.strip("[]'\" ")
            if "," in cuisines:
                cuisines = [c.strip().strip("'\"") for c in cuisines.split(",")]
            else:
                cuisines = [cuisines] if cuisines else []
        elif not isinstance(cuisines, list):
            try:
                cuisines = list(cuisines)
            except TypeError:
                cuisines = []

        cuisines = [clean_str(c) for c in cuisines]

        return Restaurant(
            id=clean_str(row.get("id", "")),
            name=clean_str(row.get("name", "Unknown")),
            location=clean_str(row.get("location", "Unknown")),
            cuisines=cuisines,
            rating=float(row.get("rating", 0.0)),
            estimated_cost=float(row.get("estimated_cost", 0.0)),
            budget_band=clean_str(row.get("budget_band", "medium"))
        )
