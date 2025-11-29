# processor.py
import pandas as pd, os, time
from datetime import datetime

BASE = os.path.join(os.path.dirname(__file__), "..")
STREAM = os.path.join(BASE, "stream")
OUT = os.path.join(BASE, "output")
os.makedirs(OUT, exist_ok=True)
TRAFFIC = os.path.join(STREAM, "traffic_stream.csv")
AQ = os.path.join(STREAM, "aq_stream.csv")
MERGED = os.path.join(OUT, "merged_live.csv")

def safe_read(path, **kwargs):
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path, **kwargs)

print("Processor starting. CTRL+C to stop.")
try:
    while True:
        df_t = safe_read(TRAFFIC, parse_dates=["timestamp"])
        df_a = safe_read(AQ, parse_dates=["timestamp"])
        if df_t.empty or df_a.empty:
            time.sleep(1)
            continue

        df_t['timestamp'] = pd.to_datetime(df_t['timestamp'])
        df_a['timestamp'] = pd.to_datetime(df_a['timestamp'])
        df_t['minute'] = df_t['timestamp'].dt.floor('min')
        df_a['minute'] = df_a['timestamp'].dt.floor('min')

        # aggregate traffic per minute across roads
        traffic_agg = df_t.groupby('minute').agg({
            'cars_count':'sum',
            'avg_speed_kmh':'mean'
        }).reset_index()

        # agg AQ per minute (city average)
        aq_agg = df_a.groupby('minute').agg({
            'pm2_5':'mean','pm10':'mean','no2':'mean','co':'mean','aqi':'mean'
        }).reset_index()

        merged = pd.merge(traffic_agg, aq_agg, on='minute', how='left')
        merged = merged.ffill().bfill().fillna(0)

        # derive
        merged['traffic_level'] = pd.cut(merged['cars_count'], bins=[-1,100,300,600,100000], labels=['Low','Medium','High','Very High'])
        merged.to_csv(MERGED, index=False)
        print("Wrote merged_live.csv (rows):", len(merged))
        time.sleep(5)
except KeyboardInterrupt:
    print("Processor stopped.")
