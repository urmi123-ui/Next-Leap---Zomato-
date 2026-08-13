import sys
import os

# Add the src directory to the path so we can import from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app.ingestion.loader import DatasetLoader
from app.ingestion.normalizer import SchemaNormalizer
from app.ingestion.pipeline import DataPipeline

def main():
    print("Starting data ingestion process...")
    
    loader = DatasetLoader()
    raw_df = loader.load_raw_dataset()
    
    print("Normalizing schema...")
    normalized_df = SchemaNormalizer.normalize(raw_df)
    
    print("Cleaning and preparing data...")
    final_df = DataPipeline.clean_and_prepare(normalized_df)
    
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'processed'))
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'restaurants.parquet')
    
    print(f"Saving {len(final_df)} processed records to {output_path}...")
    final_df.to_parquet(output_path, engine='fastparquet')
    
    print("Ingestion complete!")

if __name__ == "__main__":
    main()
