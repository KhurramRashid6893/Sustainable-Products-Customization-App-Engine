
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import lightgbm as lgb
import random

def app():
    # Load and preprocess data
    df = pd.read_csv("eco_friendly_product_recommendation_data_consistent_names.csv")
    df["Compliance_with_Standards"] = df["Compliance_with_Standards"].fillna("ISO 14001")
    df["Certification"] = df["Certification"].fillna("Energy Star")

    # Map categorical values to numeric codes for model training
    sustainability_mapping = {'Partially Sustainable': 0, 'Non-Sustainable': 1, 'Sustainable': 2}
    df['Resource_Sourcing'] = df['Resource_Sourcing'].map(sustainability_mapping)

    impact_mapping = {'low': 0, 'medium': 1, 'high': 2}
    df['Manufacturing_Impact'] = df['Manufacturing_Impact'].str.lower().str.strip().map(impact_mapping)

    # Define feature columns and target variable
    feature_columns = ['Carbon_Footprint_kgCO2e', 'Water_Usage_Liters', 'Manufacturing_Impact', 'Price_Range_USD']
    X = df[feature_columns]
    y = df['Resource_Sourcing']

    # Train models
    rf_model = RandomForestClassifier().fit(X, y)
    xgb_model = xgb.XGBClassifier().fit(X, y)
    lgb_model = lgb.LGBMClassifier().fit(X, y)

    def predict_resource_sourcing(model, carbon_footprint, water_usage, manufacturing_impact, price_range):
        inputs = pd.DataFrame([[carbon_footprint, water_usage, manufacturing_impact, price_range]], columns=feature_columns)
        prediction = model.predict(inputs)
        return prediction[0]

    st.title("Eco-Friendly Product Recommendation System 🌍")
    st.write("Predict and explore the sustainability level of products based on environmental metrics.")

    # Sidebar - User inputs
    st.sidebar.header("Input Details and Model Selection")
    carbon_footprint = random.uniform(0.0, 100.0)  # Random float between 0 and 100
    water_usage = random.randint(0, 200)
    manufacturing_impact = st.sidebar.selectbox("Manufacturing Impact", ["Low", "Medium", "High"]).lower()
    price_range = st.sidebar.slider("Price Range (USD)", min_value=5.0, max_value=500.0, step=10.0)
    manufacturing_impact = impact_mapping[manufacturing_impact]

    user_choice = st.sidebar.radio("Choose Prediction Model:", ("Fast (Random Forest)", "Better (LightGBM)", "Best (XGBoost)"))
    model = rf_model if user_choice == "Fast (Random Forest)" else (lgb_model if user_choice == "Better (LightGBM)" else xgb_model)

    # Predict sustainability
    if st.sidebar.button("Show Product"):
        prediction = predict_resource_sourcing(model, carbon_footprint, water_usage, manufacturing_impact, price_range)
        sustainability_status = ["Partially Sustainable", "Non-Sustainable", "Sustainable"][prediction]
        
        st.success(f"Predicted Sustainability Status is {sustainability_status}, So Recommending the Sustainable Product with Sustainability Score.")


        # Filter recommended products by sustainability and price range
        filtered_products = df[(df['Resource_Sourcing'] == prediction) & (df['Price_Range_USD'] <= price_range)][['Product_Name', 'Category', 'Brand', 'Carbon_Footprint_kgCO2e', 'Water_Usage_Liters', 'Manufacturing_Impact', 'Price_Range_USD']]
        
        if not filtered_products.empty:
            st.write("Recommended Products:")
            for _, product in filtered_products.iterrows():
                # Display product information
                st.subheader(f"{product['Product_Name']} ({product['Brand']})")
                st.write(f"Category: {product['Category']}")
                st.write(f"Price Range: ${product['Price_Range_USD']}")
                
                # Display icons and visual indicators
                st.write("Sustainability Metrics")
                st.write(f"Carbon Footprint: {product['Carbon_Footprint_kgCO2e']} kgCO2e 🌿")
                st.write(f"Water Usage: {product['Water_Usage_Liters']} Liters 💧")
                st.write(f"Manufacturing Impact: {'Low' if product['Manufacturing_Impact'] == 0 else 'Medium' if product['Manufacturing_Impact'] == 1 else 'High'} 🔧")

                # Add Sustainability Score
                score = 100 - ((product['Carbon_Footprint_kgCO2e'] / 100) * 50 + (product['Water_Usage_Liters'] / 200) * 30 + product['Manufacturing_Impact'] * 20)
                st.write(f"Sustainability Score: {score:.2f}")
                st.progress(int(score))

                # Green badge for highly sustainable products
                if score > 75:
                    st.markdown(f"<span style='color:white; background-color:green; padding: 5px 10px; border-radius: 5px;'>Highly Sustainable</span>", unsafe_allow_html=True)
                elif score > 50:
                    st.markdown(f"<span style='color:white; background-color:yellowgreen; padding: 5px 10px; border-radius: 5px;'>Moderately Sustainable</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span style='color:white; background-color:orange; padding: 5px 10px; border-radius: 5px;'>Low Sustainability</span>", unsafe_allow_html=True)

                st.write("---")
        else:
            st.warning("No products found within the selected price range and sustainability level.")
    
    st.write("Empowering eco-friendly choices with machine learning models!")


















