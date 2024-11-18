import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def create_scoring_chart(df, year):
    filtered_df = df[df['Year'] == year].nlargest(10, 'PPG')
    fig = px.bar(
        filtered_df,
        x='Player',
        y='PPG',
        title=f'Top 10 Scorers ({year})',
        color='Team',
        text='PPG'
    )
    fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    return fig

def create_efficiency_chart(df, year):
    filtered_df = df[df['Year'] == year].nlargest(10, 'FG%')
    fig = px.bar(
        filtered_df,
        x='Player',
        y='FG%',
        title=f'Field Goal Percentage Leaders ({year})',
        color='Team',
        text='FG%'
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    return fig

def create_team_stats(df, year):
    team_stats = df[df['Year'] == year].groupby('Team').agg({
        'PPG': 'mean',
        'RPG': 'mean',
        'APG': 'mean',
        'FG%': 'mean'
    }).round(2)
    return team_stats

def create_player_radar_chart(player_data):
    categories = ['PPG', 'RPG', 'APG', 'FG%', 'FT%', '3P%']
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=[player_data[cat] for cat in categories],
        theta=categories,
        fill='toself',
        name=player_data['Player']
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max([player_data[cat] for cat in categories]) * 1.2]
            )),
        showlegend=True,
        title=f"Player Profile: {player_data['Player']}"
    )
    return fig