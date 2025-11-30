import pandas as pd

# ================================
# 1) Load Cairo Smart City Datasets
# ================================

traffic = pd.read_csv("traffic_cairo.csv")
pollution = pd.read_csv("pollution_cairo.csv")
gps = pd.read_csv("gps_cairo.csv")

print("===== TRAFFIC DATA SAMPLE =====")
print(traffic.head())

print("\n===== POLLUTION DATA SAMPLE =====")
print(pollution.head())

print("\n===== GPS DATA SAMPLE =====")
print(gps.head())
