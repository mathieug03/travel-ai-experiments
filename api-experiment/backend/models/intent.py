from __future__ import annotations

from pydantic import BaseModel
from datetime import date


class TravelIntent(BaseModel):
    origin: str | None = None
    destination: str | None = None
    departure_date: date | None = None
    return_date: date | None = None
    duration_days: int | None = None
    flexibility: str = "exact"  # "exact" | "flexible_few_days" | "flexible_week" | "anytime"
    travelers: int = 1
    budget: str | None = None  # "pas cher", "modéré", "pas de limite"
    preferences: list[str] = []  # ["train_only", "no_fly", "direct", "overnight"]
    purpose: str | None = None  # "city break", "road trip", "nature"
    raw_query: str = ""
