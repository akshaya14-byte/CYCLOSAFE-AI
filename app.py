import tkinter as tk
from tkinter import ttk, messagebox
import pickle
import numpy as np
from impact_detector import (
    detect_impacted_regions,
    generate_alert_summary,
    generate_safety_plan
)
from real_map import show_map
from tkinter import scrolledtext
MODEL_PATH = "cyclone_model.pkl"

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("✅ ML Model Loaded")
except:
    messagebox.showerror("Error", "cyclone_model.pkl not found!")
    exit()

def generate_ml_path(lat, lon, wind, pressure, steps=6):
    path = []
    impact_scores = []

    cur_lat, cur_lon = lat, lon

    for _ in range(steps):
        X = np.array([[cur_lat, cur_lon, wind, pressure]])
        pred = model.predict(X)[0]

        cur_lat = float(pred[0])
        cur_lon = float(pred[1])
        impact = float(pred[2])

        path.append([cur_lat, cur_lon])
        impact_scores.append(impact)

    return path, max(impact_scores)



def predict():
    
    try:
        lat = float(lat_entry.get())
        lon = float(lon_entry.get())
        wind = float(wind_entry.get())
        pressure = float(pressure_entry.get())
        path, impact_score = generate_ml_path(
            lat, lon, wind, pressure
        )

        next_lat = round(path[-1][0], 3)
        next_lon = round(path[-1][1], 3)
        impact_score = round(impact_score, 1)
        show_map(
            lat,           
            lon,
            next_lat, 
            next_lon
        )
        if impact_score > 70:
            risk_level = "HIGH"
        elif impact_score > 40:
            risk_level = "MODERATE"
        else:
            risk_level = "LOW"

        
        impacted_regions = detect_impacted_regions(lat, lon)


        alert_summary = generate_alert_summary(
            impact_score,
            risk_level,
            impacted_regions
        )

        safety_plan = generate_safety_plan(risk_level)

        result_label.config(
            text=f"📍 Predicted Cyclone Trajectory End\n"
                 f"Latitude: {next_lat}\n"
                 f"Longitude: {next_lon}\n\n"
                 f"🔥 Impact Score: {impact_score}\n"
                 f"⚠️ Risk Level: {risk_level}"
        )

        impact_textbox.delete("1.0", "end")
        impact_textbox.insert("end", alert_summary)

        safety_textbox.delete("1.0", "end")
        safety_textbox.insert("end", safety_plan)

        


    except Exception as e:
        messagebox.showerror("Prediction Error", str(e))

app = tk.Tk()
app.title("🌪️ CycloSafe AI - Cyclone Prediction System")
app.geometry("720x520")
app.configure(bg="#121212")

style = ttk.Style()
style.theme_use("default")

frame = tk.Frame(app, bg="#1f1f1f", padx=20, pady=20)
frame.pack(expand=True)

title = tk.Label(
    frame,
    text="Cyclone Prediction Dashboard",
    font=("Segoe UI", 20, "bold"),
    fg="white",
    bg="#1f1f1f"
)
title.pack(pady=10)

def create_input(label):
    row = tk.Frame(frame, bg="#1f1f1f")
    row.pack(pady=5)
    tk.Label(
        row,
        text=label,
        width=15,
        anchor="w",
        fg="white",
        bg="#1f1f1f"
    ).pack(side="left")
    entry = tk.Entry(row, width=20)
    entry.pack(side="left")
    return entry

lat_entry = create_input("Latitude")
lon_entry = create_input("Longitude")
wind_entry = create_input("Wind Speed")
pressure_entry = create_input("Pressure")

predict_btn = tk.Button(
    frame,
    text="🚀 Predict Cyclone",
    font=("Segoe UI", 12, "bold"),
    bg="#00b894",
    fg="white",
    command=predict
)
predict_btn.pack(pady=15)

result_label = tk.Label(
    frame,
    text="Prediction will appear here...",
    fg="white",
    bg="#1f1f1f",
    font=("Consolas", 12),
    justify="left"
)
result_label.pack(pady=10)

impact_textbox = scrolledtext.ScrolledText(
    frame,
    width=50,
    height=6,
    bg="#111",
    fg="white",
    font=("Consolas", 11)
)
impact_textbox.pack(pady=5)

safety_textbox = scrolledtext.ScrolledText(
    frame,
    width=50,
    height=6,
    bg="#111",
    fg="white",
    font=("Consolas", 11)
)
safety_textbox.pack(pady=5)

print("🚀 Starting CYCLOSAFE AI GUI...")
app.mainloop()
