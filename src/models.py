
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MinMaxScaler
import pickle
import os

class ContentRecommender:
    def __init__(self, anime_df):
        self.anime_df = anime_df
        self.tfidf_matrix = None
        self.indices = None
        
    def fit(self):
        print("Training Content Recommender...")
        # Create a soup of metadata for TF-IDF
        # Filling NaNs
        self.anime_df['genre'] = self.anime_df['genre'].fillna('')
        self.anime_df['type'] = self.anime_df['type'].fillna('')
        self.anime_df['synopsis'] = self.anime_df['synopsis'].fillna('')
        self.anime_df['rating'] = self.anime_df['rating'].fillna(0)
        
        # Weighted Soup: Genre is most important, Type adds context, Synopsis adds detail
        # We repeat genre to give it more weight naturally in the text
        self.anime_df['soup'] = (
            (self.anime_df['genre'] + " ") * 2 + 
            self.anime_df['type'] + " " + 
            self.anime_df['synopsis']
        )
        
        tfidf = TfidfVectorizer(stop_words='english', min_df=3, max_features=5000)
        self.tfidf_matrix = tfidf.fit_transform(self.anime_df['soup'])
        
        # Mapping Name -> Index
        self.indices = pd.Series(self.anime_df.index, index=self.anime_df['name']).drop_duplicates()
        print("Content Recommender Trained.")

    def get_recommendations(self, anime_id, top_n=20):
        # Get index from anime_id
        idx = self.anime_df.index[self.anime_df['anime_id'] == anime_id].tolist()
        if not idx:
            return {}
        idx = idx[0]
        
        # Cosine Similarity
        # Efficiently compute only for the validation vector
        cosine_sim = cosine_similarity(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
        
        # Get scores
        sim_scores = list(enumerate(cosine_sim))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Top N (excluding self)
        sim_scores = sim_scores[1:top_n+1]
        
        # Return Dict {anime_id: score}
        anime_indices = [i[0] for i in sim_scores]
        scores = [i[1] for i in sim_scores]
        
        rec_ids = self.anime_df.iloc[anime_indices]['anime_id'].values
        return dict(zip(rec_ids, scores))


class CollaborativeRecommender:
    def __init__(self, ratings_df):
        self.ratings_df = ratings_df
        self.algo = None
        self.pivoted_ratings = None
        self.corr_matrix = None
        
    def fit(self):
        print("Training Collaborative Recommender...")
        # Pivot Table: Users x Anime
        # Warning: This can be huge. We use SVD on sparse matrix if possible, 
        # but for simplicity and "Item-Item" finding, we can use a Pivot + Correlation or SVD.
        
        # Let's use Truncated SVD for dimensionality reduction
        # Create Sparse Matrix from User-Item ratings
        user_item_matrix = self.ratings_df.pivot_table(index='user_id', columns='anime_id', values='rating').fillna(0)
        
        # Transpose to Item-User for Item-Item similarity
        item_user_matrix = user_item_matrix.T
        
        # SVD
        SVD = TruncatedSVD(n_components=12, random_state=42)
        matrix = SVD.fit_transform(item_user_matrix)
        
        # Compute Correlation Matrix (Item-Item)
        self.corr_matrix = np.corrcoef(matrix)
        
        # Map anime_id to matrix index
        self.anime_id_to_idx = {id_: i for i, id_ in enumerate(item_user_matrix.index)}
        self.idx_to_anime_id = {i: id_ for i, id_ in enumerate(item_user_matrix.index)}
        
        print("Collaborative Recommender Trained.")

    def get_recommendations(self, anime_id, top_n=20):
        if anime_id not in self.anime_id_to_idx:
            return {}
        
        idx = self.anime_id_to_idx[anime_id]
        
        # Correlation vector for this anime
        corr_vector = self.corr_matrix[idx]
        
        # Sort indices
        sorted_indices = np.argsort(corr_vector)[::-1]
        
        # Top N
        top_indices = sorted_indices[1:top_n+1]
        
        rec_ids = [self.idx_to_anime_id[i] for i in top_indices]
        scores = [corr_vector[i] for i in top_indices]
        
        return dict(zip(rec_ids, scores))


class HybridRecommender:
    def __init__(self, anime_df, ratings_df):
        self.anime_df = anime_df
        self.content_engine = ContentRecommender(anime_df)
        self.collab_engine = CollaborativeRecommender(ratings_df)
        
    def fit(self):
        self.content_engine.fit()
        self.collab_engine.fit()
        
    def recommend(self, anime_name, weights={'content': 0.4, 'collab': 0.6}, top_k=3):
        # 1. Fuzzy Match / Lookup ID
        # Simple Case-Insensitive Exact Match first
        matches = self.anime_df[self.anime_df['name'].str.contains(anime_name, case=False, regex=False)]
        
        if matches.empty:
            # Try splitting generic matching
             return [], "Anime not found. Try a more specific name."
             
        # Assume user meant the most popular result (most members) or exact match
        target_anime = matches.sort_values(by='rating', ascending=False).iloc[0]
        target_id = target_anime['anime_id']
        target_name = target_anime['name']
        
        print(f"Generating recommendations for: {target_name} ({target_id})")
        
        # 2. Get Scores
        content_scores = self.content_engine.get_recommendations(target_id, top_n=50)
        collab_scores = self.collab_engine.get_recommendations(target_id, top_n=50)
        
        # 3. Merge Scores
        # We need to normalize scores or just sum them if they are in same range (0-1)
        # Cosine Sim is -1 to 1 (mostly 0-1 for TF-IDF). Corr is -1 to 1. 
        
        all_ids = set(content_scores.keys()) | set(collab_scores.keys())
        final_scores = []
        
        for aid in all_ids:
            c_score = content_scores.get(aid, 0)
            cl_score = collab_scores.get(aid, 0)
            
            # Hybrid Score
            final_score = (c_score * weights['content']) + (cl_score * weights['collab'])
            
            # 4. Hidden Gem & Popularity Bias
            # Get metadata
            meta = self.anime_df[self.anime_df['anime_id'] == aid]
            if meta.empty:
                continue
            meta = meta.iloc[0]
            
            # Boost: High Rating
            try:
                if float(meta['rating']) > 8.0:
                    final_score *= 1.1
            except (ValueError, TypeError):
                # Skip boost if rating is UNKNOWN or invalid
                pass
            
            # Penalize: Extremely Popular (if desired, to avoid "Attack on Titan" everywhere)
            # if meta['members'] > 1_000_000:
            #     final_score *= 0.9
                
            final_scores.append((aid, final_score))
            
        # Sort
        final_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Get Top K details with sequel/spin-off filtering
        results = []
        # Extract main words from target name for filtering
        import re
        target_words = set(re.findall(r'\b\w{4,}\b', target_name.lower()))  # Words with 4+ chars
        
        for aid, score in final_scores:
            if len(results) >= top_k:
                break
                
            meta = self.anime_df[self.anime_df['anime_id'] == aid].iloc[0]
            rec_name = meta['name']
            
            # Filter out sequels/spin-offs by checking name similarity
            rec_words = set(re.findall(r'\b\w{4,}\b', rec_name.lower()))
            
            # Skip if more than 60% of target words are in the recommendation
            if target_words and rec_words:
                overlap = len(target_words & rec_words) / len(target_words)
                if overlap > 0.6:
                    continue
            
            results.append({
                'title': rec_name,
                'genres': meta['genre'],
                'rating': meta['rating'],
                'episodes': meta['episodes'],
                'type': meta['type'],
                'image_url': meta['image_url'],
                'score': score
            })
            
        return results, target_name
