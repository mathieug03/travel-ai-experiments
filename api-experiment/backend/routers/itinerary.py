from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.carbon_service import compare_carbon

router = APIRouter(prefix="/api", tags=["itinerary"])


class CarbonCompareResponse(BaseModel):
    origin: str
    destination: str
    distance_km: float
    train_co2_grams: int
    flight_co2_grams: int
    savings_grams: int
    savings_pct: int
    train_equivalence: str
    flight_equivalence: str


@router.get("/carbon/compare", response_model=CarbonCompareResponse | None)
async def carbon_compare(origin: str, destination: str):
    """Compare CO2 emissions between train and flight for a route."""
    return compare_carbon(origin, destination)
