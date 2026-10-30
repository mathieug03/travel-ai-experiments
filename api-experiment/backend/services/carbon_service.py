from __future__ import annotations

import json
from pathlib import Path
from geopy.distance import geodesic

# Major European city coordinates for distance calculation
CITY_COORDS: dict[str, tuple[float, float]] = {
    "Paris": (48.8566, 2.3522),
    "London": (51.5074, -0.1278),
    "Amsterdam": (52.3676, 4.9041),
    "Brussels": (50.8503, 4.3517),
    "Berlin": (52.5200, 13.4050),
    "Munich": (48.1351, 11.5820),
    "Frankfurt": (50.1109, 8.6821),
    "Vienna": (48.2082, 16.3738),
    "Zurich": (47.3769, 8.5417),
    "Milan": (45.4642, 9.1900),
    "Rome": (41.9028, 12.4964),
    "Naples": (40.8518, 14.2681),
    "Venice": (45.4408, 12.3155),
    "Barcelona": (41.3874, 2.1686),
    "Madrid": (40.4168, -3.7038),
    "Prague": (50.0755, 14.4378),
    "Budapest": (47.4979, 19.0402),
    "Lyon": (45.7640, 4.8357),
    "Marseille": (43.2965, 5.3698),
    "Lisbon": (38.7223, -9.1393),
    "Copenhagen": (55.6761, 12.5683),
    "Stockholm": (59.3293, 18.0686),
    "Oslo": (59.9139, 10.7522),
    "Warsaw": (52.2297, 21.0122),
    "Edinburgh": (55.9533, -3.1883),
    "Montreal": (45.46886, -73.730698),
}

DATA_DIR = Path(__file__).parent.parent / "data"


def _load_carbon_factors() -> dict:
    with open(DATA_DIR / "carbon_factors.json") as f:
        return json.load(f)["factors"]


CARBON_FACTORS = _load_carbon_factors()


def get_distance_km(origin: str, destination: str) -> float | None:
    """Calculate distance between two cities in km."""
    origin_coords = CITY_COORDS.get(origin)
    dest_coords = CITY_COORDS.get(destination)
    if not origin_coords or not dest_coords:
        return None
    return geodesic(origin_coords, dest_coords).kilometers


def calculate_co2(mode: str, distance_km: float) -> int:
    """Return gCO2 per passenger for the trip."""
    factor_map = {
        "train": "tgv_electric",
        "flight": "flight_short" if distance_km < 1500 else "flight_medium",
        "bus": "bus",
    }
    factor_key = factor_map.get(mode, "tgv_electric")
    factor = CARBON_FACTORS[factor_key]["g_co2_per_km"]
    return int(distance_km * factor)


def co2_equivalence(grams: int) -> str:
    """Convert grams of CO2 to human-readable equivalences."""
    km_car = grams / 115
    trees = grams / 25000
    streaming_hours = grams / 36
    return f"≈ {int(km_car)} km en voiture, ou {trees:.1f} arbre pendant un an, ou {int(streaming_hours)}h de streaming"


def compare_carbon(origin: str, destination: str) -> dict | None:
    """Compare CO2 emissions between train and flight for a route."""
    distance = get_distance_km(origin, destination)
    if distance is None:
        return None

    train_co2 = calculate_co2("train", distance)
    flight_co2 = calculate_co2("flight", distance)
    savings_grams = flight_co2 - train_co2
    savings_pct = int((savings_grams / flight_co2) * 100) if flight_co2 > 0 else 0

    return {
        "origin": origin,
        "destination": destination,
        "distance_km": round(distance, 1),
        "train_co2_grams": train_co2,
        "flight_co2_grams": flight_co2,
        "savings_grams": savings_grams,
        "savings_pct": savings_pct,
        "train_equivalence": co2_equivalence(train_co2),
        "flight_equivalence": co2_equivalence(flight_co2),
    }
