from calendar import day_abbr


def get_historical_based_menu_prompt(menu, preference):
    prompt =f"""
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
    Day | MealType | Dish | Type (Veg/Non-Veg) | Recipe 
    """
    return prompt


def get_cuisine_preference_based_menu_prompt(cuisine, preference, meal):
    prompt = f"""
        You are a helpful AI chef assistant.

        Generate a {preference.lower()} {meal} for {cuisine} cuisine. Don't include 
        preamble. 
        It should include {meal} as per the selection.
        Each dish should be realistic, reflect the cuisine, and include an actual **online recipe link** (if known). Use links from reputable sources.
        Respect preferences and do not include red meat.

        Format:
        MealType | Dish | Type (Veg/Non-Veg) | Recipe
        
        """
    return prompt

def get_mode_based_menu_prompt(mood,dietary, meal):
    prompt = f"""
        You're a helpful meal planner AI. Create a {meal} for someone who is feeling "{mood}".
        Consider their dietary preference: {dietary}.
        Avoid repeating ingredients across meals. 
        Don't include preamble. 
        
        Output Format:
        MealType | Dish | Type (Veg/Non-Veg) | Recipe 
        """
    return prompt


def get_fridge_to_food_menu_prompt(ingredients, dietary):
    prompt = f"""
        
        Suggest creative meals using only the following ingredients: {ingredients} only. 
        Don't include any other ingredients that are not provided. 
        Make 2-3 suggestions for breakfast, lunch, or dinner. Dietary preference: {dietary}.
        Don't include preamble. 

        Output Format:
        MealType | Dish | Description | Veg/Non-Veg | Recipe 
        
        """
    return prompt


def get_weekly_food_insights_prompt(user_history_input):
    prompt = f"""
        
        Analyze the following weekly meal log and provide insights about eating habits, nutrition balance, and suggestions to improve.
        Data:
        {user_history_input}

        Your response should be bullet points summarizing the user’s diet patterns and smart tips.
        Your response should be within 2-3 sentences. 
        """
    return prompt


def get_list_of_cuisine_prompt():
    prompt = f"""
        You're a helpful meal planner AI. Provide a list of cuisine available in the world.
        Avoid repeating cuisines. 
        Don't include preamble. 
        
        Output Format:
        Cuisine
        """
    return prompt