from fli.models import Airport

def get_airports() -> list[tuple[str, str]]:
    """
    Returns a list of tuples containing information about airports.

    Each tuple contains the full name of an airport (in the format 'Airport Name - IATA Code')
    and its corresponding IATA code. The data is retrieved from the Airport class.

    :return: A list of tuples, where each tuple contains an airport's full name and IATA code.
    """
    return [(f"{airport.name} - {airport.value}", airport.name) for airport in Airport]


def get_airport() -> list[str]:
    """
    Returns a list of strings containing the names of airports.

    Each string represents an airport's name, with its IATA code appended (e.g. 'New York JFK').
    The data is retrieved from the Airport class.

    :return: A list of strings, where each string contains an airport's name and IATA code.
    """
    return [f"{airport.name} - {airport.value}" for airport in Airport]


def validate_date(date: str):
    """
    This is a docstring.
    :param date:
    :return:
    """
    pass
