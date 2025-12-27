
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

## 🐳 Container Deployment

This application supports both **Docker** and **Podman** container runtimes.

### Quick Start with Podman/Docker Compose (Recommended)

1. **Build and run**
   ```bash
   # With Podman
   podman compose up -d
   
   # With Docker
   docker-compose up -d
   ```

2. **Access the app**
   - Open http://localhost:8501

3. **View logs**
   ```bash
   # Podman
   podman compose logs -f
   
   # Docker
   docker-compose logs -f
   ```

4. **Stop the app**
   ```bash
   # Podman
   podman compose down
   
   # Docker
   docker-compose down
   ```

### Manual Build and Run

#### Using Podman
```bash
# Build
podman build -t anime-codex:latest .

# Run
podman run -d \
  --name anime-codex \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data:ro \
  anime-codex:latest

# Logs
podman logs -f anime-codex

# Stop
podman stop anime-codex
podman rm anime-codex
```

#### Using Docker
```bash
# Build
docker build -t anime-codex:latest .

# Run
docker run -d \
  --name anime-codex \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data:ro \
  --restart unless-stopped \
  anime-codex:latest

# Logs
docker logs -f anime-codex

# Stop
docker stop anime-codex
docker rm anime-codex
```

> **Note**: Podman users may see a HEALTHCHECK warning - this is normal and doesn't affect functionality.

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
- `Dockerfile`: Container image definition.
- `docker-compose.yml`: Orchestration configuration.

## Tech Stack
- **Backend**: Python 3.11, Pandas, scikit-learn
- **Frontend**: Streamlit with Material UI design
- **ML Models**: TF-IDF, Truncated SVD
- **Deployment**: Docker/Podman, Docker Compose
- **Containerization**: OCI-compliant images

