from unittest.mock import MagicMock, patch
from search import search_round_trip


def test_search_round_trip_returns_pairs():
    outbound = MagicMock()
    return_flight = MagicMock()
    pairs = [(outbound, return_flight)]

    with patch("search.SearchFlights") as mock_cls:
        mock_cls.return_value.search.return_value = pairs
        result = search_round_trip(
            departure_date="2026-06-01",
            return_date="2026-06-08",
            departure_airport="MTY",
            arrival_airport="BOS",
            passengers=1,
        )

    assert result == pairs


def test_search_round_trip_returns_none_on_failure():
    with patch("search.SearchFlights") as mock_cls:
        mock_cls.return_value.search.side_effect = Exception("API error")
        result = search_round_trip(
            departure_date="2026-06-01",
            return_date="2026-06-08",
            departure_airport="MTY",
            arrival_airport="BOS",
            passengers=1,
        )

    assert result is None
