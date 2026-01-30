from math import sqrt
import math

# -------------------------
# State + District Database
# -------------------------
LOCATIONS = {
    "Tamil Nadu": {
        "Chennai": (13.08, 80.27),
        "Cuddalore": (11.74, 79.76),
        "Nagapattinam": (10.76, 79.84),
        "Ramanathapuram": (9.40, 78.83),
    },
    "Andhra Pradesh": {
        "Nellore": (14.44, 79.98),
        "Ongole": (15.50, 80.05),
        "Machilipatnam": (16.18, 81.13),
        "Visakhapatnam": (17.68, 83.21),
    },
    "Kerala": {
        "Kochi": (9.93, 76.26),
        "Kozhikode": (11.25, 75.78),
        "Thiruvananthapuram": (8.52, 76.93),
    },
    "Odisha": {
        "Gopalpur": (19.26, 84.90),
        "Puri": (19.81, 85.83),
        "Balasore": (21.49, 86.93),
    }
}

import math

# -----------------------------------
# Proper Haversine Distance (KM)
# -----------------------------------
def distance(coord1, coord2):
    """
    Calculate distance between two lat/lon points in KM
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    R = 6371  # Earth radius in KM

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

