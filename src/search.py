from fli.models import FlightSearchFilters, FlightSegment, Airport, PassengerInfo, FlightResult
from fli.search import SearchFlights

import datetime


def search_flight(
    departure_date: datetime.date,
    departure_airport: str,
    arrival_airport: str,
    passengers: int
) -> list[FlightResult]:
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
        results = search.search(filters)
        return results
