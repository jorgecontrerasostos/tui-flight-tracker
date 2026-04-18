from fli.models import Airport


def get_airports() -> list[tuple[str, str]]:
    return [(f"{airport.name} - {airport.value}", airport.name) for airport in Airport]


def get_airport() -> list[str]:
    return [f"{airport.name} - {airport.value}" for airport in Airport]


def validate_date():
    pass
