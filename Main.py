from io import StringIO
import streamlit as st
import pandas as pd


import langchain_helper_geminiapi

# This menu generator AI tool uses the following

st.title("🍽️ AI Menu Generator")

# Upload Excel
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

# Initialize xls as None
xls = None

if uploaded_file is not None:
    # Load Excel
    xls = pd.ExcelFile(uploaded_file)
elif st.checkbox("Use sample menu"):
    # 👇 Replace with your actual file path
    fallback_path = r"C:\Ronita-Work\AI-Learnings\Code\1.MenuItemGenerator\MenuItems_History.xlsx"
    try:
        xls = pd.ExcelFile(fallback_path)
        #st.success("✅ Loaded sample menu successfully.")
    except FileNotFoundError:
        st.error("❌ Sample file not found.")
else:
    st.info("📂 Please upload a file or check the sample menu.")
if xls:
    try:
        # Only proceed if xls is loaded
        menu_df = pd.read_excel(xls, "MenuHistory")
        prefs_df = pd.read_excel(xls, "Preferences")

        # Show Menu History inside an expander
        with st.expander("📅 View Menu History"):
            st.dataframe(menu_df)

        # Show Preferences inside an expander
        with st.expander("👥 View Preferences"):
            st.dataframe(prefs_df)


        if st.button("🔮 Generate Menu"):
            # Combine data into prompt text
            menu_text = menu_df.to_string(index=False)
            prefs_text = prefs_df.to_string(index=False)

            # Run the chain
            with st.spinner("Generating menu..."):
                result = langchain_helper_geminiapi.generate_menu_item(menu_text, prefs_text).strip()
                # st.text_area("📝 Raw Gemini Output", result, height=200)

                # Remove the markdown separator line
                cleaned_lines = [
                    line for line in result.split('\n')
                    if not set(line.strip()) <= {'-', '|'}  # filters out lines like "---|---|---|---"
                ]

                # Join the cleaned lines back into a string
                cleaned_result = '\n'.join(cleaned_lines)

                # Convert text to DataFrame
                df = pd.read_csv(StringIO(cleaned_result), sep='|')
                df.columns = df.columns.str.strip()
                df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

            # Output
            st.success("✅ Menu Generated!")
            st.subheader("Generated Menu")
            st.dataframe(df)
    except ValueError as e:
        st.error(f"❌ Sheet not found or unreadable: {e}")

