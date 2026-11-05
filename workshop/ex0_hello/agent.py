"""Smoke test: if this agent says hi back, your setup works."""

from google.adk.agents import Agent

root_agent = Agent(
    name="hello",
    model="gemini-3.5-flash-lite",
    instruction="Greet the traveller in one short, friendly sentence.",
)
