# Exercise 1: Build it, watch it overspend

**Goal:** build a working travel agent in about 10 lines, then catch it breaking the budget.

**New idea:** an `Agent` is a model, an instruction and tools. Tools are plain Python functions, and the docstring tells the model what they do.

**Time:** 12 minutes (8 to build, 4 to break it)

## How tools work

You don't call the tools yourself. You give them to the agent, and the model decides when to use them:

1. You list your functions in the agent: `tools=[my_function]`, with no brackets after the name.
2. ADK reads each function's name, type hints and docstring, and describes the tool to the model.
3. When the model wants a tool, it asks for it by name and chooses the arguments, for example `search_hotels(city="Barcelona")`.
4. ADK runs your Python function and sends the returned result back to the model.
5. The model reads the result, then calls another tool or writes its answer.

You can watch all of this happen in the **Events** tab of `adk web`.

## Build (8 min)

`tools.py` is ready. Your work is in `agent.py`, which includes a small example agent to follow.

1. Read `tools.py` to see what the agent will be able to call. The mock data it searches is in `data/` at the repo root.
2. In `agent.py`, create `root_agent` with a name, the model and an instruction describing TripMate.
3. Give it the two tools.
4. From the repo root, run `adk web workshop`, open http://localhost:8000, pick `ex1_overspend` and say hi.

## Break (4 min)

Send this golden prompt:

> I'm flying from Amsterdam to Barcelona for 4 nights. My total budget is €600. I love the beach! Plan my trip with flights, a hotel and a day-by-day plan.

Start a new session and send it again, for 3 runs in total. For each run:

1. Work out the real total: `(price + fees) × nights + flight`.
2. Open the **Events** tab and find the tool results. Were the fees there? Did the agent mention them?
3. Score it: did this run stay within €600?

## Discuss

- We asked it to stay within budget. Why didn't it?
- Would shouting help ("NEVER exceed the budget!!!")? How sure would you be?
- What did it get right?

Stuck? Compare your work with `solutions/ex1_overspend/agent.py`.
