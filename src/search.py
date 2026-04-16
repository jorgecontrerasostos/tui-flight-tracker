from fli.models import (
    FlightSearchFilters,
    FlightSegment,
    Airport,
    PassengerInfo,
    FlightResult,
)
from fli.search import SearchFlights

import datetime
import logging

logger = logging.getLogger(__name__)


def search_flight(
    departure_date: str,
    departure_airport: str,
    arrival_airport: str,
    passengers: int,
) -> list[FlightResult] | None:
    """Search flights for a one-way route and departure date.

    Args:
        departure_date: Travel date for the outbound segment.
        departure_airport: Departure airport enum key used by ``Airport``.
        arrival_airport: Arrival airport enum key used by ``Airport``.
        passengers: Number of adult passengers.

    Returns:
        A list of matching flight results when the search succeeds, otherwise ``None``.
    """
    departure = Airport[departure_airport]
    arrival = Airport[arrival_airport]

    search = SearchFlights()
    filters = FlightSearchFilters(
        passenger_info=PassengerInfo(adults=passengers),
        flight_segments=[
            FlightSegment(
                departure_airport=[[departure, 0]],
                arrival_airport=[[arrival, 0]],
                travel_date=departure_date,
            )
        ],
    )
    results = None
    try:
        results = search.search(filters)
    except Exception as e:
        logger.error(f"Flight search failed: {e}")
        return None
    return results
