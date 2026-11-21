from google.adk.agents import Agent, SequentialAgent

from .budget import enforce_budget, save_trip_details
from .tools import (
    get_hotel_details,
    get_local_notes,
    get_restaurants,
    get_transport,
    search_flights,
    search_hotels,
)

# Exercise 3's team, with root_agent renamed to trip_planner and a description added.
local_insider = Agent(
    name="local_insider",
    model="gemini-3.5-flash-lite",
    description="Knows local closures, events, strikes and beach conditions.",
    instruction="""Find the destination in the traveller's message and call
get_local_notes for it. Reply with one short line per day.""",
    tools=[get_local_notes],
    output_key="local_notes",
)

planner_agent = Agent(
    name="planner_agent",
    model="gemini-3.5-flash-lite",
    description="Plans trips: flights, a hotel within budget, and a day-by-day plan.",
    instruction="""You are TripMate, a friendly travel assistant.
Use the tools to find flights and hotels, then suggest a trip
with a day-by-day plan. Stay within the traveller's budget.

Local notes for the trip dates:
{local_notes}

Never schedule anything the local notes say is closed or unsafe.""",
    tools=[search_flights, search_hotels, get_hotel_details, save_trip_details],
    after_tool_callback=enforce_budget,
)

trip_planner = SequentialAgent(
    name="trip_planner",
    description="Plans a complete trip: checks local notes, then finds flights "
    "and a hotel within budget and writes a day-by-day plan.",
    sub_agents=[local_insider, planner_agent],
)


food_guide = Agent(
    name="food_guide",
    model="gemini-3.5-flash-lite",
    description="Recommends restaurants and food markets at the destination.",
    instruction="""Recommend places to eat using get_restaurants.
Local notes: {local_notes?}
Total trip budget: {budget_eur?} euros for {nights?} nights.
Skip anything the local notes say is closed, and keep prices sensible.""",
    tools=[get_restaurants],
)

getting_around = Agent(  # level 2
    name="getting_around",
    model="gemini-3.5-flash-lite",
    description="Explains how to get to and around the destination.",
    instruction="""Suggest ways to get around using get_transport.
Local notes: {local_notes?}
Warn about strikes or closures in the local notes and offer alternatives.""",
    tools=[get_transport],
)

root_agent = Agent(
    name="concierge",
    model="gemini-3.5-flash-lite",
    instruction="""You are the front desk of TripMate. Greet travellers and
answer quick general questions yourself (for example, simple phrases
in the local language). Hand trip planning, restaurant tips and
transport advice to the right specialist.""",
    sub_agents=[trip_planner, food_guide, getting_around],
)
