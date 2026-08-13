import pandas as pd
from typing import List

class SchemaNormalizer:
    @staticmethod
    def normalize(df: pd.DataFrame) -> pd.DataFrame:
        """
        Maps raw dataset columns to the canonical Restaurant model structure.
        """
        # Rename columns to standardized names based on dataset inspection
        column_mapping = {
            "name": "name",
            "location": "location",
            "cuisines": "cuisines",
            "rate": "rating",
            "approx_cost(for two people)": "estimated_cost"
        }
        
        # Only rename columns that exist in the dataframe
        rename_dict = {k: v for k, v in column_mapping.items() if k in df.columns}
        df = df.rename(columns=rename_dict)
        
        # Add id column if not present
        if "Restaurant ID" in df.columns:
            df = df.rename(columns={"Restaurant ID": "id"})
            df["id"] = df["id"].astype(str)
        else:
            df["id"] = [str(i) for i in range(len(df))]
            
        # Ensure target columns exist (fill with defaults if they don't)
        if "location" not in df.columns and "City" in df.columns:
            df = df.rename(columns={"City": "location"})
            
        required_cols = ["id", "name", "location", "cuisines", "rating", "estimated_cost"]
        for col in required_cols:
            if col not in df.columns:
                print(f"Warning: Missing expected column {col}")
                
        return df
