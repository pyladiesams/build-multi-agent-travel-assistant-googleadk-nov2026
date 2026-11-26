# Build a Multi-Agent Travel Assistant with Google ADK
### Presentation: [workshop slides (PDF)](workshop/build-multi-agent-travel-assistant-googleadk-nov2026.pdf) · [PowerPoint](workshop/build-multi-agent-travel-assistant-googleadk-nov2026.pptx)

## Workshop description
In this hands-on workshop, participants will use Google ADK to build a travel assistant powered by multiple agents. We’ll explore how agents can work together, and how to give LLMs room to be creative while guiding them toward the task and outcomes you have in mind.

The workshop looks at moving beyond a single open-ended prompt towards agent workflows that are more structured and dependable. Participants will get practical experience shaping these workflows and a clearer sense of how to balance flexibility with control.

## Requirements
* Comfortable writing basic Python functions
* [Git](https://git-scm.com/downloads)
* Python 3.11+ (required by the pinned `google-adk` version). If you use uv, it downloads a suitable Python for you.
* A Google account, to create a free Gemini API key in [Google AI Studio](https://aistudio.google.com)
* PyLadies Amsterdam uses [uv](https://docs.astral.sh/uv/) for dependency management (pip works too)

## Setup
If you can, set this up before the session, so you can start building straight away.

### 1. Get the code
```bash
git clone https://github.com/pyladiesams/build-multi-agent-travel-assistant-googleadk-nov2026.git
cd build-multi-agent-travel-assistant-googleadk-nov2026
```
All the commands below are run from this folder (the repo root).

### 2. Install the dependencies
**Option A: uv (recommended)**

Check whether you have uv with `uv --version`. If you get `command not found`, install it and then open a new terminal:
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Then, from the repo root:
```bash
uv sync
```
Activate the virtual environment:
```bash
# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

**Option B: pip**

Check first that `python --version` (or `python3 --version`) shows 3.11 or higher. Then, from the repo root:
```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Windows
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add your API key
Create your own free key in [Google AI Studio](https://aistudio.google.com) (click **Get API key**). Please don't share a key: free limits apply per project, and on `gemini-3.5-flash-lite` a project gets 15 requests per minute, which one table sharing a key would quickly use up.

Copy the example file to `.env` in the repo root:
```bash
# macOS / Linux
cp .env.example .env

# Windows
copy .env.example .env
```
Open `.env` in your editor and replace `paste-your-key-here` with your key:
```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your-actual-key
```
`.env` is in `.gitignore`, so your key won't be committed.

### 4. Run the smoke test
With the virtual environment active, from the repo root run:
```bash
adk web workshop
```
Open http://localhost:8000, pick `ex0_hello` in the dropdown at the top left and say hi. If it replies, you're ready. Stop the server with `Ctrl+C`.

If `adk` isn't found, the virtual environment isn't active: run the activate command from step 2 again. With uv you can also skip activation and run `uv run adk web workshop`.

If a reply fails with `503 UNAVAILABLE`, the model is busy. Wait a minute and try again.

### 5. On the day
We may still update the exercises before the session, so pull the latest version when you arrive:
```bash
git pull
uv sync                           # or: pip install -r requirements.txt
```

## Exercises
| # | Exercise | Starter | Solution |
|---|----------|---------|----------|
| 1 | [Build it, watch it overspend](workshop/ex1_overspend/README.md) | `workshop/ex1_overspend/` | `solutions/ex1_overspend/` |
| 2 | [Make the budget a rule](workshop/ex2_budget_rule/README.md) | `workshop/ex2_budget_rule/` | `solutions/ex2_budget_rule/` |
| 3 | [A team with a fixed order](workshop/ex3_fixed_order/README.md) | `workshop/ex3_fixed_order/` | `solutions/ex3_fixed_order/` |
| 4 | [Capstone: the front desk](workshop/ex4_front_desk/README.md) | `workshop/ex4_front_desk/` | `solutions/ex4_front_desk/` |

[CHEATSHEET.md](CHEATSHEET.md) has every pattern from today on one page. For topics we didn't cover, see [WANT_MORE.md](WANT_MORE.md).

To run a solution, use `adk web solutions`. After changing code, restart `adk web` and start a new session.

## For the workshop giver
Before the workshop, regenerate `requirements.txt` after any dependency change:
```bash
uv export --no-dev --no-hashes -o requirements.txt
```
Each agent folder has an `__init__.py` containing `from . import agent` and an `agent.py` that defines `root_agent`. Everything the exercises share lives in the `tripmate/` package at the repo root, which `uv sync` / `pip install -r requirements.txt` installs:

- `tripmate/config.py`: settings such as the model name and the hotel share of the budget. Change them here, once.
- `tripmate/data.py`: loads the mock data from `data/`.
- `tripmate/tools.py`: every tool the agents can call.
- `tripmate/budget.py`: the budget rule from Exercise 2, used from Exercise 3 on.

Instead of calling third-party APIs to fetch flights, hotels and other travel data, the workshop uses mock data: JSON files in `data/` that imitate what those APIs would return.

## Video record
Re-watch [this YouTube stream](https://www.youtube.com/live/YkeQV9zuog8)

## Credits
This workshop was set up by @pyladiesams and @blutab

## Appendix
### Pre-Commit Hooks

To ensure our code looks beautiful, PyLadies uses pre-commit hooks. You can enable them by running `pre-commit install`. You may have to install `pre-commit` first, using `uv sync`, `uv pip install pre-commit` or `pip install pre-commit`.

Happy Coding :)
