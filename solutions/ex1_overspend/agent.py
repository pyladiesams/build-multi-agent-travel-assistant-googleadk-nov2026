from google.adk.agents import Agent

from .tools import search_flights, search_hotels

root_agent = Agent(
    name="tripmate",
    model="gemini-3.5-flash-lite",
    instruction="""You are TripMate, a friendly travel assistant.
Use the tools to find flights and hotels, then suggest a trip
with a day-by-day plan. Stay within the traveller's budget.""",
    tools=[search_flights, search_hotels],
)
