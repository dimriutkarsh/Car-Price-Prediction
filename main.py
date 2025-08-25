import streamlit as st
import pickle
import numpy as np

# ---------------------------
# Load Trained Model
# ---------------------------
with open("models.pkl", "rb") as f:
    model = pickle.load(f)

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="centered"
)

# ---------------------------
# Custom CSS Styling (safe selectors)
# ---------------------------
st.markdown("""
    <style>
    /* Main body styling */
    .main {
        background-color: #eef1f5; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 20px;
        border-radius: 12px;
    }

    /* Title styling */
    h1 {
        color: #334455; 
        text-align: center;
        border-bottom: 2px solid #00b0ff; 
        padding-bottom: 10px;
        margin-bottom: 20px;
        font-size: 2.2em;
    }

    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #00c6ff, #0072ff);
        color: white;
        border-radius: 12px;
        padding: 12px 30px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4);
        display: block;
        margin: 20px auto; /* center button */
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0072ff, #00c6ff);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 114, 255, 0.6);
        cursor: pointer;
    }

    /* Input & Select styling */
    .stSelectbox, .stNumberInput {
        font-size: 16px;
    }
    .stSelectbox label, .stNumberInput label {
        font-weight: bold;
        color: #333;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #cccccc;
        padding: 6px;
    }

    /* Result Card */
    .result-card {
        padding: 25px;
        background: linear-gradient(145deg, #f0fdfc, #e5f5f4);
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 30px;
        border: 2px solid #00a878;
    }
    .result-card h2 {
        color: #007a5f;
        margin-bottom: 5px;
    }
    .result-card h1 {
        font-size: 3em !important;
        color: #00b07f;
        font-weight: 800;
        margin-top: 5px;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
    /* Make dropdown and slider labels white */
.css-1p0tmns, .css-10trblm, .stMarkdown p, label {
    color: white !important;
    font-weight: 500;
    font-size: 18px;
}

    </style>
""", unsafe_allow_html=True)

# ---------------------------
# Title
# ---------------------------
st.title("🚗 Car Price Prediction App")
st.write("Predict the price of your car using our ML model.")

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.header("ℹ️ About")
st.sidebar.write("This app predicts the **resale price** of your car using a trained ML model.")
st.sidebar.write("Made with Streamlit")

# ---------------------------
# User Inputs (2 columns)
# ---------------------------
st.header("Enter Car Details:")

col1, col2 = st.columns(2)

with col1:
    year = st.number_input("Year of Purchase", 1990, 2025, 2015)
    present_price = st.number_input("Present Price (in lakhs)", 0.0, 50.0, 5.0)
    kms_driven = st.number_input("Kms Driven", 0, 1000000, 50000)

with col2:
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
    seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
    owner = st.number_input("Number of Previous Owners", 0, 5, 0)

# Encoding categorical values
fuel_map = {"Petrol": 0, "Diesel": 1, "CNG": 2}
seller_map = {"Dealer": 0, "Individual": 1}
transmission_map = {"Manual": 0, "Automatic": 1}

features = np.array([[year, present_price, kms_driven,
                      fuel_map[fuel_type],
                      seller_map[seller_type],
                      transmission_map[transmission],
                      owner]])

# ---------------------------
# Prediction
# ---------------------------
if st.button("🔮 Predict Selling Price"):
    prediction = model.predict(features)
    st.markdown(f"""
    <div class="result-card">
        <h2>💰 Predicted Selling Price</h2>
        <h1>₹ {round(prediction[0], 2)} lakhs</h1>
    </div>
    """, unsafe_allow_html=True)
