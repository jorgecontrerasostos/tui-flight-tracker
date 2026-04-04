from fli.search import SearchFlights

from rich.text import Text
from rich.console import Console
from textual.app import App, ComposeResult
from textual.suggester import SuggestFromList
from textual.widgets import Footer, Header, Label, Button, Input, DataTable
from textual.containers import Vertical
from formatters import format_duration, format_price
from utils import get_airport
from search import search_flight

console = Console()


class FlightTracker(App):
    departure: str = ""
    arrival: str = ""
    travel_date: str = ""
    adults: int = 1

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Label(
                Text.assemble(
                    "✈️  Welcome to (A very cool app name goes here)!",
                    "bold green",
                    style="bold",
                )
            ),
            Label(Text("Where are we departing from?")),
            Input(
                suggester=SuggestFromList(
                    get_airport(),
                    case_sensitive=False,
                ),
                name="from",
            ),
            Label("Where are we going?"),
            Input(
                suggester=SuggestFromList(get_airport(), case_sensitive=False),
                name="whereto",
            ),
            Label("When?"),
            Input(placeholder="yyyy-mm-dd", type="text", name="departure_date"),
            Label("How many?"),
            Input(
                placeholder="# of travelers",
                type="integer",
                name="number_of_passengers",
            ),
            Button("Search", variant="primary"),
            DataTable(),
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

        results = search_flight(
            departure_date=self.travel_date,
            departure_airport=self.departure,
            arrival_airport=self.arrival,
            passengers=self.adults
        )
        if results is None:
            self.notify("Search failed. Try again", severity="warning")
            return
        if not results:
            self.notify("No flights for this route", severity="information")
            return

        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.add_columns(
            "Price", "Stops", "Duration", "Departure", "Arrival", "Airlines"
        )

        for result in results:
            table.add_row(
                format_price(result.price),
                str(result.stops),
                format_duration(result.duration),
                result.legs[0].departure_airport,
                result.legs[-1].arrival_airport,
                result.legs[0].airline,
            )


if __name__ == "__main__":
    app = FlightTracker()
    app.run()
