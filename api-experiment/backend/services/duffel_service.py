from __future__ import annotations

import httpx
from datetime import date, datetime
from geopy.geocoders import Nominatim

from backend.config import get_settings
from backend.models.transport import TransportOption

DUFFEL_BASE_URL = "https://api.duffel.com"


class DuffelService:
    def __init__(self):
        settings = get_settings()
        self.access_token = settings.duffel_access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Duffel-Version": "v2",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self._geocoder = Nominatim(user_agent="travel-ai")

    async def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: date,
        passengers: int = 1,
        cabin_class: str = "economy",
        max_connections: int | None = None,
    ) -> list[TransportOption]:
        """Search for flights via Duffel REST API.

        Args:
            origin: IATA airport/city code (e.g. "CDG", "PAR")
            destination: IATA airport/city code (e.g. "BCN")
            departure_date: Date of departure
            passengers: Number of adult passengers
            cabin_class: "economy", "premium_economy", "business", "first"
            max_connections: Max number of stops (0 = direct only)
        """
        payload = {
            "data": {
                "slices": [
                    {
                        "origin": origin,
                        "destination": destination,
                        "departure_date": departure_date.isoformat(),
                    }
                ],
                "passengers": [{"type": "adult"}] * passengers,
                "cabin_class": cabin_class,
            }
        }
        if max_connections is not None:
            payload["data"]["max_connections"] = max_connections

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{DUFFEL_BASE_URL}/air/offer_requests",
                headers=self.headers,
                json=payload,
                params={"return_offers": "true"},
            )
            resp.raise_for_status()
            data = resp.json()["data"]

        options: list[TransportOption] = []
        for offer in data.get("offers", []):
            slice_data = offer["slices"][0]
            segments = slice_data["segments"]
            first_seg = segments[0]
            last_seg = segments[-1]

            dep = datetime.fromisoformat(first_seg["departing_at"])
            arr = datetime.fromisoformat(last_seg["arriving_at"])
            duration_minutes = int((arr - dep).total_seconds() / 60)

            provider = (
                first_seg.get("operating_carrier", {}).get("name")
                or first_seg.get("marketing_carrier", {}).get("name")
                or "Unknown"
            )

            options.append(
                TransportOption(
                    mode="flight",
                    provider=provider,
                    origin_station=first_seg["origin"]["iata_code"],
                    destination_station=last_seg["destination"]["iata_code"],
                    departure=dep,
                    arrival=arr,
                    duration_minutes=duration_minutes,
                    price_eur=float(offer["total_amount"])
                    if offer.get("total_currency") == "EUR"
                    else None,
                    price_estimated=offer.get("total_currency") != "EUR",
                    co2_grams=0,  # Enriched by carbon_service
                    transfers=len(segments) - 1,
                    booking_url="",
                    data_source="duffel",
                )
            )

        options.sort(key=lambda o: o.price_eur or float("inf"))
        return options

    def _geocode_city(self, city: str) -> tuple[float, float] | None:
        """Geocode a city name to (latitude, longitude)."""
        location = self._geocoder.geocode(city)
        if location:
            return (location.latitude, location.longitude)
        return None

    async def search_stays(
        self,
        city: str,
        check_in: date,
        check_out: date,
        guests: int = 1,
        rooms: int = 1,
        radius_km: int = 5,
    ) -> list[dict]:
        """Search for accommodations via Duffel Stays REST API."""
        coords = self._geocode_city(city)
        if not coords:
            return []

        payload = {
            "data": {
                "rooms": rooms,
                "location": {
                    "geographic_coordinates": {
                        "latitude": coords[0],
                        "longitude": coords[1],
                    },
                    "radius": radius_km,
                },
                "check_in_date": check_in.isoformat(),
                "check_out_date": check_out.isoformat(),
                "guests": [{"type": "adult"}] * guests,
            }
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{DUFFEL_BASE_URL}/stays/search",
                headers=self.headers,
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()["data"]

        stays = []
        for result in data.get("results", []):
            accommodation = result.get("accommodation", {})
            stays.append(
                {
                    "name": accommodation.get("name", "Unknown"),
                    "rating": accommodation.get("rating"),
                    "review_score": accommodation.get("review_score"),
                    "price_eur": float(result["cheapest_rate_total_amount"])
                    if result.get("cheapest_rate_currency") == "EUR"
                    else None,
                    "currency": result.get("cheapest_rate_currency"),
                    "photos": [
                        p.get("url") for p in accommodation.get("photos", [])[:3]
                    ],
                    "booking_url": "",
                }
            )

        stays.sort(key=lambda s: s.get("price_eur") or float("inf"))
        return stays
