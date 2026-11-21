from google.adk.agents import Agent, SequentialAgent

from .budget import enforce_budget, save_trip_details
from .tools import get_hotel_details, get_local_notes, search_flights, search_hotels

# TODO 1: create local_insider, a second Agent with one small job: read the
# local notes for the destination and pass them on to the planner.
#
# You've built an Agent before, and planner_agent below is one to copy from.
# Give local_insider:
#   - the name "local_insider" and the same model as planner_agent
#   - a description: one sentence saying what it knows about
#   - an instruction for its job. It only sees the traveller's message, so
#     tell it to find the destination there and look up its local notes.
#     Keep its reply short: the planner reads it, not the traveller.
#   - one tool: get_local_notes. It's the only tool this agent needs.
#
# One new idea: output_key. It saves the agent's final reply into state.
# For example, a weather agent with
#
#     output_key="forecast"
#
# that replies "Sunny, 24°C" leaves state["forecast"] = "Sunny, 24°C" for the
# next agent to read.
#
# Give local_insider output_key="local_notes". The planner reads the notes by
# that exact name in TODO 3.

# This is TripMate from Exercise 2, now called planner_agent.
planner_agent = Agent(
    name="planner_agent",
    model="gemini-3.5-flash-lite",
    description="Plans trips: flights, a hotel within budget, and a day-by-day plan.",
    instruction="""You are TripMate, a friendly travel assistant.
Use the tools to find flights and hotels, then suggest a trip
with a day-by-day plan. Stay within the traveller's budget.""",
    # TODO 3 (do TODO 2 at the bottom of the file first): put the local notes
    # in the planner's instruction.
    #
    # A key in curly brackets inside an instruction is replaced with that value
    # from state, every time the agent runs. Back to the weather agent: a
    # packing agent after it could have
    #
    #     instruction="""Suggest what to pack. Today's forecast: {forecast}"""
    #
    # and it would see "Today's forecast: Sunny, 24°C".
    #
    # Add two things to the instruction above:
    #   - the notes local_insider saved, using its output_key in curly brackets
    #   - one sentence telling the planner what to do with them. A beach day
    #     with a jellyfish warning is the kind of plan you want to stop.
    tools=[search_flights, search_hotels, get_hotel_details, save_trip_details],
    after_tool_callback=enforce_budget,
)

# TODO 2: make root_agent a SequentialAgent named "tripmate" that runs
# local_insider, then planner_agent. It runs them in the order of the list,
# every time:
#     SequentialAgent(name=..., sub_agents=[...])
#
# Then restart and send the golden prompt. In the Traces tab, local_insider
# runs first, and the State tab has local_notes. Check the plan against the
# notes: the planner may glimpse them in the chat history, but nothing in its
# instruction tells it to follow them. TODO 3, in planner_agent above, does.
root_agent = planner_agent
