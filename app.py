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
        
        # Validate required columns
        required_columns = ['Nombre', 'Team']
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            return

        # Player selection with additional filters
        col1, col2 = st.columns(2)
        with col1:
            teams = sorted(data['Team'].dropna().unique())
            team_filter = st.multiselect(
                "Filter by Team:",
                options=teams
            )
        
        with col2:
            positions = sorted(data['Position'].dropna().unique()) if 'Position' in data.columns else []
            position_filter = st.multiselect(
                "Filter by Position:",
                options=positions
            )
        
        # Filter players based on selections
        filtered_data = data.copy()
        if team_filter:
            filtered_data = filtered_data[filtered_data['Team'].isin(team_filter)]
        if position_filter:
            filtered_data = filtered_data[filtered_data['Position'].isin(position_filter)]
        
        # Ensure we have players to display
        available_players = filtered_data['Nombre'].dropna().unique()
        if len(available_players) == 0:
            st.warning("No players found with the selected filters.")
            return
            
        player = st.selectbox(
            "Select a player to analyze:",
            options=available_players
        )
        
        # Display player information
        if player_image is not None:
            st.image(player_image, use_column_width=True)
            
            # Player stats summary
            if not filtered_data.empty:
                player_stats = filtered_data[filtered_data['Nombre'] == player].iloc[0]
                st.write("### Quick Stats")
                cols = st.columns(4)
                stats = ['PTS', 'AST', 'REB', 'FG%']
                available_stats = get_valid_columns(filtered_data, stats)
                
                for col, stat in zip(cols, available_stats):
                    try:
                        value = player_stats[stat]
                        if pd.notna(value):  # Check if value is not NaN
                            col.metric(stat, f"{value:.1f}")
                        else:
                            col.metric(stat, "N/A")
                    except Exception:
                        col.metric(stat, "N/A")
        else:
            st.warning("Player statistics visualization is currently unavailable.")

def render_yearly_stats(stat_image):
    with st.container():
        st.subheader("📈 Yearly Statistics")
        
        # Organize stats in categories
        categories = {
            "Scoring": ['PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%'],
            "Rebounds": ['OREB', 'DREB'],
            "Playmaking": ['AST', 'TOV'],
            "Defense": ['STL', 'BLK', 'PF'],
            "Other": ['RANK', 'AGE', 'GP', 'MIN', '+-', 'DD2', 'FP', 'TD3']
        }
        
        # Filter out categories with no valid stats
        valid_categories = {}
        for category, stats in categories.items():
            if any(stat in STATS_COLUMNS for stat in stats):
                valid_categories[category] = [stat for stat in stats if stat in STATS_COLUMNS]
        
        if not valid_categories:
            st.error("No valid statistics categories available.")
            return
            
        # Two-level selection
        category = st.selectbox("Select category:", list(valid_categories.keys()))
        stat = st.selectbox("Select statistic:", valid_categories[category])
        
        if stat_image is not None:
            st.image(stat_image, use_column_width=True)
            with st.expander("Understanding this trend"):
                st.write(f"""
                This visualization shows how the {stat} statistic has evolved over the years 
                in the WNBA. It helps identify league-wide trends and patterns in player performance.
                """)
        else:
            st.warning(f"Visualization for {stat} is currently unavailable.")

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
    
    # Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Overview", "Player Analysis", "League Trends"]
    )
    
    # Load data
    data = load_data(DATA_URL)
    if data is None:
        st.error("Failed to load data. Please try again later.")
        return
    
    # Main content based on navigation
    if page == "Overview":
        col1, col2 = st.columns([2, 1])
        with col1:
            render_data_section(data)
        with col2:
            contract_image = load_image(CONTRACT_GRAPH_URL)
            render_contract_analysis(contract_image)
            
    elif page == "Player Analysis":
        player = st.session_state.get('selected_player', data['Nombre'].iloc[0] if 'Nombre' in data.columns else None)
        if player:
            player_graph_url = f"{INDIVIDUAL_GRAPHS_DIR}{player.replace(' ', '_')}.png"
            player_image = load_image(player_graph_url)
            render_player_analysis(data, player_image)
        else:
            st.error("Player data is not available.")
        
    else:  # League Trends
        stat = st.session_state.get('selected_stat', STATS_COLUMNS[0] if STATS_COLUMNS else None)
        if stat:
            stat_graph_url = f"{YEARLY_GRAPHS_DIR}{stat.replace(' ', '_')}.png"
            stat_image = load_image(stat_graph_url)
            render_yearly_stats(stat_image)
        else:
            st.error("Statistics data is not available.")

if __name__ == "__main__":
    main()
