
import streamlit as st
import json

def set_page_config():
    st.set_page_config(
        page_title="Anime Codex",
        page_icon="⛩️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Roboto+Slab:wght@600;700&display=swap');
        
        /* Material Design Base */
        .stApp {
            background: #121212;
            font-family: 'Roboto', sans-serif;
        }
        
        /* Container - Centered with max-width */
        .main .block-container {
            max-width: 1400px;
            padding-left: 3rem;
            padding-right: 3rem;
            padding-top: 3rem;
            padding-bottom: 3rem;
            margin: 0 auto;
        }
        
        /* Responsive padding */
        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 1.5rem;
                padding-right: 1.5rem;
            }
        }
        
        /* Headers - Material Typography */
        h1, h2, h3 {
            font-family: 'Roboto Slab', serif;
            color: #ffffff;
            font-weight: 700;
        }
        
        h1 {
            font-size: 3.5rem;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }
        
        h1 span {
            background: linear-gradient(135deg, #FF6B9D, #C44569);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Subtitle */
        .stApp > div > div > div > div > p {
            color: #B0B0B0;
            font-size: 1.15rem;
            font-weight: 300;
            margin-bottom: 2.5rem;
            letter-spacing: 0.3px;
        }
        
        /* Material Elevation - Input Fields */
        .stSelectbox div[data-baseweb="select"] > div {
            background: #1E1E1E;
            border: 1px solid #2C2C2C;
            color: white !important;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .stSelectbox div[data-baseweb="select"] > div:hover {
            border-color: #FF6B9D;
            box-shadow: 0 4px 8px rgba(255, 107, 157, 0.15);
        }
        
        .stSelectbox div[data-baseweb="select"] > div:focus-within {
            border-color: #FF6B9D;
            box-shadow: 0 0 0 3px rgba(255, 107, 157, 0.1);
        }
        
        /* Material Cards with Elevation */
        .anime-card {
            background: #1E1E1E;
            border-radius: 8px;
            margin-bottom: 24px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            overflow: hidden;
            box-shadow: 
                0 2px 4px rgba(0,0,0,0.2),
                0 1px 2px rgba(0,0,0,0.15);
            cursor: pointer;
            position: relative;
        }
        
        .anime-card:hover {
            box-shadow: 
                0 8px 16px rgba(0,0,0,0.3),
                0 4px 8px rgba(0,0,0,0.25),
                0 0 0 2px #FF6B9D;
            transform: translateY(-4px);
        }
        
        .anime-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #FF6B9D, #C44569);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .anime-card:hover::before {
            opacity: 1;
        }
        
        /* Card Image */
        .anime-img-container {
            position: relative;
            overflow: hidden;
            height: 340px;
            background: #2C2C2C;
        }
        
        .anime-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .anime-card:hover .anime-img {
            transform: scale(1.05);
        }
        
        .anime-img-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 60%;
            background: linear-gradient(to top, rgba(18,18,18,0.95), transparent);
            pointer-events: none;
        }
        
        /* Card Content */
        .anime-content {
            padding: 16px 20px 20px;
        }
        
        .anime-title {
            font-size: 1.25rem;
            font-weight: 500;
            color: #FFFFFF;
            margin-bottom: 10px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            letter-spacing: 0.3px;
        }
        
        .anime-meta {
            font-size: 0.9rem;
            color: #B0B0B0;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        /* Material Chip - Rating Badge */
        .rating-badge {
            background: linear-gradient(135deg, #FF6B9D, #C44569);
            color: white;
            padding: 5px 14px;
            border-radius: 16px;
            font-size: 0.875rem;
            font-weight: 500;
            box-shadow: 0 2px 4px rgba(255, 107, 157, 0.3);
            display: inline-flex;
            align-items: center;
            gap: 4px;
            letter-spacing: 0.3px;
        }
        
        .genre-text {
            color: #909090;
            font-size: 0.875rem;
            line-height: 1.5;
            font-weight: 300;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        
        /* Material Button */
        .stButton button {
            background: linear-gradient(135deg, #FF6B9D, #C44569);
            color: white;
            border: none;
            border-radius: 4px;
            padding: 12px 32px;
            font-weight: 500;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 1.25px;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 
                0 2px 4px rgba(255, 107, 157, 0.3),
                0 1px 2px rgba(255, 107, 157, 0.2);
        }
        
        .stButton button:hover {
            box-shadow: 
                0 4px 8px rgba(255, 107, 157, 0.4),
                0 2px 4px rgba(255, 107, 157, 0.3);
            transform: translateY(-2px);
        }
        
        .stButton button:active {
            transform: translateY(0);
            box-shadow: 
                0 2px 4px rgba(255, 107, 157, 0.3);
        }
        
        /* Search Section */
        h3 {
            color: #FFFFFF;
            font-size: 1.5rem;
            margin-top: 2.5rem;
            margin-bottom: 1.2rem;
            font-weight: 500;
        }
        
        /* Material Spinner */
        .stSpinner > div {
            border-top-color: #FF6B9D !important;
        }
        
        /* Material Expansion Panel */
        .streamlit-expanderHeader {
            background: #1E1E1E;
            border-radius: 4px;
            color: #ffffff;
            font-weight: 500;
            padding: 12px 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }
        
        .streamlit-expanderHeader:hover {
            background: #252525;
        }
        
        /* Alerts */
        .stSuccess, .stWarning, .stError {
            background: #1E1E1E;
            border-radius: 4px;
            border-left: 4px solid;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        .stSuccess {
            border-left-color: #4CAF50;
        }
        
        .stWarning {
            border-left-color: #FF9800;
        }
        
        .stError {
            border-left-color: #F44336;
        }
        
        /* Divider */
        hr {
            border-color: #2C2C2C;
            margin: 2.5rem 0;
        }
        
        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 9999;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.7);
            animation: fadeIn 0.2s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .modal-content {
            background: #1E1E1E;
            margin: 3% auto;
            padding: 0;
            border-radius: 8px;
            width: 90%;
            max-width: 900px;
            max-height: 85vh;
            overflow-y: auto;
            box-shadow: 
                0 24px 48px rgba(0,0,0,0.5),
                0 12px 24px rgba(0,0,0,0.4);
            animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        @keyframes slideIn {
            from {
                transform: translateY(-50px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        .modal-header {
            position: relative;
            height: 400px;
            overflow: hidden;
        }
        
        .modal-header img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            filter: brightness(0.7);
        }
        
        .modal-header-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 32px;
            background: linear-gradient(to top, rgba(18,18,18,1), transparent);
        }
        
        .modal-title {
            font-size: 2.5rem;
            font-weight: 700;
            color: white;
            margin-bottom: 12px;
            font-family: 'Roboto Slab', serif;
        }
        
        .modal-body {
            padding: 32px;
        }
        
        .modal-section {
            margin-bottom: 24px;
        }
        
        .modal-section-title {
            font-size: 1.1rem;
            font-weight: 500;
            color: #FF6B9D;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .modal-section-content {
            color: #B0B0B0;
            line-height: 1.6;
            font-size: 1rem;
        }
        
        .close {
            position: absolute;
            right: 24px;
            top: 24px;
            color: white;
            font-size: 36px;
            font-weight: 300;
            cursor: pointer;
            z-index: 1;
            width: 48px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(0,0,0,0.5);
            border-radius: 50%;
            transition: all 0.2s ease;
        }
        
        .close:hover {
            background: rgba(255, 107, 157, 0.8);
            transform: rotate(90deg);
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-top: 12px;
        }
        
        .info-item {
            background: #252525;
            padding: 16px;
            border-radius: 4px;
            border-left: 3px solid #FF6B9D;
        }
        
        .info-label {
            font-size: 0.85rem;
            color: #909090;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }
        
        .info-value {
            font-size: 1.1rem;
            color: #FFFFFF;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)

def render_anime_card(details, card_id):
    """Renders an anime card with click-to-open modal functionality"""
    
    image = details.get('image_url')
    if not image or image == "None":
        image = "https://via.placeholder.com/300x450?text=No+Image"
    
    # Handle episodes safely
    try:
        episodes = float(details['episodes'])
        eps_text = f"{episodes:.0f} eps" if episodes > 0 else "?"
    except:
        eps_text = "?"
    
    # Escape quotes for JSON
    details_json = json.dumps(details).replace("'", "\\'")
        
    card_html = f"""
    <div class="anime-card" onclick="openModal{card_id}()">
        <div class="anime-img-container">
            <img src="{image}" class="anime-img" alt="{details['title']}">
            <div class="anime-img-overlay"></div>
        </div>
        <div class="anime-content">
            <div class="anime-title" title="{details['title']}">{details['title']}</div>
            <div class="anime-meta">
                <span class="rating-badge">★ {details['rating']}</span>
                <span>• {details['type']}</span>
                <span>• {eps_text}</span>
            </div>
            <div class="genre-text">
                {details['genres']}
            </div>
        </div>
    </div>
    
    <!-- Modal -->
    <div id="modal{card_id}" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <img src="{image}" alt="{details['title']}">
                <span class="close" onclick="closeModal{card_id}()">&times;</span>
                <div class="modal-header-overlay">
                    <div class="modal-title">{details['title']}</div>
                    <div class="rating-badge">★ {details['rating']}</div>
                </div>
            </div>
            <div class="modal-body">
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">Type</div>
                        <div class="info-value">{details['type']}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Episodes</div>
                        <div class="info-value">{eps_text}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Rating</div>
                        <div class="info-value">{details['rating']}</div>
                    </div>
                </div>
                
                <div class="modal-section">
                    <div class="modal-section-title">Genres</div>
                    <div class="modal-section-content">{details['genres']}</div>
                </div>
                
                <div class="modal-section">
                    <div class="modal-section-title">Match Score</div>
                    <div class="modal-section-content">
                        This anime has a similarity score of {details['score']:.3f} based on content and collaborative filtering.
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function openModal{card_id}() {{
            document.getElementById("modal{card_id}").style.display = "block";
        }}
        
        function closeModal{card_id}() {{
            document.getElementById("modal{card_id}").style.display = "none";
        }}
        
        // Close modal when clicking outside
        window.onclick = function(event) {{
            var modal = document.getElementById("modal{card_id}");
            if (event.target == modal) {{
                modal.style.display = "none";
            }}
        }}
    </script>
    """
    st.markdown(card_html, unsafe_allow_html=True)
