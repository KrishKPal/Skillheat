"""
Seed every country we have sources for.
Run after init_db. Idempotent.
"""
import logging
from sqlalchemy import select
from app.database import SessionLocal
from app.models.country import Country

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


# (code, name, latitude, longitude)
COUNTRIES = [
    ("US", "United States",         39.8283,   -98.5795),
    ("IN", "India",                 20.5937,    78.9629),
    ("GB", "United Kingdom",        55.3781,    -3.4360),
    ("DE", "Germany",               51.1657,    10.4515),
    ("FR", "France",                46.6034,     1.8883),
    ("CA", "Canada",                56.1304,  -106.3468),
    ("AU", "Australia",            -25.2744,   133.7751),
    ("JP", "Japan",                 36.2048,   138.2529),
    ("CN", "China",                 35.8617,   104.1954),
    ("KR", "South Korea",           35.9078,   127.7669),
    ("SG", "Singapore",              1.3521,   103.8198),
    ("BR", "Brazil",               -14.2350,   -51.9253),
    ("IL", "Israel",                31.0461,    34.8516),
    ("NL", "Netherlands",           52.1326,     5.2913),
    ("SE", "Sweden",                60.1282,    18.6435),
    ("ID", "Indonesia",             -0.7893,   113.9213),
    ("VN", "Vietnam",               14.0583,   108.2772),
    ("AE", "United Arab Emirates",  23.4241,    53.8478),
    ("NZ", "New Zealand",          -40.9006,   174.8860),
    ("MX", "Mexico",                23.6345,  -102.5528),
    ("AR", "Argentina",            -38.4161,   -63.6167),
    ("ZA", "South Africa",         -30.5595,    22.9375),
    ("KE", "Kenya",                 -0.0236,    37.9062),
    ("EG", "Egypt",                 26.8206,    30.8025),
    ("NG", "Nigeria",                9.0820,     8.6753),
    ("ES", "Spain",                 40.4637,    -3.7492),
    ("IT", "Italy",                 41.8719,    12.5674),
    ("PL", "Poland",                51.9194,    19.1451),
    ("IE", "Ireland",               53.4129,    -8.2439),
    ("CH", "Switzerland",           46.8182,     8.2275),
    ("TR", "Turkey",                38.9637,    35.2433),
    ("PH", "Philippines",           12.8797,   121.7740),
    ("CL", "Chile",                -35.6751,   -71.5430),
    ("CO", "Colombia",               4.5709,   -74.2973),
    ("RU", "Russia",                61.5240,   105.3188),
    ("UA", "Ukraine",               48.3794,    31.1656),
    ("FI", "Finland",               61.9241,    25.7482),
    ("DK", "Denmark",               56.2639,     9.5018),
    ("NO", "Norway",                60.4720,     8.4689),
    ("PT", "Portugal",              39.3999,    -8.2245),
    ("GR", "Greece",                39.0742,    21.8243),
    ("SA", "Saudi Arabia",          23.8859,    45.0792),
]


def main() -> None:
    db = SessionLocal()
    try:
        log.info(f"Upserting {len(COUNTRIES)} countries...")
        for code, name, lat, lon in COUNTRIES:
            existing = db.execute(
                select(Country).where(Country.code == code)
            ).scalar_one_or_none()
            if existing:
                existing.name = name
                existing.latitude = lat
                existing.longitude = lon
            else:
                db.add(Country(code=code, name=name, latitude=lat, longitude=lon))
        db.commit()
        log.info("Done.")
    finally:
        db.close()


if __name__ == "__main__":
    main()