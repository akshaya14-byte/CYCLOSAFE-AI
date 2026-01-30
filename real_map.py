import folium
import webbrowser
import os
from math import sqrt
from folium.plugins import TimestampedGeoJson
CITIES = {
    "Chennai": (13.0827, 80.2707),
    "Cuddalore": (11.7447, 79.7644),
    "Nagapattinam": (10.7660, 79.8431),
    "Ramanathapuram": (9.4071, 78.8308),
    "Madurai": (9.9252, 78.1198),
    "Trichy": (10.7905, 78.7047),
    "Thoothukudi": (8.7642, 78.1348),
    "Puducherry": (11.9416, 79.8083),
}
def distance(a, b):
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def generate_cyclone_path(start_lat, start_lon, end_lat, end_lon):
    path = []
    steps = 6
    for i in range(steps):
        t = i / (steps - 1)
        lat = start_lat + t * (end_lat - start_lat)
        lon = start_lon + t * (end_lon - start_lon)
        path.append([lat, lon])
    return path

def generate_map(start_lat, start_lon, end_lat, end_lon):


    path = generate_cyclone_path(start_lat, start_lon, end_lat, end_lon)

    m = folium.Map(
        location=path[-1],
        zoom_start=6,
        tiles="OpenStreetMap"
    )
    folium.PolyLine(
        locations=path,
        color="blue",
        weight=4,
        tooltip="Predicted Cyclone Path"
    ).add_to(m)
    features = []
    for i, point in enumerate(path):
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [point[1], point[0]]
            },
            "properties": {
                "time": f"2026-01-29T0{i}:00:00",
                "popup": "Cyclone Position",
                "icon": "circle",
                "iconstyle": {
                    "fillColor": "red",
                    "fillOpacity": 0.8,
                    "stroke": "true",
                    "radius": 8
                }
            }
        })

    TimestampedGeoJson(
        {
            "type": "FeatureCollection",
            "features": features,
        },
        period="PT1H",
        auto_play=True,
        loop=True
    ).add_to(m)

    zones = [
        (50000, "red", "High Risk"),
        (100000, "orange", "Moderate Risk"),
        (200000, "green", "Low Risk")
    ]

    for radius, color, label in zones:
        folium.Circle(
            location=path[0],
            radius=radius,
            color=color,
            fill=True,
            fill_opacity=0.2,
            tooltip=label
        ).add_to(m)

    for city, (lat, lon) in CITIES.items():
        d = distance(path[-1], (lat, lon))

        if d < 1.2:
            risk = "HIGH"
            color = "red"
        elif d < 2.5:
            risk = "MODERATE"
            color = "orange"
        else:
            continue

        folium.Marker(
            [lat, lon],
            popup=f"{city} — {risk}",
            icon=folium.Icon(color=color, icon="warning-sign")
        ).add_to(m)

    file_path = "cyclone_map.html"
    m.save(file_path)
    webbrowser.open("file://" + os.path.realpath(file_path))

def show_map(start_lat, start_lon, pred_lat, pred_lon):
    generate_map(start_lat, start_lon, pred_lat, pred_lon)

