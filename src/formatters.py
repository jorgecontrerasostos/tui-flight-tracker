from datetime import datetime

AIRLINES = {
    "Aeroenlaces Nacionales": "Viva Aerobus",
}

def format_duration(duration: int) -> str:
    """Format a duration in minutes into a compact readable string.

    Args:
        duration: Total duration in minutes.

    Returns:
        A human-readable duration string (for example, ``"45m"`` or ``"2h 5m"``).
    """
    hours = duration // 60
    minutes = duration % 60
    if duration < 60:
        return f"{duration}m"
    if duration == 60:
        return f"{hours}h"
    return f"{hours}h {minutes}m"


def format_price(price: float) -> str:
    """Format a numeric fare value in MXN.

    Args:
        price: Ticket price per passenger.

    Returns:
        A currency-formatted string in Mexican pesos.
    """
    return f"${price:,.2f} MXN p/p"

def format_airline(airline_name: str) -> str:
    """Normalize airline names using known display aliases.

    Args:
        airline_name: Airline name returned by the provider.

    Returns:
        A normalized airline name when a mapping exists, otherwise the input name.
    """
    return AIRLINES.get(airline_name, airline_name)

def format_time(dt: datetime) -> str:
    """Format a datetime value as a 24-hour time string.

    Args:
        dt: Datetime object to format.

    Returns:
        Time formatted as ``HH:MM``.
    """
    return dt.strftime("%H:%M")