"""
Seed data: countries that appear on the globe.

We don't need all 195 countries — tech news is heavily concentrated in maybe 30.
Adding more later is just appending to this list.

Coordinates are population-weighted centroids (close enough for globe markers).
"""

COUNTRIES = [
    # North America
    {"code": "US", "name": "United States", "latitude": 39.8283, "longitude": -98.5795},
    {"code": "CA", "name": "Canada", "latitude": 56.1304, "longitude": -106.3468},
    {"code": "MX", "name": "Mexico", "latitude": 23.6345, "longitude": -102.5528},
    # Europe
    {"code": "GB", "name": "United Kingdom", "latitude": 55.3781, "longitude": -3.4360},
    {"code": "DE", "name": "Germany", "latitude": 51.1657, "longitude": 10.4515},
    {"code": "FR", "name": "France", "latitude": 46.6034, "longitude": 1.8883},
    {"code": "NL", "name": "Netherlands", "latitude": 52.1326, "longitude": 5.2913},
    {"code": "ES", "name": "Spain", "latitude": 40.4637, "longitude": -3.7492},
    {"code": "IT", "name": "Italy", "latitude": 41.8719, "longitude": 12.5674},
    {"code": "SE", "name": "Sweden", "latitude": 60.1282, "longitude": 18.6435},
    {"code": "PL", "name": "Poland", "latitude": 51.9194, "longitude": 19.1451},
    {"code": "IE", "name": "Ireland", "latitude": 53.4129, "longitude": -8.2439},
    {"code": "CH", "name": "Switzerland", "latitude": 46.8182, "longitude": 8.2275},
    # Asia
    {"code": "IN", "name": "India", "latitude": 20.5937, "longitude": 78.9629},
    {"code": "CN", "name": "China", "latitude": 35.8617, "longitude": 104.1954},
    {"code": "JP", "name": "Japan", "latitude": 36.2048, "longitude": 138.2529},
    {"code": "KR", "name": "South Korea", "latitude": 35.9078, "longitude": 127.7669},
    {"code": "SG", "name": "Singapore", "latitude": 1.3521, "longitude": 103.8198},
    {"code": "ID", "name": "Indonesia", "latitude": -0.7893, "longitude": 113.9213},
    {"code": "VN", "name": "Vietnam", "latitude": 14.0583, "longitude": 108.2772},
    {"code": "IL", "name": "Israel", "latitude": 31.0461, "longitude": 34.8516},
    {"code": "AE", "name": "United Arab Emirates", "latitude": 23.4241, "longitude": 53.8478},
    # Oceania
    {"code": "AU", "name": "Australia", "latitude": -25.2744, "longitude": 133.7751},
    {"code": "NZ", "name": "New Zealand", "latitude": -40.9006, "longitude": 174.8860},
    # South America
    {"code": "BR", "name": "Brazil", "latitude": -14.2350, "longitude": -51.9253},
    {"code": "AR", "name": "Argentina", "latitude": -38.4161, "longitude": -63.6167},
    # Africa
    {"code": "ZA", "name": "South Africa", "latitude": -30.5595, "longitude": 22.9375},
    {"code": "NG", "name": "Nigeria", "latitude": 9.0820, "longitude": 8.6753},
    {"code": "KE", "name": "Kenya", "latitude": -0.0236, "longitude": 37.9062},
    {"code": "EG", "name": "Egypt", "latitude": 26.8206, "longitude": 30.8025},
]
