from io import StringIO
import streamlit as st
import pandas as pd
import langchain_helper_geminiapi
import base64

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
tab1, tab2 = st.tabs([
    "Generate Menu from Historical Data",
    "Generate Menu by Cuisine & Preference"
])



# ───────────────────────────── Tab 1
with tab1:
    if st.session_state.last_tab != "tab1":
        st.session_state.custom_menu = ""
        st.session_state.grocery_list = ""
        st.session_state.last_tab = "tab1"

    menu_option = st.radio("Choose an Option", [
        "Upload an excel with data",
        "Manually enter menu & preferences"
    ], horizontal=True)

    xls = None

    if menu_option == "Upload an excel with data":
        st.session_state.custom_menu =""
        with open("MenuItems_History.xlsx", "rb") as f:
            sample_data = f.read()
        b64 = base64.b64encode(sample_data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="MenuItems_History.xlsx">📥 Download Sample Excel Template</a>'
        st.markdown(href, unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
        if uploaded_file:
            xls = pd.ExcelFile(uploaded_file)
            # Add download link for sample Excel

    # elif menu_option == "Use a sample menu":
    #     try:
    #         xls = pd.ExcelFile("MenuItems_History.xlsx")
    #     except FileNotFoundError:
    #         st.error("❌ Sample file not found.")

    elif menu_option == "Manually enter menu & preferences":
        st.session_state.custom_menu = ""
        st.markdown("### ✍️ Enter Menu History")

        if "menu_input_df" not in st.session_state:
            st.session_state.menu_input_df = pd.DataFrame({
                "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                "Breakfast": ["" for _ in range(7)],
                "Lunch": ["" for _ in range(7)],
                "Dinner": ["" for _ in range(7)],
            })

        edited_menu_df = st.data_editor(
            st.session_state.menu_input_df,
            use_container_width=True,
            num_rows="dynamic",
            key="menu_editor"
        )

        st.markdown("### 👥 Enter Family Preferences")

        if "prefs_input_df" not in st.session_state:
            st.session_state.prefs_input_df = pd.DataFrame({
                "Name": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                "Preference": ["Vegetarian", "Non-Vegetarian","Vegetarian", "Non-Vegetarian","Vegetarian",
                               "Non-Vegetarian","Vegetarian"]
            })

        edited_prefs_df = st.data_editor(
            st.session_state.prefs_input_df,
            use_container_width=True,
            num_rows="dynamic",
            key="prefs_editor"
        )

        if st.button("🔮 Generate Menu from Manual Entry"):
            with st.spinner("Generating..."):
                menu_text = edited_menu_df.to_string(index=False)
                prefs_text = edited_prefs_df.to_string(index=False)
                result = langchain_helper_geminiapi.generate_menu_item(menu_text, prefs_text).strip()
                df = format_llm_response(result)
                st.session_state.custom_menu = result
                st.session_state.grocery_list = ""

    if xls:
        try:
            menu_df = pd.read_excel(xls, "MenuHistory")
            prefs_df = pd.read_excel(xls, "Preferences")

            with st.expander("📅 View Menu History"):
                st.dataframe(menu_df)

            with st.expander("👥 View Preferences"):
                st.dataframe(prefs_df)

            if st.button("🔮 Generate Menu"):
                with st.spinner("Generating menu..."):
                    menu_text = menu_df.to_string(index=False)
                    prefs_text = prefs_df.to_string(index=False)
                    result = langchain_helper_geminiapi.generate_menu_item(menu_text, prefs_text).strip()
                    df = format_llm_response(result)
                    st.session_state.custom_menu = result
                    st.session_state.grocery_list = ""

        except ValueError as e:
            st.error(f"❌ Sheet not found or unreadable: {e}")

    if st.session_state.custom_menu:
        with st.expander("🍲 Generated Menu", expanded=False):
            df = format_llm_response(st.session_state.custom_menu)
            st.dataframe(df)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("💾 Download Menu as CSV", data=csv, file_name="menu.csv", mime="text/csv", key="tab1_download_menu_csv")

# ───────────────────────────── Tab 2

# 🔸 Tab 2: Generate Based on Cuisine + Prefs
with tab2:
    # st.header("🍽️ Generate menu by cuisine & preference")

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
    with col2:
        preference = st.radio(
            "Choose preference",
            ["Vegetarian", "Non-Vegetarian", "Both"]
        )

    # Generate Menu / Grocery Buttons

    if st.button("🔮 Generate Custom Menu"):
        with st.spinner("Generating..."):
            if preference == "Both":
                preference = "Vegetarian & Non-Vegetarian"
            result = langchain_helper_geminiapi.generate_custom_menu(cuisine, preference)
            st.session_state.custom_menu = result.strip()
            st.session_state.grocery_list = ""  # clear previous grocery list
            st.session_state.custom_menu_ready_tab2 = True

        # --- Display generated menu
        if st.session_state.custom_menu:
            with st.expander("🍲 Generated Menu", expanded=False):
                df = format_llm_response(st.session_state.custom_menu)
                st.dataframe(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("💾 Download Menu as CSV", data=csv, file_name="menu.csv", mime="text/csv",
                                   key="download_custom_menu_csv")

    # # display grocery list
    # if st.button("🛒 Generate Grocery List"):
    #     print("Inside Grocery Button Clicked")
    #     with st.spinner("Working..."):
    #         grocery_list = langchain_helper_geminiapi.generate_grocery_list(st.session_state.custom_menu)
    #         print("Inside Grocery Button Clicked {grocery_list}")
    #         st.session_state.grocery_list = grocery_list.strip()
    #
    #
    #
    # # --- Display grocery list if available
    # if st.session_state.grocery_list:
    #     with st.expander("🧾 Generated Grocery List", expanded=False):
    #         st.text_area("Grocery List", st.session_state.grocery_list, height=300)
    #         txt = st.session_state.grocery_list.encode('utf-8')
    #         st.download_button("💾 Download Grocery List as TXT", data=txt, file_name="grocery_list.txt",
    #                            mime="text/plain", key="download_grocery_csv")