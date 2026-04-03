from os import name
from fli.search import SearchFlights
from fli.models import FlightSearchFilters, FlightSegment, Airport, PassengerInfo
from rich import print
from rich.jupyter import display
from rich.text import Text
from rich.console import Console
from textual.app import App, ComposeResult
from textual.suggester import SuggestFromList
from textual.widgets import Footer, Header, Label, Select, Button, Input, DataTable
from textual.containers import Vertical

console = Console()

def get_airports() -> list[tuple[str, str]]:
    return [(f"{airport.name} - {airport.value}", airport.name) for airport in Airport]

def get_airport() -> list[str]:
    return [f"{airport.name} - {airport.value}"for airport in Airport]

def validate_date():
    pass

def format_duration(duration: int) -> str:
    hours = duration // 60
    minutes = duration % 60
    if duration < 60:
        return f"{duration}m"
    if duration == 60:
        return f"{hours}h"
    return f"{hours}h {minutes}m"

def format_price(price: float) -> str:
    return f"${price:,.2f} MXN"


class FlightTracker(App):
    departure: str = ""
    arrival: str = ""
    travel_date: str = ""
    adults: int = 1

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Label(
                Text.assemble("✈️  Welcome to (A very cool app name goes here)!", "bold green", style="bold")
            ),
            Label(Text("Where are we departing from?")),
            Input(suggester=SuggestFromList(get_airport(), case_sensitive=False,), name="from"),
            Label("Where are we going?"),
            Input(suggester=SuggestFromList(get_airport(), case_sensitive=False), name="whereto"),
            Label("When?"),
            Input(placeholder="yyyy-mm-dd", type="text", name="departure_date"),
            Label("How many?"),
            Input(placeholder="# of travelers", type="integer", name="number_of_passengers"),
            Button("Search", variant="primary"),
            DataTable()
        )
        yield Footer()


    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.name == "departure_date":
            self.travel_date = event.value
        if event.input.name == "number_of_passengers":
            self.adults = int(event.value) if event.value.isdigit() else 1
        if event.input.name == "from":
            self.departure = str(event.value.split("-")[0].strip())
        if event.input.name == "whereto":
            self.arrival = str(event.value.split("-")[0].strip())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if not self.departure or not self.arrival:
            self.notify("Departure and or Arrival can't be empty", severity="error")
            return

        departure = Airport[self.departure]
        arrival = Airport[self.arrival]

        search = SearchFlights()
        filters = FlightSearchFilters(
            passenger_info=PassengerInfo(adults=self.adults),
            flight_segments=[
                FlightSegment(
                    departure_airport=[[departure, 0]],
                    arrival_airport=[[arrival, 0]],
                    travel_date=self.travel_date,
                )
            ],
        )
        results = search.search(filters)

        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.add_columns("Price", "Stops", "Duration", "Departure", "Arrival", "Airlines")

        for result in results:
            table.add_row(
                format_price(result.price),
                str(result.stops),
                format_duration(result.duration),
                result.legs[0].departure_airport,
                result.legs[-1].arrival_airport,
                result.legs[0].airline,
            )


def main():
    pass


if __name__ == "__main__":
    main()
    app = FlightTracker()
    app.run()
