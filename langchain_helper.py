import pandas as pd
from langchain_ollama import OllamaLLM  # Import Ollama LLM
from langchain.chains import LLMChain  #Import LLM Chain
from langchain.prompts import PromptTemplate

# LangChain LLM setup
llm = OllamaLLM(model="llama3")  # Make sure it's running: ollama run llama3

def generate_menu_item(menu, preference):
        # Prompt Template
    template = """
        You are a helpful menu planner AI.

        Based on the past 2 weeks of menus and dietary preferences, generate a weekly meal plan (7 days).
        Each day should include Breakfast, Lunch and Dinner.
        Avoid repeating dishes from the past menus.
        Respect Veg/Non-Veg preferences.

        Past Menu:
        {menu_data}

        Preferences:
        {prefs_data}

        Format:
        Day | MealType | Dish | Type (Veg/Non-Veg)
        """

    print("Template ready!") #for debugging
    prompt = PromptTemplate(
        input_variables=["menu_data", "prefs_data"],
        template=template
    )

    # LangChain Chain
    chain = prompt | llm

    print("Running chain")  # for debugging
    # Run the chain
    result = chain.invoke({"menu_data": menu, "prefs_data": preference})
    print("Printing result")
    return result

if __name__ == "__main__":
    # Upload Excel

    # Load Excel
    xls = pd.ExcelFile(r"C:\Ronita-Work\AI-Learnings\Code\1.MenuItemGenerator\MenuItems_History.xlsx")
    menu_df = pd.read_excel(xls, "MenuHistory")
    prefs_df = pd.read_excel(xls, "Preferences")
    menu_text = menu_df.to_string(index=False)
    prefs_text = prefs_df.to_string(index=False)
    print(generate_menu_item(menu_text,prefs_text))