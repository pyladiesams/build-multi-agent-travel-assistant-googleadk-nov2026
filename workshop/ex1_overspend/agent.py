from google.adk.agents import Agent

from .tools import search_flights, search_hotels

# Example: an agent with one tool. It's about the weather, not travel, so don't
# copy it as is. Notice that get_weather has no brackets: you hand the function to
# the agent, and the model decides when to call it.
#
#     def get_weather(city: str) -> dict:
#         """Gets today's weather for a city."""
#         return {"status": "success", "forecast": "sunny, 24°C"}
#
#     weather_agent = Agent(
#         name="weather_bot",
#         model="gemini-3.5-flash-lite",
#         instruction="You answer questions about the weather. Use the get_weather tool.",
#         tools=[get_weather],
#     )

# TODO: create root_agent, an Agent with:
#   - name: "tripmate"
#   - model: "gemini-3.5-flash-lite"
#   - instruction: describe TripMate, a friendly travel assistant. Tell it to use
#     the tools to find flights and hotels, suggest a trip with a day-by-day plan,
#     and stay within the traveller's budget.
#   - tools: the two functions imported above
#
# The variable must be called root_agent, because that's the name adk web looks for.
