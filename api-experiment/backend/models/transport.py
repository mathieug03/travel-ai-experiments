from __future__ import annotations

from pydantic import BaseModel
from datetime import datetime


class TransportSegment(BaseModel):
    operator: str
    train_number: str | None = None
    origin: str
    destination: str
    departure: datetime
    arrival: datetime


class TransferDetail(BaseModel):
    station: str
    wait_minutes: int
    risk: str = "low"  # "low" | "medium" | "high"


class TransportOption(BaseModel):
    mode: str  # "train" | "flight" | "bus"
    provider: str  # "SNCF", "Ryanair", etc.
    origin_station: str
    destination_station: str
    departure: datetime
    arrival: datetime
    duration_minutes: int
    price_eur: float | None = None
    price_estimated: bool = False
    co2_grams: int = 0
    transfers: int = 0
    transfer_details: list[TransferDetail] = []
    booking_url: str = ""
    segments: list[TransportSegment] = []
    data_source: str  # "duffel" | "hafas" | "estimated"
