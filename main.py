from io import StringIO
import streamlit as st
import pandas as pd
from sqlalchemy.util.preloaded import import_prefix

import langchain_helper_geminiapi
import base64
import image_generator_helper

st.set_page_config(page_title="AI Menu Generator", layout="centered")
st.title("🍽️ Food Chart")

# Session state variables
for key in ["custom_menu", "grocery_list", "last_tab"]:
    if key not in st.session_state:
        st.session_state[key] = ""

selected_menu = None
df = None
# Helper function to clean and convert LLM response to DataFrame

def format_llm_response(llm_response):
    cleaned_lines = [
        line for line in llm_response.split('\n')
        if not set(line.strip()) <= {'-', '|'}
    ]
    cleaned_result = '\n'.join(cleaned_lines)
    # 🔍 DEBUGGING OUTPUT
    #st.text_area("🔍 Cleaned Result for Debugging", cleaned_result, height=300)
    try:
        df = pd.read_csv(StringIO(cleaned_result), sep='|')
        df.columns = df.columns.str.strip()
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    except Exception as e:
        st.error(f"❌ Error parsing LLM response to table: {e}")
        return pd.DataFrame()

# ─────────────────────────────────────────────────────────────
#tab1, "Past Meals to Plan",
tab2, tab3, tab4, tab5 = st.tabs([
    "Menu by Taste & Type",
    "Mood-Based Menu",
    "Fridge to Food Menu",
    "Weekly Food Insight"
])


# ───────────────────────────── Tab 1
#with tab1:
    # st.subheader("📅 Past Meals to Plan")
    # if st.session_state.last_tab != "tab1":
    #     st.session_state.custom_menu = ""
    #     st.session_state.grocery_list = ""
    #     st.session_state.last_tab = "tab1"
    #
    # menu_option = st.radio("🧭 How do you want to recall your menu?", [
    #     "Import meal history (Excel)",
    #     "Type in your meals manually"
    # ], horizontal=True)
    #
    # xls = None
    #
    # if menu_option == "Import meal history (Excel)":
    #     st.session_state.custom_menu =""
    #     with open("MenuItems_History.xlsx", "rb") as f:
    #         sample_data = f.read()
    #     b64 = base64.b64encode(sample_data).decode()
    #     href = f'<a href="data:application/octet-stream;base64,{b64}" download="MenuItems_History.xlsx">📥 Download Sample Excel Template</a>'
    #     st.markdown(href, unsafe_allow_html=True)
    #     uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
    #     if uploaded_file:
    #         xls = pd.ExcelFile(uploaded_file)
    #         # Add download link for sample Excel
    #
    # # elif menu_option == "Use a sample menu":
    # #     try:
    # #         xls = pd.ExcelFile("MenuItems_History.xlsx")
    # #     except FileNotFoundError:
    # #         st.error("❌ Sample file not found.")
    #
    # elif menu_option == "Type in your meals manually":
    #     st.session_state.custom_menu = ""
    #     st.markdown("### ✍️ Enter Menu History")
    #
    #     if "menu_input_df" not in st.session_state:
    #         st.session_state.menu_input_df = pd.DataFrame({
    #             "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    #             "Breakfast": ["" for _ in range(7)],
    #             "Lunch": ["" for _ in range(7)],
    #             "Dinner": ["" for _ in range(7)],
    #         })
    #
    #     edited_menu_df = st.data_editor(
    #         st.session_state.menu_input_df,
    #         use_container_width=True,
    #         num_rows="dynamic",
    #         key="menu_editor"
    #     )
    #
    #     st.markdown("### 👥 Enter Preferences")
    #
    #     if "prefs_input_df" not in st.session_state:
    #         st.session_state.prefs_input_df = pd.DataFrame({
    #             "Name": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    #             "Preference": ["Vegetarian", "Non-Vegetarian","Vegetarian", "Non-Vegetarian","Vegetarian",
    #                            "Non-Vegetarian","Vegetarian"]
    #         })
    #
    #     edited_prefs_df = st.data_editor(
    #         st.session_state.prefs_input_df,
    #         use_container_width=True,
    #         num_rows="dynamic",
    #         key="prefs_editor"
    #     )
    #
    #     if st.button("🔮 Generate Menu from Manual Entry"):
    #         with st.spinner("Generating..."):
    #             menu_text = edited_menu_df.to_string(index=False)
    #             prefs_text = edited_prefs_df.to_string(index=False)
    #             result = langchain_helper_geminiapi.generate_menu_item(menu_text, prefs_text).strip()
    #             df = format_llm_response(result)
    #             st.session_state.custom_menu = result
    #             st.session_state.grocery_list = ""
    #
    # if xls:
    #     try:
    #         menu_df = pd.read_excel(xls, "MenuHistory")
    #         prefs_df = pd.read_excel(xls, "Preferences")
    #
    #         with st.expander("📅 View Menu History"):
    #             st.dataframe(menu_df)
    #
    #         with st.expander("👥 View Preferences"):
    #             st.dataframe(prefs_df)
    #
    #         if st.button("🔮 Generate Meal Plan"):
    #             with st.spinner("Generating menu..."):
    #                 menu_text = menu_df.to_string(index=False)
    #                 prefs_text = prefs_df.to_string(index=False)
    #                 result = langchain_helper_geminiapi.generate_menu_item(menu_text, prefs_text).strip()
    #                 df = format_llm_response(result)
    #                 st.session_state.custom_menu = result
    #                 st.session_state.grocery_list = ""
    #
    #     except ValueError as e:
    #         st.error(f"❌ Sheet not found or unreadable: {e}")
    #
    # if st.session_state.custom_menu:
    #     with st.expander("🍲 Generated Menu", expanded=False):
    #         df = format_llm_response(st.session_state.custom_menu)
    #         st.dataframe(df)
    #         csv = df.to_csv(index=False).encode("utf-8")
    #         st.download_button("💾 Download Menu as CSV", data=csv, file_name="menu.csv", mime="text/csv", key="tab1_download_menu_csv")

# ───────────────────────────── Tab 2

# 🔸 Tab 2: Generate Based on Cuisine + Prefs
with tab2:
    st.header("🍛 Meals by Taste & Type")

    if "custom_menu_ready_tab2" not in st.session_state:
        st.session_state.custom_menu_ready_tab2 = False

    # Reset only when switching tabs
    if st.session_state.last_tab != "tab2":
        st.session_state.custom_menu = ""
        st.session_state.grocery_list = ""
        st.session_state.custom_menu_ready_tab2 = False
        st.session_state.last_tab = "tab2"

    # Input section
    col1, col2 = st.columns([2, 1])
    with col1:
        cuisine = st.radio(
            "Choose a cuisine",
            ["Indian", "Italian", "Chinese", "Continental"],
            horizontal=True
        )
        meal = st.radio(
            "Choose meal type",
            ["Breakfast", "Lunch", "Dinner"],
            horizontal=True
        )
    with col2:
        preference = st.radio(
            "Choose preference",
            ["Vegetarian", "Non-Vegetarian", "Both"]
        )

    # Generate Menu / Grocery Buttons
    if st.button("🍳 Suggest Preferred Meals"):
        with st.spinner("Generating..."):
            if preference == "Both":
                preference = "Vegetarian & Non-Vegetarian"
            result = langchain_helper_geminiapi.generate_custom_menu(cuisine, preference, meal)
            st.session_state.custom_menu = result.strip()
            st.session_state.grocery_list = ""  # clear previous grocery list
            st.session_state.custom_menu_ready_tab2 = True

            # --- Display generated menu
            if st.session_state.custom_menu:
                with st.expander("🍲 Generated Meals", expanded=True):
                    df = format_llm_response(st.session_state.custom_menu)
                    for idx, row in df.iterrows():
                        meal = row.get("Meal") or row.get("Dish") or row.iloc[0]
                        st.subheader(f"🍽️ {meal}")
                        image_url = image_generator_helper.fetch_meal_image(meal)
                        if image_url:
                            # Display image with fixed width and optional styling
                            st.markdown(
                                f"""
                                            <div style="text-align: center; margin-bottom: 10px;">
                                                <img src="{image_url}" width="250" style="border-radius: 10px; border: 1px solid #ccc;" />
                                            </div>
                                            """,
                                unsafe_allow_html=True
                            )
                        else:
                            st.info("No image found for this meal.")

                        # Display recipe link if available
                        recipe_val = row.get("Recipe") or ""
                        if recipe_val.startswith("[http://") or recipe_val.startswith("[https://"):
                            st.markdown(f"[📖 View Recipe]({recipe_val})")
                        elif len(recipe_val.strip()) > 0:
                            st.markdown("📖 *Recipe available in details below*")
                        else:
                            st.markdown("❌ *No recipe link provided*")

                        # Show the rest of the row excluding the full recipe text
                        display_row = row.drop(labels=["RecipeLink"]) if "RecipeLink" in row else row
                        st.write(display_row.to_frame().T)

                    # st.dataframe(df)
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button("💾 Download Menu as CSV", data=csv, file_name="menu.csv", mime="text/csv",
                                       key="download_custom_menu_csv")

# ───────────────────────────── Tab 3:  Mood-Based Menu Generator
with tab3:
    st.subheader("🌤️ Mood-Based Meals")
    if not st.session_state.get("is_pro_user", True):
        st.warning("🔒 This feature is available for Pro users only.")
        st.stop()

    mood = st.text_input("How are you feeling today?", placeholder="e.g., tired, happy, bloated, energetic")
    dietary_preference = st.selectbox("Choose dietary preference",
                                      ["Vegetarian", "Non-Vegetarian", "Vegan", "Keto", "Any"])
    meal = st.selectbox("Choose meal type",
                                      ["Breakfast", "Lunch", "Dinner"])

    if st.button("🍳 Suggest Mood-Based Meals"):
        with st.spinner("Thinking like a foodie..."):
            result = langchain_helper_geminiapi.generate_mode_based_menu(mood, dietary_preference, meal).strip()
            with st.expander("🍲 Generated Meals", expanded=True):
                df = format_llm_response(result)
                st.dataframe(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("💾 Download Menu as CSV", data=csv, file_name="menu.csv", mime="text/csv",
                                   key="download_mode_based_menu_csv")

# ───────────────────────────── Tab 4: Fridge to Food
with tab4:
    st.subheader("📷 Fridge-to-Food Meals")

    if not st.session_state.get("is_pro_user", True):
        st.warning("🔒 This feature is available for Pro users only.")
        st.stop()

    ingredients = st.text_area("What ingredients do you have?", placeholder="e.g., 2 eggs, spinach, onion, tomato")
    dietary_preference = st.selectbox("Choose dietary preference", ["Vegetarian", "Non-Vegetarian", "Vegan", "Any"])
    meal = st.selectbox("Choose a meal type",  ["Breakfast", "Lunch", "Dinner"])
    if st.button("🍳 Suggest Meals"):
        with st.spinner("Cooking up ideas..."):
            result = langchain_helper_geminiapi.generate_fridge_to_food_menu(ingredients, dietary_preference, meal).strip()
            with st.expander("🍲 Generated Meals", expanded=True):
                df = format_llm_response(result)
                st.dataframe(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("💾 Download Menu as CSV", data=csv, file_name="menu.csv", mime="text/csv",
                                   key="download_fridge_to_food_based_menu_csv")

# ───────────────────────────── Tab 5: Weekly Food Insight
with tab5:
    st.subheader("🧠 Weekly Food Insights")

    if not st.session_state.get("is_pro_user", True):
        st.warning("🔒 This feature is available for Pro users only.")
        st.stop()

    user_history_input = st.text_area("Paste your weekly menu (raw or table format)")

    if st.button("🔍 Analyze"):
        with st.spinner("Analyzing patterns..."):
            result = langchain_helper_geminiapi.generate_weekly_food_insights(user_history_input).strip()
            st.markdown(result)