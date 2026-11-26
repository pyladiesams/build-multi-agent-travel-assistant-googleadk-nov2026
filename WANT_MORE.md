# Want more?

Today we used tools, state, an `after_tool_callback`, a `SequentialAgent` and routing with `sub_agents`. ADK can do a lot more. Below are the topics we didn't cover, with a short idea to try on TripMate and links to read further.

The official ADK docs live at [adk.dev](https://adk.dev/). Start with the [Python quickstart](https://adk.dev/get-started/python/) if you want a refresher.

## Parallel and loop agents

`SequentialAgent` runs steps one after another. `ParallelAgent` runs independent steps at the same time, for example searching flights and hotels at once. `LoopAgent` repeats steps until a condition is met, for example a writer and a critic going back and forth until the plan stays within budget.

**Try it:** split the TripMate planner into a flight finder and a hotel finder that run in parallel, then a writer that combines both.

- [Workflow agents overview](https://adk.dev/agents/workflow-agents/)
- [Parallel agents](https://adk.dev/agents/workflow-agents/parallel-agents/)
- [Loop agents](https://adk.dev/agents/workflow-agents/loop-agents/)
- [Multi-agent workflows](https://adk.dev/workflows/) and [common patterns](https://adk.dev/workflows/patterns/)
- [Graph workflows](https://adk.dev/graphs/): newer, for flows with branches, retries and human input

## Structured output with `output_schema`

Every agent today replied in free text. With `output_schema` and a Pydantic model, an agent returns data in a fixed shape that your code can use directly, like a trip summary with a total price as a number.

**Try it:** add an agent that turns the final plan into a `TripSummary` with destination, nights, total cost and hotel.

- [LLM agents: data handling](https://adk.dev/agents/llm-agents/#data-handling) (`output_schema`, `input_schema`, `output_key`)
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/)

## More callbacks: `before_agent_callback` and `before_model_callback`

We only used `after_tool_callback`. `before_agent_callback` can skip an agent that isn't ready yet, and `before_model_callback` can check or block a message before it reaches the model. [CHEATSHEET.md](CHEATSHEET.md#callbacks-exercise-2) has short examples of each.

**Try it:** stop the planner from running until the budget is in state, or block messages that contain card numbers.

- [Callbacks overview](https://adk.dev/callbacks/)
- [Types of callbacks](https://adk.dev/callbacks/types-of-callbacks/)
- [Callback design patterns and best practices](https://adk.dev/callbacks/design-patterns-and-best-practices/)
- [Plugins](https://adk.dev/plugins/): the same idea, applied to every agent at once
- [Safety and security for agents](https://adk.dev/safety/)
- [Asking for confirmation before a tool runs](https://adk.dev/tools-custom/confirmation/)

## Running agents in production

`adk web` is a development tool: sessions live in memory and disappear when you stop it, there's no login, and it shows debug information to anyone who opens it. In production you run the agent from your own code or an API server, store sessions in a database, and deploy it somewhere.

**Try it:** run TripMate with `adk api_server` and call it from a small script, or deploy it to Cloud Run.

- [Agent runtime](https://adk.dev/runtime/): running agents from your own code with a `Runner`
- [API server](https://adk.dev/runtime/api-server/) and [command line](https://adk.dev/runtime/command-line/)
- [Sessions and session services](https://adk.dev/sessions/session/), including storing sessions in a database
- [State](https://adk.dev/sessions/state/) and [long-term memory](https://adk.dev/sessions/memory/)
- [Deploying your agent](https://adk.dev/deploy/): [Cloud Run](https://adk.dev/deploy/cloud-run/), [Agent Runtime](https://adk.dev/deploy/agent-runtime/) (managed by Google Cloud), [GKE](https://adk.dev/deploy/gke/)
- [Observability](https://adk.dev/observability/): logs, metrics and traces
- [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits)

## More to learn from

- [google/adk-samples](https://github.com/google/adk-samples): complete example agents to read and run
- [google/adk-python](https://github.com/google/adk-python): the source code, for when the docs aren't enough
- [Kaggle 5-day AI Agents course](https://www.kaggle.com/learn-guide/5-day-agents): free, built on ADK
- [Google Codelabs on ADK](https://codelabs.developers.google.com/?text=adk): short guided labs
