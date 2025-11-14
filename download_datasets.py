import pandas as pd
import json
import os

os.makedirs('data/raw', exist_ok=True)

# 1. PM-KISAN Tamil Nadu Farmers (Sample CSV)
print("Creating PM-KISAN TN sample data...")
df_pmkisan = pd.DataFrame({
    'farmer_id': [1001, 1002, 1003, 1004, 1005],
    'name': ['Raj Kumar', 'Priya Singh', 'Arjun Patel', 'Lakshmi Devi', 'Vikram Sharma'],
    'district': ['Madurai', 'Chennai', 'Coimbatore', 'Tiruchirappalli', 'Salem'],
    'land_size_ha': [2.5, 1.8, 3.2, 2.0, 1.5],
    'subsidy_amount': [6000, 6000, 6000, 6000, 6000]
})
df_pmkisan.to_csv('data/raw/pmkisan_tn.csv', index=False)
print("✓ PM-KISAN data saved")

# 2. Soil Health Cards TN
print("Creating Soil Health sample data...")
df_soil = pd.DataFrame({
    'farmer_id': [1001, 1002, 1003, 1004, 1005],
    'ph': [6.5, 7.2, 6.8, 7.0, 6.9],
    'nitrogen': [280, 250, 300, 270, 290],
    'phosphorus': [22, 18, 25, 20, 23],
    'potassium': [195, 210, 200, 205, 190],
    'organic_matter': [0.85, 0.92, 0.78, 0.88, 0.81]
})
df_soil.to_csv('data/raw/soil_tn.csv', index=False)
print("✓ Soil Health data saved")

# 3. e-NAM Mandi Prices TN
print("Creating e-NAM sample data...")
df_enam = pd.DataFrame({
    'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
    'mandi': ['Madurai', 'Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli'],
    'commodity': ['Rice', 'Sugarcane', 'Maize', 'Cotton', 'Groundnut'],
    'price_per_quintal': [3200, 280, 1850, 5600, 4200],
    'quantity_traded': [500, 1200, 800, 300, 600]
})
df_enam.to_csv('data/raw/enam_tn.csv', index=False)
print("✓ e-NAM data saved")

# 4. Tamil Nadu Land Records (GeoJSON Sample)
print("Creating Land Records sample data...")
geo_land = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"farmer_id": 1001, "land_id": "TN-MAD-001"},
            "geometry": {"type": "Point", "coordinates": [9.9252, 78.1198]}
        },
        {
            "type": "Feature",
            "properties": {"farmer_id": 1002, "land_id": "TN-CHN-001"},
            "geometry": {"type": "Point", "coordinates": [13.0827, 80.2707]}
        }
    ]
}
with open('data/raw/tn_land.geojson', 'w') as f:
    json.dump(geo_land, f, indent=2)
print("✓ Land Records data saved")

# 5. Weather TN (Sample)
print("Creating Weather sample data...")
df_weather = pd.DataFrame({
    'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
    'district': ['Madurai', 'Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli'],
    'temperature_max': [32.5, 31.2, 29.8, 33.1, 30.5],
    'temperature_min': [22.1, 21.8, 20.5, 23.2, 21.0],
    'humidity': [65, 72, 68, 62, 70],
    'rainfall': [0, 2.3, 0, 5.1, 0.5]
})
df_weather.to_csv('data/raw/weather_tn.csv', index=False)
print("✓ Weather data saved")

print("\n✅ All datasets created successfully!")