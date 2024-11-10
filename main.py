import streamlit as st
import home
import data_Visual
import fast
import product_refine

st.set_page_config(
    page_title="Eco-Friendly Product Recommendation",
    page_icon="🌍",
    layout="wide",  # Optional: "centered" or "wide"
    initial_sidebar_state="expanded"  # Optional: "expanded" or "collapsed"
)
# Sidebar Navigation
pages_dict = {
    "Home": home,
    "Data Visualization": data_Visual,
    "Search/Filter Panel": product_refine,
    "Sustainable Products Customization (Fast)": fast,
}

st.sidebar.title("🌿 Navigation")
user_choice = st.sidebar.radio("Go to", tuple(pages_dict.keys()))

# Load selected page
if user_choice == "Home":
    home.app()
else:
    selected_page = pages_dict[user_choice]
    selected_page.app()
