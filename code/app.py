# app.py
import streamlit as st, pandas as pd, os
BASE = os.path.join(os.path.dirname(__file__), "..")
MERGED = os.path.join(BASE, "output", "merged_live.csv")
st.title("Smart City Live Dashboard - Cairo (Simulated)")
if os.path.exists(MERGED):
    df = pd.read_csv(MERGED, parse_dates=['minute'])
    last = df.tail(1).iloc[0]
    st.metric("Vehicles (last minute)", int(last['cars_count']))
    st.metric("Avg Speed", round(last['avg_speed_kmh'],2))
    st.metric("PM2.5 (last)", round(last['pm2_5'],2))
    st.line_chart(df.set_index('minute')[['cars_count','pm2_5']].tail(200))
else:
    st.write("No merged data yet. Run processor.")
