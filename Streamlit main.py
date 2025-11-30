import streamlit as st
import pandas as pd

st.title("📊 Smart City Dashboard - Cairo")

# ================================
# Team Members Section
# ================================
st.subheader("👨‍💻 Project Team Members")

st.write("""
**By:**
- Eng / Youssef Ehab Taha El-Morsi  
-Eng / Ahmed Maged Salah Elsayed  
-Eng / Mohamed Saber Salah Abd Elwhab  
-Eng / Hassan Ahmed Ismail Ibrahim  
-Eng / Ahmed Maged Ahmed Abdelrahman  
""")

st.write("مرحباً! هذا تطبيق Streamlit لعرض بيانات المدينة الذكية في القاهرة.")

# Load datasets
@st.cache_data
def load_data():
    traffic = pd.read_csv("traffic_cairo.csv")
    pollution = pd.read_csv("pollution_cairo.csv")
    gps = pd.read_csv("gps_cairo.csv")
    return traffic, pollution, gps

traffic, pollution, gps = load_data()

# --- Traffic Section ---
st.header("🚗 Traffic Data")
st.write("أول 5 صفوف من بيانات المرور:")
st.dataframe(traffic.head())

# --- Pollution Section ---
st.header("🌫 Pollution Data")
st.write("أول 5 صفوف من بيانات التلوث:")
st.dataframe(pollution.head())

# --- GPS Section ---
st.header("📍 GPS Data")
st.write("أول 5 صفوف من بيانات الـ GPS:")
st.dataframe(gps.head())
