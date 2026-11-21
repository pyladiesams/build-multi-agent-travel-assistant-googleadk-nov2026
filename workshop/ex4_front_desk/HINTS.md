# Exercise 4: hints

Three hints, in the order you build. Open only the ones you need. Each one goes into `agent.py`, below the imports.

If the sections don't fold in your editor, read this file on GitHub or in your editor's Markdown preview.

<details>
<summary><b>Hint 1: the trip-planning team (paste this)</b></summary>

This is Exercise 3 again, so there's nothing new to learn by retyping it. The only changes: the `SequentialAgent` is now called `trip_planner` instead of `root_agent`, and it has a `description` for the concierge to read.

```python
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
```

To check it on its own, add `root_agent = trip_planner` as the last line for now, restart, and send the golden prompt. Replace that line when you build the concierge.

</details>

<details>
<summary><b>Hint 2: the food guide (fill in the gaps)</b></summary>

The state lines are done. Write the description and finish the instruction yourself.

```python
food_guide = Agent(
    name="food_guide",
    model="gemini-3.5-flash-lite",
    description="...",  # one sentence: which questions should come here?
    instruction="""...tell it to recommend places to eat using get_restaurants...
Local notes: {local_notes?}
Total trip budget: {budget_eur?} euros for {nights?} nights.
...tell it what to do about closed places and prices...""",
    tools=[get_restaurants],
)
```

The `?` matters. A traveller might ask about food before planning a trip, and then `local_notes` isn't in state yet.

For level 2, `getting_around` has the same shape, with `get_transport` and `{local_notes?}`.

</details>

<details>
<summary><b>Hint 3: the concierge (fill in the gaps)</b></summary>

The concierge has no tools. It has `sub_agents`, and it reads their descriptions to decide who gets each question.

```python
root_agent = Agent(
    name="concierge",
    model="gemini-3.5-flash-lite",
    instruction="""...who is it? What does it answer itself?
What does it hand to a specialist?...""",
    sub_agents=[trip_planner, food_guide],  # add getting_around for level 2
)
```

Two things to check if a test fails:

- **Test 3 hands off or re-plans:** say in the instruction that quick general questions, like a phrase in the local language, are answered by the concierge itself.
- **A question goes to the wrong specialist:** make that specialist's `description` more specific.

</details>
