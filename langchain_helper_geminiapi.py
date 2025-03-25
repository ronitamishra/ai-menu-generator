import google.generativeai as genai
import pandas as pd
import os
import prompt_template

# Load environment variables

# Set your API Key
genai.configure(api_key="AIzaSyCafzEwpRz4NhPcUaGFIRIfLGbEuOHv5Qw")  # Or load from env

def generate_menu_item(menu, preference):
    prompt = f"""
    You are a helpful AI chef assistant.

    Based on the past 2 weeks of menus and dietary preferences, generate a weekly meal plan (7 days). Don't include 
    preamble. 
    Each day should include Breakfast, Lunch, and Dinner.
    Avoid repeating dishes from the past menus.
    Respect Veg/Non-Veg preferences and do not include red meat.

    Past Menu:
    {menu}

    Preferences:
    {preference}
    
    Format:
    Day | MealType | Dish | Type (Veg/Non-Veg)
    """

    model = genai.GenerativeModel("gemini-1.5-flash")  # or gemini-1.5-pro
    response = model.generate_content(prompt)

    return response.text

def generate_custom_menu(cuisine, preference):
    prompt = f"""
    You are a helpful AI chef assistant.
    
    Generate a weekly {preference.lower()} menu for {cuisine} cuisine. Don't include 
    preamble. 
    It should include Breakfast, Lunch, and Dinner.
    Respect preferences and do not include red meat.
      
    Format:
    Day | MealType | Dish | Type (Veg/Non-Veg) 
    """
    print(prompt)
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

def generate_mode_based_menu(mood, dietary_preference):
    prompt = prompt_template.get_mode_based_menu_prompt(mood,dietary_preference)
    return run_gemini_api(prompt)

def generate_fridge_to_food_menu(ingredients, dietary_preference):
    prompt = prompt_template.get_mode_based_menu_prompt(ingredients,dietary_preference)
    return run_gemini_api(prompt)

def generate_weekly_food_insights(user_history_input):
    prompt = prompt_template.get_weekly_food_insights_prompt(user_history_input)
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
