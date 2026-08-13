from datasets import load_dataset
import pandas as pd

class DatasetLoader:
    def __init__(self, dataset_url: str = "ManikaSaini/zomato-restaurant-recommendation"):
        self.dataset_url = dataset_url

    def load_raw_dataset(self) -> pd.DataFrame:
        """
        Loads the raw Zomato dataset from Hugging Face and returns it as a pandas DataFrame.
        """
        print(f"Loading dataset from {self.dataset_url}...")
        dataset = load_dataset(self.dataset_url, split="train")
        df = dataset.to_pandas()
        print(f"Loaded {len(df)} records.")
        return df

if __name__ == "__main__":
    loader = DatasetLoader()
    df = loader.load_raw_dataset()
    print(df.head())
    print(df.columns)
