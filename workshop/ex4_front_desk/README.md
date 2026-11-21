# Exercise 4 (capstone): The front desk

**Goal:** build TripMate's front desk yourself: a concierge that greets travellers, answers quick questions and routes the rest to the right specialist, while trip planning keeps all its guarantees.

**New idea:** an `Agent` with `sub_agents=[...]` reads each sub-agent's `description` and hands the conversation to the best one. A description is to an agent what a docstring is to a tool.

**Time:** 14 minutes (9 to build, 5 for the acceptance tests)

This time there are no TODOs. You know every pattern you need, and `CHEATSHEET.md` in the repo root has them all. If `trip_planner` isn't working after 3 minutes, open hint 1 in [HINTS.md](HINTS.md) and paste it: it's Exercise 3 again, and the new part is the front desk.

## The brief

TripMate is growing. Travellers don't only want trip plans: they ask where to eat and how to get around. Build a concierge that greets them, answers quick questions itself and sends the rest to the right specialist. Trip planning must keep its guarantees from Exercises 2 and 3.

## Target architecture

```
concierge  (Agent with sub_agents: answers quick questions, routes the rest)
 ├─ trip_planner   (the Ex 3 SequentialAgent, unchanged + a description)
 │    ├─ local_insider   → state["local_notes"]
 │    └─ planner_agent   + budget callback (Ex 2) → state["budget_eur"], ["nights"]
 ├─ food_guide      get_restaurants + reads {local_notes?} {budget_eur?}
 └─ getting_around  (level 2) get_transport + reads {local_notes?}
```

## What's ready for you

| File | What's in it |
|---|---|
| `tools.py` | Every tool from Exercise 3, plus `get_restaurants` and `get_transport` |
| `budget.py` | The budget rule from Exercise 2 |
| `agent.py` | The imports, and a commented outline of each agent in the architecture |

## What you build

| Agent | What it does | Needs |
|---|---|---|
| `trip_planner` | Plans the whole trip: local notes first, then flights, a hotel within budget and a day-by-day plan. | A `SequentialAgent` of `local_insider` (with `output_key`) and `planner_agent` (with the budget rule from `budget.py`), plus a `description` |
| `food_guide` | Recommends places to eat. Skips anything the local notes say is closed, and keeps prices sensible for the budget. | `get_restaurants`; reads `{local_notes?}`, `{budget_eur?}` and `{nights?}` |
| `getting_around` (level 2) | Explains how to get around. Warns about strikes or closures in the local notes and offers alternatives. | `get_transport`; reads `{local_notes?}` |
| `concierge` (your `root_agent`) | Greets travellers and answers quick general questions itself, like simple phrases in the local language. Hands trip planning, food and transport to the right specialist. | `sub_agents=[trip_planner, food_guide, ...]` |

Every specialist needs a clear `description`, because that's what the concierge reads to decide who to call.

## Levels

- **Level 1 (everyone):** `food_guide` and the `concierge`. Passes tests 1–4.
- **Level 2:** add `getting_around`. Passes test 5.
- **Extras, if you're flying:**
  - **A `budget_tracker`** that answers "How much of my €600 is left?". Do the sums in a Python tool that reads state, not in the model. Hint: state only has the budget and nights so far, so you'll need to save the chosen flight and hotel somewhere first.
  - **Your own specialist:** a weather guide or a packing list, with a mock tool you write.
  - **A guardrail from the cheat sheet:** for example, a `before_model_callback` on the concierge that blocks card numbers.

Then restart `adk web workshop` and pick `ex4_front_desk`.

## Acceptance tests

Run them in order, in one session.

| # | Traveller says | Should be answered by | Passes if |
|---|---|---|---|
| 1 | "Hi! What can you help me with?" | concierge | It introduces the specialists |
| 2 | The golden prompt | trip_planner | Within budget, and avoids closures and red flags |
| 3 | "How do I say thank you in Catalan?" | concierge itself | "Gràcies!", with no hand-off and no new itinerary |
| 4 | "Where should we eat on day 5? Nothing fancy." | food_guide | Affordable, and not the Boqueria (closed that day) |
| 5 (level 2) | "How do we get around on day 4?" | getting_around | It mentions the metro strike and suggests bikes or walking |

Golden prompt:

> I'm flying from Amsterdam to Barcelona for 4 nights. My total budget is €600. I love the beach and I want to stay close by! Plan my trip with flights, a hotel and a day-by-day plan.

Use the **Traces** tab to see which agent answered each message.

## Tips

- `{local_notes?}` with a question mark means "empty if it isn't in state yet", instead of an error. Use it in specialists that might run before the trip is planned.
- Until `agent.py` defines `root_agent`, `adk web` shows no reply and no error. That's expected while you build.
- If a question goes to the wrong specialist, improve the descriptions first.
- An agent can have only one parent, so use `trip_planner` in one place only: your concierge's `sub_agents`. If you see an "already has a parent" error, check that no other agent also lists it.
- After test 4, the next message starts at `food_guide`, which hands off to `getting_around`. That's normal: in ADK the next turn starts at the last agent that replied, if it can hand off.

## Discuss

- Where does the model have freedom now, and where does it have none?
- When would you use `sub_agents` routing, and when a `SequentialAgent`?

Stuck? Open [HINTS.md](HINTS.md) first: it has three hints, and you open only the ones you need. The full answer is in `solutions/ex4_front_desk/agent.py`.
