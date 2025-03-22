import google.generativeai as genai
import pandas as pd
import os

# Load environment variables


# Set your API Key
genai.configure(api_key="AIzaSyCafzEwpRz4NhPcUaGFIRIfLGbEuOHv5Qw")  # Or load from env

def generate_menu_item(menu, preference):
    prompt = f"""
    You are a helpful AI chef assistant.

    Based on the past 2 weeks of menus and dietary preferences, generate a weekly meal plan (7 days).
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

if __name__ == "__main__":
    # Upload Excel

    # Load Excel
    xls = pd.ExcelFile(r"C:\Ronita-Work\AI-Learnings\Code\1.MenuItemGenerator\MenuItems_History.xlsx")
    menu_df = pd.read_excel(xls, "MenuHistory")
    prefs_df = pd.read_excel(xls, "Preferences")
    menu_text = menu_df.to_string(index=False)
    prefs_text = prefs_df.to_string(index=False)
    print(generate_menu_item(menu_text,prefs_text))