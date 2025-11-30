import streamlit as st
import pandas as pd

st.title("Cairo Smart City Dashboard")

# Load datasets
traffic = pd.read_csv("traffic_cairo.csv")
pollution = pd.read_csv("pollution_cairo.csv")
gps = pd.read_csv("gps_cairo.csv")

st.subheader("🚦 Traffic Data Sample")
st.write(traffic.head())

st.subheader("🌫️ Pollution Data Sample")
st.write(pollution.head())

st.subheader("📍 GPS Data Sample")
st.write(gps.head())
