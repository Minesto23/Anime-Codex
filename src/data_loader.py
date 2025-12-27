
import pandas as pd
import os
import glob
import logging

class DataLoader:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        
        # Paths for processed data
        self.anime_path = os.path.join(data_dir, "anime_processed.pkl")
        self.ratings_path = os.path.join(data_dir, "ratings_processed.pkl")
        
    def load_data(self):
        """Loads processed data if available, otherwise processes raw data."""
        if os.path.exists(self.anime_path) and os.path.exists(self.ratings_path):
            print("Loading pre-processed data...")
            return pd.read_pickle(self.anime_path), pd.read_pickle(self.ratings_path)
        
        print("Processing raw data for the first time... This may take a while.")
        return self._process_raw_data()
    
    def _process_raw_data(self):
        # 1. Load Anime Metadata (prioritizing 2023 dataset for more fields)
        # Using basic anime.csv as fallback/base if needed, but 2023 has 'Image URL'
        
        # Load anime-dataset-2023.csv (Metadata rich)
        anime_2023_path = os.path.join(self.data_dir, "anime-dataset-2023.csv")
        if os.path.exists(anime_2023_path):
             # Load relevant columns only to save memory
            anime_df = pd.read_csv(anime_2023_path, usecols=[
                'anime_id', 'Name', 'English name', 'Genres', 'Type', 'Score', 
                'Episodes', 'Synopsis', 'Image URL'
            ])
            # Rename for consistency
            anime_df = anime_df.rename(columns={
                'Name': 'name', 'English name': 'english_name', 'Genres': 'genre', 
                'Score': 'rating', 'Synopsis': 'synopsis', 'Image URL': 'image_url',
                 'Type': 'type', 'Episodes': 'episodes'
            })
        else:
            # Fallback to older anime.csv
            print(f"Warning: {anime_2023_path} not found. Using basic anime.csv")
            anime_path = os.path.join(self.data_dir, "anime.csv")
            anime_df = pd.read_csv(anime_path)
            # Normalize columns
            anime_df = anime_df.rename(columns={'name': 'name', 'genre': 'genre', 'type': 'type', 'rating': 'rating'})
            anime_df['image_url'] = None # No images in old dataset
            anime_df['synopsis'] = ""

        # Drop duplicates
        anime_df = anime_df.drop_duplicates(subset=['anime_id'])
        anime_df = anime_df.dropna(subset=['name'])
        
        # 2. Process Ratings (The heavy part)
        # We need to filter this aggressively for local performance
        
        # Options: final_animedataset.csv (4.5GB) or rating.csv
        # Let's try to find final_animedataset.csv first
        
        ratings_path = os.path.join(self.data_dir, "final_animedataset.csv")
        
        # We will use chunks to process the large file
        # Goal: Keep top users by activity and top anime by popularity to reduce matrix size
        
        if os.path.exists(ratings_path):
            print(f"Processing large dataset: {ratings_path}")
            
            # Strategy:
            # 1. First pass: Count ratings per user and per anime
            # 2. Filter: Keep users with > 50 ratings, Anime with > 50 ratings
            # 3. Sample: If still too big, take top N users or random sample
            
            # Since we can't load 4.5GB into memory on all machines to filter, we iterate.
            # However, for a prototype, let's try reading a significant sample or use the 'user_id' logic if available.
            # The 'final_animedataset.csv' has columns: username, anime_id, my_score, ...
            
            # Let's load just necessary columns
            chunk_size = 500000
            chunks = []
            
            # Heuristic limit: Load first 5 million rows? Or just robust sampling?
            # Better: Load random sample or just valid ratings.
            
            # Let's load the first 2 million rows for the prototype to ensure speed
            # 2 million ratings is plenty for good recs.
            
            df_iter = pd.read_csv(ratings_path, usecols=['user_id', 'anime_id', 'my_score'], chunksize=chunk_size)
            
            processed_rows = 0
            limit_rows = 2_000_000 # 2 Million ratings max for local performance
            
            for chunk in df_iter:
                # Filter valid ratings
                chunk = chunk[chunk['my_score'] > 0] 
                chunks.append(chunk)
                processed_rows += len(chunk)
                if processed_rows >= limit_rows:
                    break
            
            ratings_df = pd.concat(chunks)
            
            # Rename
            ratings_df = ratings_df.rename(columns={'my_score': 'rating'})
            
        else:
            # Fallback to mall_ratings.csv or others
            print("Large dataset not found, looking for standard ratings.csv")
            fallback_path = glob.glob(os.path.join(self.data_dir, "*ratings*.csv"))
            if fallback_path:
                 ratings_df = pd.read_csv(fallback_path[0])
                 # rename if needed [user_id, anime_id, rating]
            else:
                raise FileNotFoundError("No ratings file found in data/")

        # Final Cleanup
        # Ensure ratings only include anime we have metadata for
        ratings_df = ratings_df[ratings_df['anime_id'].isin(anime_df['anime_id'])]
        
        # Filter users with too few ratings (cold start noise)
        user_counts = ratings_df['user_id'].value_counts()
        active_users = user_counts[user_counts >= 10].index
        ratings_df = ratings_df[ratings_df['user_id'].isin(active_users)]

        print(f"Processed Data: {len(anime_df)} Anime, {len(ratings_df)} Ratings")
        
        # Save optimized files
        anime_df.to_pickle(self.anime_path)
        ratings_df.to_pickle(self.ratings_path)
        
        return anime_df, ratings_df

if __name__ == "__main__":
    loader = DataLoader()
    loader.load_data()
