import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from PIL import Image

def load_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        return image
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading image: {e}")
        return None
    except Image.UnidentifiedImageError:
        st.error("Could not identify image file.")
        return None

@st.cache_data
def load_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return pd.read_excel(BytesIO(response.content))
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None