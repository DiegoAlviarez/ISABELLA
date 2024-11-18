import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="WNBA Statistics Dashboard",
    page_icon="🏀",
    layout="wide"
)

# Title and description
st.title("WNBA Player Statistics (2016-2024)")
st.markdown("""
This dashboard provides comprehensive statistics for WNBA players and teams 
from 2016 to 2024. Explore player performance, team statistics, and historical trends.
""")

# Sidebar for filtering
st.sidebar.header("Filters")
selected_year = st.sidebar.slider("Select Year", 2016, 2024, 2024)

# Sample data structure (replace with actual data from your GitHub repository)
@st.cache_data
def load_data():
    # This is a placeholder. Replace with actual data loading from your files
    return pd.DataFrame({
        'Year': [2024, 2024, 2024],
        'Player': ['A\'ja Wilson', 'Breanna Stewart', 'Sabrina Ionescu'],
        'Team': ['Las Vegas Aces', 'New York Liberty', 'New York Liberty'],
        'PPG': [22.8, 23.0, 17.5],
        'RPG': [9.5, 9.3, 5.6],
        'APG': [2.3, 3.8, 5.4]
    })

# Load data
df = load_data()

# Main dashboard sections
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Scorers")
    fig_scorers = px.bar(
        df.nlargest(5, 'PPG'),
        x='Player',
        y='PPG',
        title='Top 5 Scorers',
        color='Team'
    )
    st.plotly_chart(fig_scorers, use_container_width=True)

with col2:
    st.subheader("Top Rebounders")
    fig_rebounds = px.bar(
        df.nlargest(5, 'RPG'),
        x='Player',
        y='RPG',
        title='Top 5 Rebounders',
        color='Team'
    )
    st.plotly_chart(fig_rebounds, use_container_width=True)

# Team Statistics
st.header("Team Statistics")
team_stats = df.groupby('Team').mean().round(2)
st.dataframe(team_stats)

# Player Search
st.header("Player Search")
player_search = st.text_input("Search for a player:")
if player_search:
    filtered_df = df[df['Player'].str.contains(player_search, case=False)]
    st.dataframe(filtered_df)

# Add footer
st.markdown("---")
st.markdown("Data source: WNBA Statistics (2016-2024)")