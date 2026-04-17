
from utils import get_airports
from fli.models import Airport

def test_get_airports():
    airports = get_airports()
    assert len(airports) == len(Airport)
    assert all(" - " in item[0] for item in airports)
