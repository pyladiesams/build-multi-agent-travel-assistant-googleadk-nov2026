# ADK cheat sheet

Every pattern from today, with a snippet.

## An agent with tools (Exercise 1)

A tool is a plain Python function. The model reads its name, type hints and docstring. Pass the function itself, without brackets.

```python
from google.adk.agents import Agent

def search_hotels(city: str) -> dict:
    """Finds hotels in a city."""
    return {"status": "success", "hotels": [...]}

root_agent = Agent(
    name="tripmate",
    model="gemini-3.5-flash-lite",
    instruction="You are TripMate, a friendly travel assistant.",
    tools=[search_hotels],
)
```

`adk web` looks for a variable called `root_agent` in `agent.py`.

## State (Exercise 2)

State is a notebook the session keeps. Add a `tool_context` parameter to a tool to read or write it. ADK fills it in, and the model never sees it.

```python
from google.adk.tools.tool_context import ToolContext

def save_trip_details(nights: int, budget_eur: int, tool_context: ToolContext) -> dict:
    """Saves the trip length and total budget."""
    tool_context.state["budget_eur"] = budget_eur
    return {"status": "saved"}
```

## Callbacks (Exercise 2)

A callback is a Python function ADK runs at a set moment. Every callback works the same way:

- **Return `None`** to carry on as normal.
- **Return a value** to replace or skip that step.

ADK passes the arguments by keyword, so the parameter names must be exactly the ones below. Attach a callback to an agent, for example `Agent(..., after_tool_callback=enforce_budget)`. You can also pass a list of callbacks.

| Callback | Runs | Parameters | Return a value to... | Guardrail examples |
|---|---|---|---|---|
| `before_agent_callback` | Before an agent starts | `callback_context` | Skip the agent and reply with this `types.Content` | No trip planning until the budget is in state |
| `after_agent_callback` | After an agent finishes | `callback_context` | Replace the agent's final reply | Reject a plan that hits a closure in the local notes |
| `before_model_callback` | Before each LLM request | `callback_context`, `llm_request` | Skip the model call and use this `LlmResponse` | Block messages with card or passport numbers; refuse off-topic requests |
| `after_model_callback` | After each LLM reply | `callback_context`, `llm_response` | Replace the model's reply | Strip personal data; block promises the business can't keep |
| `before_tool_callback` | Before a tool runs | `tool`, `args`, `tool_context` | Skip the tool and use this dict as its result | Block a booking over budget; fix bad arguments; limit calls |
| `after_tool_callback` | After a tool runs | `tool`, `args`, `tool_context`, `tool_response` | Replace what the model sees | Exercise 2's budget filter; redact internal fields |

`callback_context.state` and `tool_context.state` are the same session state.

### after_tool_callback: change what the model sees

This is Exercise 2's rule.

```python
def enforce_budget(tool, args, tool_context, tool_response):
    if tool.name != "search_hotels":
        return None
    ...
    return {"status": "success", "hotels": affordable}

root_agent = Agent(..., after_tool_callback=enforce_budget)
```

### before_tool_callback: block or fix a call before it runs

```python
def block_expensive_details(tool, args, tool_context):
    if tool.name == "get_hotel_details" and args["hotel_name"] in BLOCKED:
        return {"status": "error", "message": "Not available."}  # tool never runs
    return None

root_agent = Agent(..., before_tool_callback=block_expensive_details)
```

You can also change `args` in place, for example `args["city"] = "Barcelona"`.

### before_model_callback: check input before the model sees it

```python
import re
from google.adk.models import LlmResponse
from google.genai import types

CARD = re.compile(r"\b(?:\d[ -]?){13,16}\b")

def block_card_numbers(callback_context, llm_request):
    last = llm_request.contents[-1]
    text = " ".join(p.text or "" for p in last.parts or [])
    if CARD.search(text):
        return LlmResponse(content=types.Content(role="model", parts=[
            types.Part(text="Please don't share card numbers here.")]))
    return None  # send the request to the model as normal

root_agent = Agent(..., before_model_callback=block_card_numbers)
```

### after_model_callback: check the model's reply

```python
def no_refund_promises(callback_context, llm_response):
    text = "".join(p.text or "" for p in (llm_response.content.parts if llm_response.content else []))
    if "full refund" in text.lower():
        return LlmResponse(content=types.Content(role="model", parts=[
            types.Part(text="Refunds depend on the booking. Please check with the hotel.")]))
    return None
```

### before_agent_callback: skip an agent

```python
def need_budget_first(callback_context):
    if "budget_eur" not in callback_context.state:
        return types.Content(role="model", parts=[
            types.Part(text="What's your total budget for the trip?")])
    return None  # run the agent as normal

planner_agent = Agent(..., before_agent_callback=need_budget_first)
```

### Asking the traveller first

For actions you can't undo, like booking or paying, ADK can pause and ask for confirmation before a tool runs:

```python
from google.adk.tools import FunctionTool

root_agent = Agent(..., tools=[FunctionTool(book_hotel, require_confirmation=True)])
```

## A fixed order (Exercise 3)

`SequentialAgent` runs its sub-agents in order, every time. `output_key` saves an agent's reply into state, and `{key}` in another agent's instruction reads it.

```python
from google.adk.agents import SequentialAgent

local_insider = Agent(..., output_key="local_notes")
planner_agent = Agent(..., instruction="Local notes:\n{local_notes}")

root_agent = SequentialAgent(
    name="tripmate",
    sub_agents=[local_insider, planner_agent],
)
```

`{key}` raises an error if the key isn't in state yet. `{key?}` gives empty text instead.

## Routing (Exercise 4)

An `Agent` with `sub_agents` reads each sub-agent's `description` and hands the conversation to the best one. Control passes to that specialist; it doesn't come back like a tool result.

```python
food_guide = Agent(
    name="food_guide",
    description="Recommends restaurants and food markets at the destination.",
    ...
)

root_agent = Agent(
    name="concierge",
    instruction="Answer quick questions yourself. Hand the rest to a specialist.",
    sub_agents=[trip_planner, food_guide],
)
```

An agent can have only one parent.

## Which tool for which job?

| You need | Use |
|---|---|
| The model to call your code | A tool |
| A rule that must always hold | State + a callback |
| A check before something runs | A `before_*` callback |
| Approval before an action you can't undo | `require_confirmation=True` |
| Steps that must happen in order | `SequentialAgent` |
| The model to pick a specialist | `sub_agents` on an `Agent` |

Let the model handle language, taste and judgement. Let code handle rules, money and order.
