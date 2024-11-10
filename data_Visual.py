import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import plotly.express as px
import plotly.graph_objects as go


def app():
    # Load data
    df = pd.read_csv("eco_friendly_product5.csv")
    st.set_option("deprecation.showPyplotGlobalUse", False)

    # Title and subtitles for the app
    st.markdown("<h1 style='text-align: center; color: green;'>Sustainable Products Customization Web App</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #1E88E5;'>Eco-Friendly Product Data Visualization</h2>", unsafe_allow_html=True)
    
    # Sidebar title
    st.sidebar.title("Product Visualization")

    # Display raw data if selected
    if st.sidebar.button('Display Complete Product Data'):
        st.subheader("Product Data Set")
        st.dataframe(df)
        st.write("Number of Rows:", df.shape[0])
        st.write("Number of Columns:", df.shape[1])

    # Display summary statistics if selected
    # if st.sidebar.button("Describe"):
    #     st.write(df.describe())

    # Select column to display from the sidebar
    selected_columns = st.sidebar.multiselect("Select columns to display", df.columns)

        # Display selected columns in the main area
    if st.sidebar.button("Show"):
        if selected_columns:
            st.write("Displaying selected columns:")
            st.dataframe(df[selected_columns])
        else:
            st.write("Please select at least one column to display.")

    # Search functionality in the sidebar
    st.sidebar.subheader("Search Products")
    search_query = st.sidebar.text_input("Enter a keyword to search")

    # Function to search for a keyword within the dataset
    def search_in_dataframe(df, keyword):
        keyword = keyword.lower()
        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
        return filtered_df

    # Display search results if a search query is entered
    if search_query:
        st.write(f"Search results for '{search_query}':")
        search_results = search_in_dataframe(df, search_query)
        
        if not search_results.empty:
            st.dataframe(search_results)
        else:
            st.write(f"No results found for '{search_query}'.")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Comparison section title
    st.title("Sustainable Product Comparison")

    # Sidebar for selecting products to compare
    selected_products = st.multiselect("Select products to compare:", df["Product_Name"].tolist())
    filtered_data = df[df["Product_Name"].isin(selected_products)]

    # Radar Chart for Sustainability Comparison
    st.subheader("Sustainability Metrics - Radar Chart")
    categories = ["Carbon Footprint", "Water Usage", "Manufacturing Impact", "Price Range"]

    # Prepare data for radar chart
    if not filtered_data.empty:
        fig_radar = go.Figure()
        for i, row in filtered_data.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[row["Carbon_Footprint_kgCO2e"], row["Water_Usage_Liters"], row["Manufacturing_Impact"], row["Price_Range_USD"]],
                theta=categories,
                fill='toself',
                name=row["Product_Name"]
            ))

        # Set range and layout for the radar chart
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]  # Customize this range based on your data
                )),
            showlegend=True
        )
        st.plotly_chart(fig_radar)
    else:
        st.write("Please select at least one product to display the radar chart.")

    categories = ["Carbon_Footprint_kgCO2e", "Water_Usage_Liters", "Manufacturing_Impact", "Price_Range_USD"]

    # Check if columns exist
    if all(col in df.columns for col in categories):
        # Melt data and create bar graph
        df_melted = pd.melt(filtered_data, id_vars=["Product_Name"], value_vars=categories, var_name="Metric", value_name="Value")
        fig_bar = px.bar(df_melted, x="Metric", y="Value", color="Product_Name", barmode="group")
        st.plotly_chart(fig_bar)
    else:
        st.write("One or more columns specified in 'categories' are missing from the DataFrame.")


    # Additional information and guidance
    st.write("Use the controls on the left to select products and visualize their sustainability metrics.")
    st.write("Explore the sustainability data for informed eco-friendly choices!")

