import google.generativeai as genai
import pandas as pd
import os

from click import prompt

import prompt_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv("secret.env")

# Set your API Key
api_key = os.getenv("GOOGLE_API_KEY")
# ✅ Sanity check (just for debugging)
#print("API Key Loaded:", "✅" if api_key else "❌ NOT FOUND")
genai.configure(api_key=api_key)  # Or load from env

def generate_menu_item(menu, preference):
    prompt = prompt_template.get_historical_based_menu_prompt(menu, preference)
    return run_gemini_api(prompt)


def generate_custom_menu(cuisine, preference, meal):
    prompt = prompt_template.get_cuisine_preference_based_menu_prompt(cuisine, preference, meal)
    return run_gemini_api(prompt)

def run_gemini_api(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")  # or gemini-1.5-pro
    response = model.generate_content(prompt)
    return response.text

def generate_grocery_list(selected_menu):
    prompt = f"""Given this daily menu, generate a detailed grocery list grouped by category:
    MENU:
    {selected_menu}
    """
    return run_gemini_api(prompt)

def generate_mode_based_menu(mood, dietary_preference, meal):
    prompt = prompt_template.get_mode_based_menu_prompt(mood,dietary_preference, meal)
    return run_gemini_api(prompt)

def generate_fridge_to_food_menu(ingredients, dietary_preference, meal):
    prompt = prompt_template.get_mode_based_menu_prompt(ingredients,dietary_preference, meal)
    return run_gemini_api(prompt)

def generate_weekly_food_insights(user_history_input):
    prompt = prompt_template.get_weekly_food_insights_prompt(user_history_input)
    return run_gemini_api(prompt)

def generate_list_of_cuisine():
    prompt = prompt_template.get_list_of_cuisine_prompt()
    return run_gemini_api(prompt)

if __name__ == "__main__":
    # Upload Excel

    # Load Excel
    #xls = pd.ExcelFile(r"C:\Ronita-Work\AI-Learnings\Code\1.MenuItemGenerator\MenuItems_History.xlsx")
    #menu_df = pd.read_excel(xls, "MenuHistory")
    #prefs_df = pd.read_excel(xls, "Preferences")
    #menu_text = menu_df.to_string(index=False)
    #prefs_text = prefs_df.to_string(index=False)
    #print(generate_menu_item(menu_text,prefs_text))

    print(generate_grocery_list(generate_custom_menu("Chinese","Vegetarian")))
