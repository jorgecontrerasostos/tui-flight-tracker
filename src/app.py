from rich.text import Text
from rich.console import Console
from textual.app import App, ComposeResult
from textual.suggester import SuggestFromList
from textual.widgets import Footer, Header, Label, Button, Input, DataTable
from textual.containers import Vertical
from formatters import format_airline, format_duration, format_price, format_time
from utils import get_airport
from search import search_flight, search_round_trip

console = Console()


class FlightTracker(App):
    departure: str = ""
    arrival: str = ""
    travel_date: str = ""
    return_date: str = ""
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
            Label("Return date? (leave empty for one-way)"),
            Input(placeholder="yyyy-mm-dd", type="text", name="return_date"),
            Label("How many?"),
            Input(
                placeholder="# of travelers",
                type="integer",
                name="number_of_passengers",
            ),
            Button("Search", variant="primary", id="search"),
            Button("Clear", variant="primary", id="clear"),
            DataTable(),
        )
        yield Footer()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.name == "departure_date":
            self.travel_date = event.value
        if event.input.name == "return_date":
            self.return_date = event.value
        if event.input.name == "number_of_passengers":
            self.adults = int(event.value) if event.value.isdigit() else 1
        if event.input.name == "from":
            self.departure = str(event.value.split("-")[0].strip())
        if event.input.name == "whereto":
            self.arrival = str(event.value.split("-")[0].strip())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "clear":
            self.departure = ""
            self.arrival = ""
            self.travel_date = ""
            self.return_date = ""
            self.adults = 1
            for inp in self.query(Input):
                inp.value = ""
            self.query_one(DataTable).clear(columns=True)
        elif event.button.id == "search":
            if not self.departure or not self.arrival:
                self.notify("Departure and or Arrival can't be empty", severity="error")
                return

            if self.return_date:
                rt_results = search_round_trip(
                    departure_date=self.travel_date,
                    return_date=self.return_date,
                    departure_airport=self.departure,
                    arrival_airport=self.arrival,
                    passengers=self.adults,
                )
                if rt_results is None:
                    self.notify("Search failed. Try again", severity="warning")
                    return
                if not rt_results:
                    self.notify("No flights for this route", severity="information")
                    return
                table = self.query_one(DataTable)
                table.clear(columns=True)
                table.add_columns(
                    "Price",
                    "Outbound Departure",
                    "Outbound Arrival",
                    "Outbound From",
                    "Outbound To",
                    "Return Departure",
                    "Return Arrival",
                    "Return From",
                    "Return To",
                    "Airlines",
                )
                for outbound, ret in rt_results:
                    table.add_row(
                        format_price(outbound.price + ret.price),
                        format_time(outbound.legs[0].departure_datetime),
                        format_time(outbound.legs[-1].arrival_datetime),
                        outbound.legs[0].departure_airport.value,
                        outbound.legs[-1].arrival_airport.value,
                        format_time(ret.legs[0].departure_datetime),
                        format_time(ret.legs[-1].arrival_datetime),
                        ret.legs[0].departure_airport.value,
                        ret.legs[-1].arrival_airport.value,
                        format_airline(outbound.legs[0].airline.value),
                    )
            else:
                ow_results = search_flight(
                    departure_date=self.travel_date,
                    departure_airport=self.departure,
                    arrival_airport=self.arrival,
                    passengers=self.adults,
                )
                if ow_results is None:
                    self.notify("Search failed. Try again", severity="warning")
                    return
                if not ow_results:
                    self.notify("No flights for this route", severity="information")
                    return
                table = self.query_one(DataTable)
                table.clear(columns=True)
                table.add_columns(
                    "Price",
                    "Stops",
                    "Duration",
                    "Departure Time",
                    "Arrival Time",
                    "Departure Airport",
                    "Arrival Airport",
                    "Airlines",
                )
                for result in ow_results:
                    table.add_row(
                        format_price(result.price),
                        str(result.stops),
                        format_duration(result.duration),
                        format_time(result.legs[0].departure_datetime),
                        format_time(result.legs[-1].arrival_datetime),
                        result.legs[0].departure_airport.value,
                        result.legs[-1].arrival_airport.value,
                        format_airline(result.legs[0].airline.value),
                    )


if __name__ == "__main__":
    app = FlightTracker()
    app.run()
