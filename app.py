import streamlit as st
from utils import load_data, load_image
from config import *

def get_valid_columns(data, columns):
    """Return only columns that exist in the dataframe"""
    return [col for col in columns if col in data.columns]

def render_data_section(data):
    with st.container():
        st.subheader("📊 Player Statistics")
        search = st.text_input("Search players:", "")
        if 'Nombre' in data.columns:
            filtered_data = data[data['Nombre'].str.contains(search, case=False)] if search else data
            st.dataframe(filtered_data, height=400)
        else:
            st.error("Required column 'Nombre' not found in the data.")

def render_contract_analysis(contract_image):
    with st.container():
        st.subheader("💰 Contract Analysis")
        if contract_image is not None:
            st.image(contract_image, use_column_width=True)
            with st.expander("About this visualization"):
                st.write("""
                This graph shows the relationship between player contracts and their 
                performance statistics. It helps identify patterns between player 
                compensation and their on-court performance.
                """)
        else:
            st.warning("Contract analysis visualization is currently unavailable.")

def render_player_analysis(data, player_image):
    with st.container():
        st.subheader("👤 Player Analysis")
        
        # Player selection without team filter initially
        available_players = data['Nombre'].dropna().unique() if 'Nombre' in data.columns else []
        
        if len(available_players) == 0:
            st.error("No player data available.")
            return
            
        player = st.selectbox(
            "Select a player to analyze:",
            options=available_players
        )
        
        # Display player information
        if player:
            player_data = data[data['Nombre'] == player].iloc[0]
            
            # Display available stats
            st.write("### Quick Stats")
            cols = st.columns(4)
            stats = ['PTS', 'AST', 'REB', 'FG%']
            available_stats = get_valid_columns(data, stats)
            
            for col, stat in zip(cols, available_stats):
                try:
                    value = player_data[stat]
                    if pd.notna(value):  # Check if value is not NaN
                        col.metric(stat, f"{value:.1f}")
                    else:
                        col.metric(stat, "N/A")
                except Exception:
                    col.metric(stat, "N/A")
            
            # Try to load and display player image
            try:
                if player_image is not None:
                    st.image(player_image, use_column_width=True)
            except Exception:
                st.warning("Player visualization is currently unavailable.")

def render_yearly_stats(stat_image):
    with st.container():
        st.subheader("📈 Yearly Statistics")
        
        # Get available stats from the actual data columns
        available_stats = get_valid_columns(st.session_state.get('data', pd.DataFrame()), STATS_COLUMNS)
        
        if not available_stats:
            st.error("No statistics data available.")
            return
            
        # Organize available stats in categories
        categories = {
            "Scoring": ['PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%'],
            "Rebounds": ['OREB', 'DREB'],
            "Playmaking": ['AST', 'TOV'],
            "Defense": ['STL', 'BLK', 'PF'],
            "Other": ['RANK', 'AGE', 'GP', 'MIN', '+-', 'DD2', 'FP', 'TD3']
        }
        
        # Filter categories to only include available stats
        valid_categories = {}
        for category, stats in categories.items():
            valid_stats = [stat for stat in stats if stat in available_stats]
            if valid_stats:
                valid_categories[category] = valid_stats
        
        if not valid_categories:
            st.error("No valid statistics categories available.")
            return
            
        # Two-level selection
        category = st.selectbox("Select category:", list(valid_categories.keys()))
        stat = st.selectbox("Select statistic:", valid_categories[category])
        
        try:
            if stat_image is not None:
                st.image(stat_image, use_column_width=True)
                with st.expander("Understanding this trend"):
                    st.write(f"""
                    This visualization shows how the {stat} statistic has evolved over the years 
                    in the WNBA. It helps identify league-wide trends and patterns in player performance.
                    """)
            else:
                st.warning(f"Visualization for {stat} is currently unavailable.")
        except Exception:
            st.warning("Statistics visualization is currently unavailable.")

def main():
    st.set_page_config(page_title="WNBA Statistics", layout="wide")
    
    # Custom CSS
    st.markdown("""
        <style>
        .stSelectbox {margin-bottom: 1rem;}
        .stExpander {margin-top: 1rem;}
        .stContainer {margin-bottom: 2rem;}
        div[data-testid="stMetricValue"] {
            font-size: 24px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("🏀 WNBA Player Statistics (2016-2024)")
    
    # Load data first
    data = load_data(DATA_URL)
    if data is None:
        st.error("Failed to load data. Please try again later.")
        return
        
    # Store data in session state for access across the app
    st.session_state['data'] = data
    
    # Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Overview", "Player Analysis", "League Trends"]
    )
    
    # Main content based on navigation
    if page == "Overview":
        col1, col2 = st.columns([2, 1])
        with col1:
            render_data_section(data)
        with col2:
            contract_image = load_image(CONTRACT_GRAPH_URL)
            render_contract_analysis(contract_image)
            
    elif page == "Player Analysis":
        if 'Nombre' not in data.columns:
            st.error("Player data is not available. Required column 'Nombre' is missing.")
            return
            
        player = data['Nombre'].iloc[0] if not data.empty else None
        if player:
            player_graph_url = f"{INDIVIDUAL_GRAPHS_DIR}{player.replace(' ', '_')}.png"
            player_image = load_image(player_graph_url)
            render_player_analysis(data, player_image)
        else:
            st.error("No player data available.")
        
    else:  # League Trends
        available_stats = get_valid_columns(data, STATS_COLUMNS)
        if available_stats:
            stat = available_stats[0]
            stat_graph_url = f"{YEARLY_GRAPHS_DIR}{stat.replace(' ', '_')}.png"
            stat_image = load_image(stat_graph_url)
            render_yearly_stats(stat_image)
        else:
            st.error("Statistics data is not available.")

if __name__ == "__main__":
    main()
