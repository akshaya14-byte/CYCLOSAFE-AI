import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle

DATA_PATH = "data/processed/india_cyclone_clean.csv"
MODEL_PATH = "cyclone_model.pkl"

print("📂 Loading dataset...")
df = pd.read_csv(DATA_PATH)
print("Samples:", len(df))
df["NEXT_LAT"] = df["LAT"].shift(-1)
df["NEXT_LON"] = df["LON"].shift(-1)
df["IMPACT_SCORE"] = (
    (df["WIND"] / df["WIND"].max()) * 60 +
    ((1010 - df["PRESSURE"]) / 100) * 40
)

df["IMPACT_SCORE"] = df["IMPACT_SCORE"].clip(0, 100)

df.dropna(inplace=True)
FEATURES = ["LAT", "LON", "WIND", "PRESSURE"]
TARGETS = ["NEXT_LAT", "NEXT_LON", "IMPACT_SCORE"]

X = df[FEATURES]
y = df[TARGETS]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("🤖 Training multi-output ML model...")
model = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print("✅ Model trained successfully")
print("📊 Model R² Score:", round(accuracy, 3))
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

print(f"💾 Model saved as: {MODEL_PATH}")
def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

model_loaded = load_model()
def predict_cyclone(lat, lon, wind, pressure):
    """
    Returns:
        next_lat, next_lon, impact_score
    """
    X = np.array([[lat, lon, wind, pressure]])
    pred = model_loaded.predict(X)[0]

    next_lat = float(pred[0])
    next_lon = float(pred[1])
    impact_score = float(pred[2])

    return next_lat, next_lon, impact_score
if __name__ == "__main__":
    lat, lon, impact = predict_cyclone(11.0, 80.0, 140, 970)
    print("Predicted Next Position:", lat, lon)
    print("Predicted Impact Score:", round(impact, 2))
