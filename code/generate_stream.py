# generate_stream.py
import csv, time, random, os
from datetime import datetime

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "stream")
os.makedirs(OUT_DIR, exist_ok=True)
TRAFFIC_FILE = os.path.join(OUT_DIR, "traffic_stream.csv")
AQ_FILE = os.path.join(OUT_DIR, "aq_stream.csv")

if not os.path.exists(TRAFFIC_FILE):
    with open(TRAFFIC_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["timestamp","road_id","road_name","cars_count","avg_speed_kmh","district","lat","lon"])

if not os.path.exists(AQ_FILE):
    with open(AQ_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["timestamp","district","pm2_5","pm10","no2","co","aqi","lat","lon"])

SENSOR_ROADS = [
    (1,"صلاح سالم","مدينة نصر",30.067,31.330),
    (2,"الهرم","الجيزة",29.973,31.126),
    (3,"كورنيش النيل","وسط البلد",30.046,31.235),
    (4,"المعادي كورنيش","المعادي",29.975,31.255),
    (5,"محور المشير/التجمع","التجمع الخامس",30.021,31.499)
]

DISTRICTS = {
    "مدينة نصر": (30.067,31.330),
    "الجيزة": (29.973,31.126),
    "وسط البلد": (30.046,31.235),
    "المعادي": (29.975,31.255),
    "التجمع الخامس": (30.021,31.499)
}

print("Stream generator starting — Ctrl+C to stop.")
try:
    while True:
        ts = datetime.utcnow().isoformat()
        # traffic
        road = random.choice(SENSOR_ROADS)
        cars = max(0,int(random.gauss(120,40)))
        speed = max(5, random.gauss(40 - (cars/120)*10, 8))
        lat = road[3] + random.uniform(-0.0008,0.0008)
        lon = road[4] + random.uniform(-0.0008,0.0008)
        with open(TRAFFIC_FILE,"a",newline="") as f:
            csv.writer(f).writerow([ts, road[0], road[1], cars, round(speed,2), road[2], round(lat,6), round(lon,6)])

        # aq
        dis = random.choice(list(DISTRICTS.keys()))
        base_pm25 = random.uniform(20,120)
        pm25 = max(1, base_pm25 + (cars/150)*20 + random.gauss(0,5))
        pm10 = max(1, pm25*1.6 + random.gauss(0,6))
        no2 = max(0.1, random.uniform(10,80) + (cars/200)*30)
        co = max(0.05, random.uniform(0.3,1.2))
        lat2, lon2 = DISTRICTS[dis]
        lat2 += random.uniform(-0.0008,0.0008); lon2 += random.uniform(-0.0008,0.0008)
        aqi = pm25*0.5 + pm10*0.3 + no2*0.2
        with open(AQ_FILE,"a",newline="") as f:
            csv.writer(f).writerow([ts, dis, round(pm25,2), round(pm10,2), round(no2,2), round(co,2), round(aqi,2), round(lat2,6), round(lon2,6)])

        time.sleep(1)  # 1 second cadence; change to 5 or 10 if too fast
except KeyboardInterrupt:
    print("Stopped.")
