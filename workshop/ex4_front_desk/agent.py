"""Exercise 4: build TripMate's front desk from scratch.

The README has the target architecture, what each agent should do, and the
acceptance tests. CHEATSHEET.md in the repo root has every pattern from today.
"""

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

# an agent that knows local closures, events, strikes and beach conditions
# local_insider = Agent(
#     name="local_insider",
# )

# an agent that plans flights, a hotel within budget and a day-by-day plan
# planner_agent = Agent(
#     name="planner_agent",
# )

# a team that always runs local_insider first, then planner_agent
# trip_planner = SequentialAgent(
#     name="trip_planner",
# )

# an agent that guides travellers through the food scene
# food_guide = Agent(
#     name="food_guide",
# )

# level 2: an agent that explains how to get around
# getting_around = Agent(
#     name="getting_around",
# )

# the front desk: answers quick questions itself and routes the rest
# root_agent = Agent(
#     name="concierge",
# )
