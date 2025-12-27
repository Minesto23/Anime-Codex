
import streamlit as st
import pandas as pd
from src.data_loader import DataLoader
from src.models import HybridRecommender
from src.ui_components import set_page_config, inject_custom_css, render_anime_card
import os

# Page Config
set_page_config()
inject_custom_css()

# Helper to load resources (cached)
@st.cache_resource(show_spinner=True)
def load_resources():
    loader = DataLoader()
    anime_df, ratings_df = loader.load_data()
    
    recommender = HybridRecommender(anime_df, ratings_df)
    recommender.fit()
    
    return recommender, anime_df

# UI Layout
def main():
    st.markdown("<h1>⛩️ Anime <span>Codex</span></h1>", unsafe_allow_html=True)
    st.markdown("<p>Discover your next favorite anime using AI-powered hybrid recommendation engine.</p>", unsafe_allow_html=True)
    
    # Load Data
    with st.spinner("Initializing Codex..."):
        recommender, anime_df = load_resources()
    
    # Search Section
    st.markdown("### 🔍 Find recommendations based on")
    
    # Autocomplete
    all_anime_names = anime_df['name'].tolist()
    selected_anime = st.selectbox(
        "Select an anime you liked:",
        options=[""] + all_anime_names,
        format_func=lambda x: "Type to search..." if x == "" else x,
        help="Start typing to search for an anime."
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Generate Recommendations", use_container_width=True):
            if not selected_anime:
                st.warning("Please select an anime first.")
            else:
                with st.spinner(f"Analyzing {selected_anime} and finding match..."):
                    recommendations, target_name = recommender.recommend(selected_anime, top_k=6)
                
                if not recommendations:
                    st.error(target_name) # Error message returned
                else:
                    st.success(f"Because you liked **{target_name}**:")
                    st.markdown("---")
                    
                    # Display Results - 2 rows of 3 cards
                    # First row
                    r_col1, r_col2, r_col3 = st.columns(3)
                    with r_col1:
                        render_anime_card(recommendations[0], 0)
                    with r_col2:
                        render_anime_card(recommendations[1], 1)
                    with r_col3:
                        render_anime_card(recommendations[2], 2)
                    
                    # Second row
                    r_col4, r_col5, r_col6 = st.columns(3)
                    with r_col4:
                        render_anime_card(recommendations[3], 3)
                    with r_col5:
                        render_anime_card(recommendations[4], 4)
                    with r_col6:
                        render_anime_card(recommendations[5], 5)
                        
                    # Detailed Explanation (Optional / Expandable)
                    with st.expander("ℹ️ Why these recommendations?"):
                        st.write("These recommendations utilize a Hybrid engine combining content similarity (genres, synopsis) and collaborative filtering (what similar users liked).")
                        st.json(recommendations)

if __name__ == "__main__":
    main()
