import streamlit as st
import pandas as pd
import numpy as np
import joblib
import folium
from streamlit_folium import st_folium
if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "inputs" not in st.session_state:
    st.session_state.inputs = None



# Load model and scaler
model = joblib.load("model/cyclone_rf.pkl")
scaler = joblib.load("model/scaler.pkl")

st.set_page_config(layout="wide")
st.title("🌪️ CycloSafe AI  Cyclone Risk Prediction")

st.markdown("Predict cyclone movement and estimate risk impact.")

# Sidebar input
st.sidebar.header("Input Parameters")

lat = st.sidebar.number_input("Latitude", value=13.0)
lon = st.sidebar.number_input("Longitude", value=80.0)
wind = st.sidebar.slider("Wind Speed (km/h)", 30, 250, 80)
pres = st.sidebar.slider("Pressure (hPa)", 900, 1020, 980)
if st.sidebar.button("🚀 Predict Cyclone Path"):
    st.session_state.show_result = True
    st.session_state.inputs = (lat, lon, wind, pres)


if st.session_state.show_result:

    lat, lon, wind, pres = st.session_state.inputs
    input_data = np.array([[lat, lon, wind, pres]])

    input_scaled = scaler.transform(input_data)

    pred_scaled = model.predict(input_scaled)
    pred = scaler.inverse_transform(
    np.hstack([pred_scaled, [[wind, pres]]]))[0]
    pred_lat, pred_lon = pred[0], pred[1]

    st.subheader("📍 Predicted Next Position")
    st.write(f"Latitude: {pred_lat:.3f}")
    st.write(f"Longitude: {pred_lon:.3f}")

    # Map
    m = folium.Map(location=[pred_lat, pred_lon], zoom_start=6)

    folium.Marker(
        [lat, lon],
        tooltip="Current Position",
        icon=folium.Icon(color="blue")
    ).add_to(m)

    folium.Marker(
        [pred_lat, pred_lon],
        tooltip="Predicted Position",
        icon=folium.Icon(color="red")
    ).add_to(m)

    folium.PolyLine(
    [[lat, lon], [pred_lat, pred_lon]],
    weight=5,
    opacity=0.8
).add_to(m)

    st_folium(m, width=700, height=500)

    # Risk score
    population_factor = 1.5
    risk_score = (wind * population_factor) / 100

    st.subheader("⚠️ Risk Assessment")
    st.metric("Risk Score", f"{risk_score:.1f}")

    if risk_score > 3:
        st.error("🚨 High Risk – Immediate evacuation recommended.")
    elif risk_score > 1.5:
        st.warning("⚠️ Medium Risk – Prepare emergency measures.")
    else:
        st.success("✅ Low Risk – Monitor situation.")


# Impact score (simple logic)
population_factor = 1.5   # demo assumption
risk_score = (wind * population_factor) / 100

st.subheader("⚠️ Risk Assessment")
st.metric("Risk Score", f"{risk_score:.1f}")

if risk_score > 3:
    st.error("🚨 High Risk – Immediate evacuation recommended.")
elif risk_score > 1.5:
    st.warning("⚠️ Medium Risk – Prepare emergency measures.")
else:
    st.success("✅ Low Risk – Monitor situation.")

st.caption("Hackathon prototype – AI-powered cyclone decision support.")
