import streamlit as st
from PIL import Image


def app():
    st.markdown(
        """
        <div style='text-align: center; padding: 20px 0;'>
            <h2 style='color: #4CAF50;'>Sustainable Products Customization Web App</h2>
            <h4 style='color: #1E88E5;'>Eco-Friendly Product Recommendation Engine</h4>
        </div>
        """, unsafe_allow_html=True
    )

    # Sidebar options
    st.sidebar.header("Customize Your Product Search")
    product_type = st.sidebar.selectbox("Select Product Type", ["All", "Reusable Bags", "Biodegradable Containers", "Eco-Friendly Utensils"])
    price_range = st.sidebar.slider("Select Price Range", 0, 100, (10, 50))

    # Recommended products section
    st.subheader("Recommended Products")
    st.markdown(
        """
        <div style='background-color: #F1F8E9; padding: 15px; border-radius: 10px;'>
            <h4 style='color: #388E3C;'>1. Eco-friendly Bag</h4>
            <p>Made from 100% recycled materials. Price: $20</p>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style='background-color: #F1F8E9; padding: 15px; border-radius: 10px; margin-top: 10px;'>
            <h4 style='color: #388E3C;'>2. Biodegradable Utensil Set</h4>
            <p>Perfect for picnics and gatherings. Price: $15</p>
        </div>
        """, unsafe_allow_html=True
    )