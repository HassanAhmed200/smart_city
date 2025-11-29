# plots.py
import pandas as pd, os, matplotlib.pyplot as plt
BASE = os.path.join(os.path.dirname(__file__), "..")
MERGED = os.path.join(BASE, "output", "merged_live.csv")
OUT = os.path.join(BASE, "output", "charts"); os.makedirs(OUT, exist_ok=True)
df = pd.read_csv(MERGED, parse_dates=['minute']).tail(500)

plt.figure(figsize=(8,4)); plt.plot(df['minute'], df['cars_count']); plt.xticks(rotation=45)
plt.title("Vehicle Count (recent)"); plt.tight_layout(); plt.savefig(os.path.join(OUT,'cars_count.png')); plt.close()

plt.figure(figsize=(8,4)); plt.plot(df['minute'], df['pm2_5']); plt.xticks(rotation=45)
plt.title("PM2.5 (recent)"); plt.tight_layout(); plt.savefig(os.path.join(OUT,'pm25.png')); plt.close()

plt.figure(figsize=(8,4)); plt.scatter(df['cars_count'], df['pm2_5'], s=10)
plt.title("Cars vs PM2.5"); plt.xlabel("cars_count"); plt.ylabel("pm2_5"); plt.tight_layout()
plt.savefig(os.path.join(OUT,'cars_vs_pm25.png')); plt.close()

print("Saved charts to", OUT)
