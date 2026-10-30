from fastapi import APIRouter, Depends, Query
from datetime import date

from backend.models.transport import TransportOption
from backend.services.duffel_service import DuffelService
from backend.services.carbon_service import calculate_co2, get_distance_km

router = APIRouter(prefix="/api/search", tags=["search"])


def get_duffel() -> DuffelService:
    return DuffelService()


@router.get("/transport", response_model=list[TransportOption])
async def search_transport(
    origin: str = Query(..., description="Origin city or IATA code"),
    destination: str = Query(..., description="Destination city or IATA code"),
    date: date = Query(..., description="Departure date (YYYY-MM-DD)"),
    mode: str = Query("all", description="Transport mode: train, flight, all"),
    duffel: DuffelService = Depends(get_duffel),
):
    """Search for transport options (flights + trains) between two cities."""
    results: list[TransportOption] = []

    # Flight search via Duffel
    if mode in ("flight", "all"):
        flights = await duffel.search_flights(origin, destination, date)
        # Enrich with CO2 data
        distance = get_distance_km(origin, destination)
        if distance:
            for flight in flights:
                flight.co2_grams = calculate_co2("flight", distance)
        results.extend(flights)

    # Train search via HAFAS — TODO: implement hafas_service
    if mode in ("train", "all"):
        pass  # Will be added with HAFAS integration

    return results
