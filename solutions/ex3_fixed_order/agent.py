from google.adk.agents import Agent, SequentialAgent

from .budget import enforce_budget, save_trip_details
from .tools import get_hotel_details, get_local_notes, search_flights, search_hotels

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

root_agent = SequentialAgent(
    name="tripmate",
    sub_agents=[local_insider, planner_agent],
)
