import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from PIL import Image

def load_image(url):
    try:
        response = requests.get(url, timeout=10)  # Added timeout
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        return image
    except requests.exceptions.RequestException as e:
        st.warning(f"Could not load image from URL: {url}")
        return None
    except Exception as e:
        st.warning("Image loading failed")
        return None

@st.cache_data(show_spinner=True)
def load_data(url):
    try:
        response = requests.get(url, timeout=10)  # Added timeout
        response.raise_for_status()
        df = pd.read_excel(BytesIO(response.content))
        
        # Clean the dataframe
        df = df.replace(r'^\s*$', pd.NA, regex=True)
        
        # Rename columns if needed
        column_mapping = {
            'Equipo': 'Team',
            'Posición': 'Position',
            'Puntos': 'PTS',
            'Asistencias': 'AST',
            'Rebotes': 'REB',
            'Porcentaje de tiros de campo': 'FG%'
        }
        df = df.rename(columns=column_mapping)
        
        # Convert numeric columns
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
        # Fill NaN values appropriately
        string_columns = df.select_dtypes(include=['object']).columns
        for col in string_columns:
            df[col] = df[col].fillna('N/A')
            
        # Ensure required columns exist
        required_columns = ['Nombre', 'PTS', 'AST', 'REB', 'FG%']
        for col in required_columns:
            if col not in df.columns:
                df[col] = 'N/A'
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None
