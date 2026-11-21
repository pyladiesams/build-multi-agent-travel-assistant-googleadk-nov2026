# Exercise 3: Why a team? A fixed order

**Goal:** split TripMate into a Local Insider and a planner, and guarantee the insider always runs first.

**New ideas:**
- **`SequentialAgent`** runs its sub-agents in a fixed order, every time. Your code decides the order, not the model.
- **`output_key`** saves an agent's reply into state, the same state as in Exercise 2. Writing `{local_notes}` in another agent's instruction reads it back.

**Time:** 12 minutes (9 to build, 3 to prove it)

## What broke

At the end of Exercise 2, your plan probably walked into the local notes: Sagrada Família is closed on day 2, the beaches have a jellyfish red flag on days 3 and 4, and there's a metro strike on day 4. Giving one agent a local-notes tool doesn't make it use the tool every time.

## Build (9 min)

Your work is in `agent.py`. `tools.py` now has a `get_local_notes` tool, and the budget rule from Exercise 2 has moved to `budget.py`.

1. **TODO 1:** create `local_insider`, a small agent that looks up the local notes and saves its reply into state. Most of it you know from Exercise 1. The new part is `output_key`, and the comment in `agent.py` explains it.
2. **TODO 2** (at the bottom of the file): make `root_agent` a `SequentialAgent` that runs `local_insider`, then `planner_agent`.

   Checkpoint: restart `adk web workshop`, pick `ex3_fixed_order` and send the golden prompt. `local_insider` runs first and `local_notes` is in state. Check the plan against the notes. The planner may glimpse them in the chat history, but nothing in its instruction tells it to follow them yet.
3. **TODO 3** (inside `planner_agent`): put the notes into the planner's instruction, and add a rule in your own words for what to do with them. The comment in `agent.py` shows how an instruction reads a value from state.

Then restart `adk web workshop` again.

## Prove (3 min)

Send the golden prompt in 3 new sessions:

> I'm flying from Amsterdam to Barcelona for 4 nights. My total budget is €600. I love the beach and I want to stay close by! Plan my trip with flights, a hotel and a day-by-day plan.

For each run, check:

1. No Sagrada Família on day 2, no beach on days 3 and 4, no metro on day 4.
2. Still within budget.
3. **Traces** tab: does `local_insider` run first every time?
4. **State** tab: is `local_notes` there, next to the budget from Exercise 2?

## Discuss

- Which reason for splitting into agents mattered most here?
- What would happen if you swapped the order in the list?
- The order is guaranteed by code. Is following the local notes guaranteed too?

Stuck? Compare your work with `solutions/ex3_fixed_order/agent.py`.
