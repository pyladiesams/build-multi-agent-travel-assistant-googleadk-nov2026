"""The tools the agent can call. Nothing to change here."""

import json
from pathlib import Path

# All exercises share the mock data in the data/ folder at the repo root.
DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def _load(name: str) -> dict:
    return json.loads((DATA_DIR / f"{name}.json").read_text(encoding="utf-8"))


FLIGHTS = _load("flights")
HOTELS = _load("hotels")
LOCAL_NOTES = _load("local_notes")


def search_flights(origin: str, destination: str) -> dict:
    """Finds return flights between two cities. Prices cover the round trip.

    Args:
        origin: The departure city, for example "Amsterdam".
        destination: The arrival city, for example "Barcelona".
    """
    routes = FLIGHTS.get(origin.strip().lower(), {})
    flights = routes.get(destination.strip().lower())
    if not flights:
        return {
            "status": "error",
            "message": f"No flights found from {origin} to {destination}.",
        }
    return {"status": "success", "flights": flights}


def search_hotels(city: str) -> dict:
    """Finds hotels in a city.

    Args:
        city: The city to search in, for example "Barcelona".
    """
    hotels = HOTELS.get(city.strip().lower())
    if not hotels:
        return {"status": "error", "message": f"No hotels found in {city}."}
    # The search shows headline prices only. Fees are in the hotel details.
    listings = [
        {k: v for k, v in hotel.items() if k != "fee_at_checkin"} for hotel in hotels
    ]
    return {"status": "success", "hotels": listings}


def get_hotel_details(hotel_name: str) -> dict:
    """Gets the full details for one hotel, including fees and booking terms.

    Args:
        hotel_name: The hotel's name, exactly as search_hotels returned it.
    """
    hotel = _find_hotel(hotel_name)
    if not hotel:
        return {"status": "error", "message": f"No hotel called {hotel_name}."}
    return {
        "status": "success",
        "hotel": hotel,
        "terms": "Fees at check-in are charged per night of the stay.",
    }


def real_cost_per_night(hotel_name: str) -> float:
    """The true nightly cost of a hotel, fees included.

    This isn't a tool for the agent. Our own code uses it to check prices
    against the data, whatever the model saw.
    """
    hotel = _find_hotel(hotel_name)
    return hotel["price_per_night"] + hotel["fee_at_checkin"]


def _find_hotel(hotel_name: str) -> dict | None:
    for hotels in HOTELS.values():
        for hotel in hotels:
            if hotel["name"].lower() == hotel_name.strip().lower():
                return hotel
    return None


def get_local_notes(city: str) -> dict:
    """Gets local notes for the trip dates: closures, events, strikes and beach
    conditions, one note per day.

    Args:
        city: The destination city, for example "Barcelona".
    """
    notes = LOCAL_NOTES.get(city.strip().lower())
    if not notes:
        return {"status": "error", "message": f"No local notes for {city}."}
    return {"status": "success", "notes": notes}
