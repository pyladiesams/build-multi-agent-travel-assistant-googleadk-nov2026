"""The budget rule from Exercise 2. Nothing to change here."""

from google.adk.tools.tool_context import ToolContext

from .tools import real_cost_per_night

# Hotels may use at most 80% of the total budget, which leaves room for the flight.
HOTEL_SHARE = 0.8


def save_trip_details(nights: int, budget_eur: int, tool_context: ToolContext) -> dict:
    """Saves the trip length and total budget. Call this before searching for hotels.

    Args:
        nights: How many nights the traveller is staying.
        budget_eur: The traveller's total budget for the whole trip, in euros.
    """
    tool_context.state["nights"] = nights
    tool_context.state["budget_eur"] = budget_eur
    return {"status": "saved"}


def enforce_budget(tool, args, tool_context, tool_response):
    """Runs after every tool call. Hides hotels the traveller can't afford,
    in search results and in hotel details.

    It checks the real cost from our data, not the prices the model saw.

    Returning None keeps the tool's result as it is.
    Returning a dict replaces what the model sees.
    """
    hotel_tools = ("search_hotels", "get_hotel_details")
    if tool.name not in hotel_tools or tool_response.get("status") != "success":
        return None  # leave other tools, and errors, alone

    budget = tool_context.state.get("budget_eur")
    nights = tool_context.state.get("nights")
    if not budget or not nights:
        return {
            "status": "error",
            "message": "Ask for the budget and number of nights, "
            "then call save_trip_details.",
        }

    max_per_night = budget * HOTEL_SHARE / nights

    # get_hotel_details can reach the same data, so it needs the same rule.
    if tool.name == "get_hotel_details":
        if real_cost_per_night(tool_response["hotel"]["name"]) > max_per_night:
            return {"status": "error", "message": "This hotel is over the budget."}
        return None

    affordable = [
        h
        for h in tool_response["hotels"]
        if real_cost_per_night(h["name"]) <= max_per_night
    ]

    # Add the real nightly cost, so the model's sums include the fees.
    affordable = [
        {**h, "real_cost_per_night": real_cost_per_night(h["name"])}
        for h in affordable
    ]

    return {
        "status": "success",
        "hotels": affordable,
        "note": f"Only hotels up to €{max_per_night:.0f}/night incl. fees are shown. "
        "Use real_cost_per_night for totals: it includes the fees.",
    }
