def get_mode_based_menu_prompt(mood,dietary):
    prompt = f"""
        You're a helpful meal planner AI. Create a full-day menu (breakfast, lunch, dinner) for someone who is feeling "{mood}".
        Consider their dietary preference: {dietary}.
        Avoid repeating ingredients across meals. 
        Don't include preamble. 
        
        Output Format:
        Day | MealType | Dish | Type (Veg/Non-Veg) 
        """
    return prompt


def get_fridge_to_food_menu_prompt(ingredients, dietary):
    prompt = f"""
        
        Suggest creative meals using only the following ingredients: {ingredients}.
        Make 2-3 suggestions for breakfast, lunch, or dinner. Dietary preference: {dietary}.
        Don't include preamble. 

        Output Format:
        MealType | Dish | Description | Veg/Non-Veg.
        """
    return prompt


def get_weekly_food_insights_prompt(user_history_input):
    prompt = f"""
        
        Analyze the following weekly meal log and provide insights about eating habits, nutrition balance, and suggestions to improve.
        Data:
        {user_history_input}

        Your response should be bullet points summarizing the user’s diet patterns and smart tips.
        """
    return prompt