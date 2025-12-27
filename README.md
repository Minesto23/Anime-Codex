
# Anime Codex ⛩️

A modern, hybrid AI-powered anime recommendation application. 

**Anime Codex** uses a combination of Content-Based Filtering (Genres, Type, Synopsis) and Collaborative Filtering (SVD on User Ratings) to suggest anime you'll love, discovering both popular hits and hidden gems.

## Features
- **Hybrid Recommendation Engine**: Balances what specific users liked with content similarity.
- **Search Autocomplete**: Instantly find anime from a database of 20,000+ entries.
- **Modern Dark UI**: A sleek, responsiveness interface built with Streamlit.
- **Hidden Gem Discovery**: Algorithms boosted to surface high-rated but less mainstream series.

## Setup & Installation

1. **Prerequisites**
   - Python 3.9+ installed.
   - Data files placed in the `data/` directory.

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare Data**
   The application processes raw CSV data on the first run.
   - Ensure `anime.csv`, `ratings.csv` (or `final_animedataset.csv`) are in `data/`.
   - Run the data loader manually (optional, app handles it too):
     ```bash
     python src/data_loader.py
     ```

4. **Run the App**
   ```bash
   streamlit run app.py
   ```

## How It Works

### Hybrid Engine strategy
1. **Content Matching**: We use **TF-IDF** on anime Genres, Types, and Synopses to find show with similar themes.
2. **Collaborative Filtering**: We use **Truncated SVD** (Matrix Factorization) to find patterns in user ratings, identifying anime that similar users enjoyed.
3. **Scoring**: 
   - `Final Score = (Content_Similarity * 0.4) + (Collaborative_Score * 0.6)`
   - Scores are boosted for high-rated shows and penalized slightly for hyper-popular ones to ensure variety.

## Directory Structure
- `app.py`: Main application entry point.
- `src/`: Source code for models, data loading, and UI.
- `data/`: Dataset storage (ignored in git).
