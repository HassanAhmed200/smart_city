# predictor.py
import pandas as pd, os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

BASE = os.path.join(os.path.dirname(__file__), "..")
MERGED = os.path.join(BASE, "output", "merged_live.csv")
PRED_OUT = os.path.join(BASE, "output", "predictions.csv")

if not os.path.exists(MERGED):
    print("Run processor first.")
    exit(1)

df = pd.read_csv(MERGED, parse_dates=['minute'])
df = df.sort_values('minute').reset_index(drop=True)
df['hour'] = df['minute'].astype('datetime64[ns]').dt.hour
df['min_of_day'] = df['minute'].astype('datetime64[ns]').dt.hour*60 + df['minute'].astype('datetime64[ns]').dt.minute
df['pm2_5_next'] = df['pm2_5'].shift(-1)
df = df.dropna()
features = ['cars_count','avg_speed_kmh','pm2_5','hour','min_of_day']
X = df[features]; y = df['pm2_5_next']
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, shuffle=False)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train,y_train)
pred = model.predict(X_test)
mse = mean_squared_error(y_test,pred)
print("Test MSE:", mse)
# predict next minute from last row
last = X.iloc[[-1]]
next_pred = model.predict(last)[0]
print("Next minute PM2.5 prediction:", round(next_pred,2))
# append to CSV
import datetime
row = {'timestamp': datetime.datetime.utcnow().isoformat(), 'pm2_5_pred_next_min': round(next_pred,2), 'mse':mse}
pd.DataFrame([row]).to_csv(PRED_OUT, mode='a', header=not os.path.exists(PRED_OUT), index=False)
print("Saved prediction to", PRED_OUT)
