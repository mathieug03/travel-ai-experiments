"""Local checks; all provider HTTP traffic is intercepted by MockTransport."""
import unittest
from datetime import date
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

from backend.main import app
from backend.services.carbon_service import compare_carbon
from backend.services.duffel_service import DuffelService


class CarbonTests(unittest.TestCase):
    def test_unknown_city_returns_no_estimate(self):
        self.assertIsNone(compare_carbon("Unknown place", "Paris"))

    def test_public_endpoint_and_units(self):
        response = TestClient(app).get(
            "/api/carbon/compare", params={"origin": "Paris", "destination": "London"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(data["distance_km"], 300)
        self.assertLess(data["distance_km"], 400)
        self.assertGreater(data["flight_co2_grams"], data["train_co2_grams"])
        self.assertEqual(data["savings_grams"], data["flight_co2_grams"] - data["train_co2_grams"])


def offer(amount, currency="EUR", stops=0):
    segments = []
    for i in range(stops + 1):
        segments.append({
            "departing_at": f"2030-06-01T{10+i:02}:00:00",
            "arriving_at": f"2030-06-01T{11+i:02}:00:00",
            "origin": {"iata_code": "CDG" if i == 0 else "AMS"},
            "destination": {"iata_code": "LHR" if i == stops else "AMS"},
            "operating_carrier": {"name": "Example Air"},
        })
    return {"total_amount": str(amount), "total_currency": currency, "slices": [{"segments": segments}]}


class FlightTests(unittest.IsolatedAsyncioTestCase):
    async def test_normalization_preserves_stops_duration_and_unknown_currency(self):
        requests = []

        def handler(request):
            requests.append(request)
            return httpx.Response(200, json={"data": {"offers": [
                offer(250), offer(80, "USD"), offer(100, stops=1)
            ]}})

        client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        with patch("backend.services.duffel_service.httpx.AsyncClient", return_value=client):
            options = await DuffelService().search_flights("CDG", "LHR", date(2030, 6, 1))
        self.assertEqual(len(requests), 1)
        self.assertEqual([o.price_eur for o in options], [100, 250, None])
        self.assertEqual(options[0].transfers, 1)
        self.assertEqual(options[0].duration_minutes, 120)
        self.assertEqual(options[0].origin_station, "CDG")
        self.assertEqual(options[0].destination_station, "LHR")
        self.assertTrue(options[-1].price_estimated)
        self.assertEqual(options[-1].data_source, "duffel")

    async def test_provider_error_is_not_returned_as_fake_inventory(self):
        client = httpx.AsyncClient(transport=httpx.MockTransport(
            lambda request: httpx.Response(401, json={"errors": [{"message": "Unauthorized"}]})
        ))
        with patch("backend.services.duffel_service.httpx.AsyncClient", return_value=client):
            with self.assertRaises(httpx.HTTPStatusError):
                await DuffelService().search_flights("CDG", "LHR", date(2030, 6, 1))


if __name__ == "__main__":
    unittest.main()
