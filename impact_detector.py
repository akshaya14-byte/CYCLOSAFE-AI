from geo_data import LOCATIONS, distance
import math

from geo_data import LOCATIONS

print("DEBUG LOCATIONS STATES:", list(LOCATIONS.keys()))
from geo_data import LOCATIONS, distance

def detect_impacted_regions(lat, lon, radius=300):
    impacted = []

    for state, cities in LOCATIONS.items():
        nearest_city = None
        nearest_dist = float("inf")

        for city, coord in cities.items():
            d = distance((lat, lon), coord)

            if d < nearest_dist:
                nearest_dist = d
                nearest_city = city
        if nearest_dist <= radius:
            impacted.append({
                "state": state,
                "district": nearest_city,
                "distance": round(nearest_dist, 1)
            })

    impacted.sort(key=lambda x: x["distance"])

    return impacted
def generate_alert_summary(impact_score, risk, impacted_regions):

    if not impacted_regions:
        return (
            "✅ CYCLONE UPDATE\n\n"
            "Current prediction indicates no major populated regions "
            "within immediate impact radius.\n\n"
            f"Impact Score: {impact_score}\n"
            f"Risk Level: {risk}"
        )

    primary = impacted_regions[0]

    summary = f"""
⚠️ CYCLONE ALERT ⚠️

Primary Threat Area:
• State: {primary['state']}
• District: {primary['district']}
• Distance from cyclone: {primary['distance']} km

Risk Level: {risk}
Impact Severity Score: {impact_score}

Expected Hazards:
• Heavy to extreme rainfall
• Gale-force winds
• Power & communication disruption
• Flooding in low-lying regions
• Coastal storm surge risk
"""

    return summary.strip()
def generate_safety_plan(risk):

    risk = risk.upper()

    if "HIGH" in risk:
        return """
🚨 HIGH RISK – IMMEDIATE ACTION REQUIRED

• Begin evacuation from coastal & low-lying zones
• Secure homes, boats, and livestock
• Store drinking water & dry food for 72 hours
• Charge mobile phones & power banks
• Keep emergency kits ready
• Follow government & disaster authority alerts
• Avoid sea travel and highways
"""

    elif "MODERATE" in risk:
        return """
⚠️ MODERATE RISK – PREPARE & STAY ALERT

• Stay indoors during peak cyclone hours
• Secure windows, doors, and rooftops
• Avoid unnecessary travel
• Keep emergency contacts accessible
• Monitor official weather updates regularly
"""

    else:
        return """
✅ LOW RISK – ADVISORY

• No evacuation required at this time
• Stay informed through official updates
• Normal activities may continue with caution
"""
