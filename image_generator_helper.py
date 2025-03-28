import requests
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv("secret.env")

# Set your API Key
api_key = os.getenv("PEXELS_API_KEY")

@st.cache_data(show_spinner=False)
def fetch_meal_image(meal_name, cuisine):
    headers = {
        "Authorization": api_key
    }
    params = {
        "query": str(meal_name) + cuisine + "food",
        "per_page": 1
    }
    response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["photos"]:
            return data["photos"][0]["src"]["medium"]
    return None