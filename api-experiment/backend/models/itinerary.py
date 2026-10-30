from __future__ import annotations

from pydantic import BaseModel
from datetime import date
from .transport import TransportOption


class Activity(BaseModel):
    name: str
    description: str
    duration_hours: float | None = None
    booking_url: str = ""


class Accommodation(BaseModel):
    name: str
    price_eur: float | None = None
    booking_url: str = ""


class ItineraryDay(BaseModel):
    day_number: int
    date: date
    city: str
    transport: TransportOption | None = None
    accommodation: Accommodation | None = None
    activities: list[Activity] = []
    tips: list[str] = []


class Itinerary(BaseModel):
    title: str
    summary: str  # Brief éditorial
    total_co2_grams: int
    co2_vs_flight_savings: int
    co2_equivalence: str  # "Équivalent à 3 arbres plantés"
    total_price_estimate: float
    days: list[ItineraryDay]
    transport_options_considered: list[TransportOption] = []
