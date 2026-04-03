# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python TUI application for searching Google Flights data using the `fli` (flights) library. Currently scaffolded — `src/main.py` contains a working `main()` that runs a hardcoded flight search, and a skeleton `FlightTracker` Textual app that currently just renders a header/footer.

## Commands

```bash
# Install dependencies
uv sync

# Run the application
uv run python src/main.py

# Run a specific test
uv run pytest tests/path/to/test_file.py::test_name -v

# Run all tests
uv run pytest

# Lint and format
uv run ruff check src/
uv run ruff format src/
```

## Architecture

`src/main.py` is the only source file. It contains two parallel execution paths:

1. **`main()`** — runs a hardcoded flight search (MTY → BOS, 2026-06-06, 1 adult) using `fli.search.SearchFlights` and prints results via `rich`. This is currently commented out in `__main__`.
2. **`FlightTracker(App)`** — a Textual app stub (just Header + Footer). This is what runs when you execute the file.

The intended direction is to wire `search_flight()` (currently empty) into the Textual UI, replacing the hardcoded search in `main()`.

### `fli` Library Key Imports

- `fli.search.SearchFlights` — executes the search
- `fli.models.FlightSearchFilters` — top-level search config (passengers + segments)
- `fli.models.FlightSegment` — one leg of the trip (departure/arrival airports + date)
- `fli.models.Airport` — enum of airport codes
- `fli.models.PassengerInfo` — passenger counts

## Key Dependencies

| Package | Role |
|---|---|
| `flights` (`fli`) | Core flight search and data models |
| `textual` | TUI framework |
| `rich` | Styled terminal output |
| `pandas` | Data manipulation (available, not yet used) |

## Python Version

3.12.12 (enforced via `.python-version`)
