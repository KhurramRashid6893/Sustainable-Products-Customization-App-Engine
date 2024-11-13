import streamlit as st
import pandas as pd

def app():

    # Load data
    @st.cache_data
    def load_data():
        df = pd.read_csv("eco_friendly_product_recommendation_data_consistent_names.csv")  # Replace with your actual file path
        return df

    # Load data
    df = load_data()

    # Sidebar - Search and Filter Panel
    st.sidebar.title("Search & Filter Products")

    # Collapsible filter section
    with st.sidebar.expander("Search and Filter Options", expanded=False):
        
        # Filter by Brand
        st.subheader("Filter by Brand")
        brands = df['Brand'].unique()
        selected_brands = st.multiselect("Select brands:", options=brands)
        
        # Filter by Price Range
        st.subheader("Filter by Price Range")
        min_price = st.slider("Minimum Price", int(df['Price_Range_USD'].min()), int(df['Price_Range_USD'].max()), int(df['Price_Range_USD'].min()))
        max_price = st.slider("Maximum Price", min_price, int(df['Price_Range_USD'].max()), int(df['Price_Range_USD'].max()))

        # Filter by Eco-labels
        st.subheader("Eco-labels and Certifications")
        eco_labels = df['Certification'].unique()  # Assuming 'Certification' is a column for certifications or eco-labels
        selected_labels = st.multiselect("Select eco-labels:", options=eco_labels)

        # Additional Filters - Checkboxes for Sustainability Features
        st.subheader("Sustainability Features")
        low_carbon = st.checkbox("Low Carbon Footprint")
        minimal_water = st.checkbox("Minimal Water Use")
        
    # Apply Filters
    filtered_data = df.copy()

    if selected_brands:
        filtered_data = filtered_data[filtered_data['Brand'].isin(selected_brands)]

    filtered_data = filtered_data[(filtered_data['Price_Range_USD'] >= min_price) & (filtered_data['Price_Range_USD'] <= max_price)]

    if selected_labels:
        filtered_data = filtered_data[filtered_data['Certification'].isin(selected_labels)]

    if low_carbon:
        filtered_data = filtered_data[filtered_data['Carbon_Footprint_kgCO2e'] < 20]  # Adjust threshold as needed

    if minimal_water:
        filtered_data = filtered_data[filtered_data['Water_Usage_Liters'] < 30]  # Adjust threshold as needed

    # Display Filtered Results
    st.title("Filtered Product Results")
    if not filtered_data.empty:
        st.dataframe(filtered_data)
    else:
        st.write("No products match your search criteria.")

    # Top-right "Interactive Insights" button
    #st.markdown("<style>div.stButton > button { position: fixed; top: 60px; right: 60px; }</style>", unsafe_allow_html=True)
    num_low_carbon = st.number_input("Number of Top Low-Carbon Footprint Products to Display", min_value=1, max_value=10, value=3)

    if st.button("Interactive Insights"):
        # Show Insights Section
        st.subheader("Interactive Insights")

        # User input for number of top low-carbon products to display
        #num_low_carbon = st.number_input("Number of Top Low-Carbon Footprint Products to Display", min_value=1, max_value=10, value=3)

        # Display Top N Products with Lowest Carbon Footprint
        top_carbon = filtered_data.nsmallest(num_low_carbon, 'Carbon_Footprint_kgCO2e')
        if not top_carbon.empty:
            st.write(f"### Top {num_low_carbon} Products with Lowest Carbon Footprint:")
            st.dataframe(top_carbon[['Product_Name', 'Brand', 'Carbon_Footprint_kgCO2e']])

        # User input for keyword search in Packaging_Type column
        if 'Packaging_Type' in filtered_data.columns:
            packaging_keyword = st.text_input("Enter keyword for recycled packaging search (e.g., 'recycled')", "recycled")
            recycled_packaging = filtered_data[filtered_data['Packaging_Type'].str.contains(packaging_keyword, case=False, na=False)]
            if not recycled_packaging.empty:
                st.write(f"### Products with '{packaging_keyword}' in Packaging Type:")
                st.dataframe(recycled_packaging[['Product_Name', 'Brand', 'Packaging_Type']])
            else:
                st.write(f"No products found with '{packaging_keyword}' in packaging type.")
        else:
            st.write("Packaging data is not available.")

app()
