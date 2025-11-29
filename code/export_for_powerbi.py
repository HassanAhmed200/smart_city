# export_for_powerbi.py
import pandas as pd, os
BASE = os.path.join(os.path.dirname(__file__), "..")
MERGED = os.path.join(BASE, "output", "merged_live.csv")
PRED = os.path.join(BASE, "output", "predictions.csv")
OUTX = os.path.join(BASE, "output", "powerbi_export.xlsx")

if not os.path.exists(MERGED):
    print("Run processor first.")
    exit(1)

df = pd.read_csv(MERGED, parse_dates=['minute'])
last_24h = df.tail(24*60) if len(df)>24*60 else df
hourly = last_24h.copy()
hourly['hour'] = hourly['minute'].astype('datetime64[ns]').dt.floor('h')
hourly = hourly.groupby('hour').agg({'cars_count':'sum','avg_speed_kmh':'mean','pm2_5':'mean','aqi':'mean'}).reset_index()
top_congested = df.sort_values('cars_count', ascending=False).head(100)
preds = pd.read_csv(PRED) if os.path.exists(PRED) else pd.DataFrame()

with pd.ExcelWriter(OUTX, engine='openpyxl') as writer:
    last_24h.to_excel(writer, sheet_name='merged_last', index=False)
    hourly.to_excel(writer, sheet_name='hourly', index=False)
    top_congested.to_excel(writer, sheet_name='top_congested', index=False)
    preds.to_excel(writer, sheet_name='predictions', index=False)

print("Exported", OUTX)
