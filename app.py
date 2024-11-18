import streamlit as st
import pandas as pd
from utils import (
    create_scoring_chart,
    create_efficiency_chart,
    create_team_stats,
    create_player_radar_chart
)

# Page configuration
st.set_page_config(
    page_title="WNBA Statistics Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 1rem;
    }
    .stPlotlyChart {
        background-color: white;
        border-radius: 5px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🏀 WNBA Statistics Dashboard (2016-2024)")
st.markdown("""
Explore comprehensive WNBA player and team statistics from 2016 to 2024. 
This dashboard provides insights into player performance, team statistics, and historical trends.
""")

# Sample data loading (replace with actual data from your repository)
@st.cache_data
def load_data():
    # This is a placeholder. Replace with actual data from your files
    return pd.DataFrame({
        'Year': range(2016, 2025),
        'Player': ['Player ' + str(i) for i in range(1, 10)],
        'Team': ['Team A', 'Team B', 'Team C'] * 3,
        'PPG': [20 + i for i in range(1, 10)],
        'RPG': [5 + i for i in range(1, 10)],
        'APG': [3 + i for i in range(1, 10)],
        'FG%': [45 + i for i in range(1, 10)],
        'FT%': [80 + i for i in range(1, 10)],
        '3P%': [35 + i for i in range(1, 10)]
    })

# Load data
df = load_data()

# Sidebar filters
st.sidebar.header("📊 Filters")
selected_year = st.sidebar.slider("Select Year", 2016, 2024, 2024)
selected_team = st.sidebar.multiselect(
    "Select Team(s)",
    options=sorted(df['Team'].unique()),
    default=None
)

# Main content
tab1, tab2, tab3 = st.tabs(["📈 Player Stats", "🏆 Team Analysis", "🔍 Player Search"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            create_scoring_chart(df, selected_year),
            use_container_width=True
        )
    
    with col2:
        st.plotly_chart(
            create_efficiency_chart(df, selected_year),
            use_container_width=True
        )

with tab2:
    st.header("Team Statistics")
    team_stats = create_team_stats(df, selected_year)
    st.dataframe(
        team_stats,
        use_container_width=True,
        height=400
    )

with tab3:
    st.header("Player Search")
    search_col1, search_col2 = st.columns([2, 1])
    
    with search_col1:
        player_search = st.text_input("Search for a player:")
        if player_search:
            filtered_df = df[df['Player'].str.contains(player_search, case=False)]
            if not filtered_df.empty:
                st.dataframe(filtered_df)
                
                # Show player radar chart
                selected_player = st.selectbox(
                    "Select player for detailed view:",
                    filtered_df['Player'].unique()
                )
                player_data = filtered_df[filtered_df['Player'] == selected_player].iloc[0]
                st.plotly_chart(
                    create_player_radar_chart(player_data),
                    use_container_width=True
                )
            else:
                st.warning("No players found matching your search.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Data source: WNBA Statistics (2016-2024)</p>
</div>
""", unsafe_allow_html=True)