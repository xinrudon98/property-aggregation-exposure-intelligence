import pandas as pd
import folium
from folium.plugins import MarkerCluster

# ==================================
# SAMPLE DATA
# ==================================

properties = pd.DataFrame(
    [
        {
            "policy_id": "POL001",
            "lat": 34.095,
            "lon": -118.405,
            "tiv": 2500000,
        },
        {
            "policy_id": "POL002",
            "lat": 34.102,
            "lon": -118.390,
            "tiv": 1800000,
        },
        {
            "policy_id": "POL003",
            "lat": 34.089,
            "lon": -118.415,
            "tiv": 3200000,
        },
    ]
)

# ==================================
# GRID AGGREGATION
# ==================================

GRID_SIZE = 0.01

properties["grid_lat"] = (
    properties["lat"] // GRID_SIZE
) * GRID_SIZE

properties["grid_lon"] = (
    properties["lon"] // GRID_SIZE
) * GRID_SIZE

aggregation = (
    properties
    .groupby(["grid_lat", "grid_lon"])
    .agg(
        property_count=("policy_id", "count"),
        total_tiv=("tiv", "sum")
    )
    .reset_index()
)

# ==================================
# MAP
# ==================================

m = folium.Map(
    location=[34.095, -118.405],
    zoom_start=12
)

marker_cluster = MarkerCluster().add_to(m)

for _, row in properties.iterrows():

    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=f"""
        Policy: {row['policy_id']}<br>
        TIV: ${row['tiv']:,.0f}
        """
    ).add_to(marker_cluster)

# ==================================
# AGGREGATION ZONES
# ==================================

for _, row in aggregation.iterrows():

    total_tiv = row["total_tiv"]

    if total_tiv > 5000000:
        color = "red"
    elif total_tiv > 2500000:
        color = "orange"
    else:
        color = "yellow"

    folium.Rectangle(
        bounds=[
            [row["grid_lat"], row["grid_lon"]],
            [
                row["grid_lat"] + GRID_SIZE,
                row["grid_lon"] + GRID_SIZE
            ]
        ],
        color=color,
        fill=True,
        fill_opacity=0.4,
        popup=f"""
        Properties: {row['property_count']}<br>
        Total TIV: ${total_tiv:,.0f}
        """
    ).add_to(m)

# ==================================
# OUTPUT
# ==================================

m.save("property_aggregation_map.html")

print("Map generated.")
