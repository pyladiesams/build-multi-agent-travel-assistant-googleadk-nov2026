# Build a Multi-Agent Travel Assistant with Google ADK 
### Presentation: [{ YOUR PRESENTATION NAME }](workshop/presentation_template.pdf)

## Workshop description
In this hands-on workshop, participants will use Google ADK to build a travel assistant powered by multiple agents. We’ll explore how agents can work together, and how to give LLMs room to be creative while guiding them toward the task and outcomes you have in mind.

The workshop looks at moving beyond a single open-ended prompt towards agent workflows that are more structured and dependable. Participants will get practical experience shaping these workflows and a clearer sense of how to balance flexibility with control.

## Requirements
* Comfortable writing basic Python functions
* Python 3.11+ (required by the pinned `google-adk` version)
* A Google account, to create a free Gemini API key in [Google AI Studio](https://aistudio.google.com)
* PyLadies Amsterdam uses [uv](https://docs.astral.sh/uv/) for dependency management (pip works too)

## Setup
Please do this before the session. There is no time for it during the workshop.

### 1. Install the dependencies
With uv:

If `uv --version` gives `command not found`, install uv first, then open a new terminal:
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Then:
```bash
git clone <github-url-of-workshop-repo>
cd <name-of-repo>

uv sync
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```
uv downloads a suitable Python if you don't have 3.11+.

Or with pip (check first that `python --version` shows 3.11+):
```bash
git clone <github-url-of-workshop-repo>
cd <name-of-repo>

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Add your API key
Copy `.env.example` to `.env` in the repo root and paste in your key:
```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=paste-your-key-here
```

### 3. Run the smoke test
From the repo root, run:
```bash
adk web workshop
```
Open http://localhost:8000, pick `ex0_hello` and say hi. If it replies, you're ready.

On Windows, if `adk` isn't found, activate the venv again.

## Exercises
| # | Exercise | Starter | Solution |
|---|----------|---------|----------|
| 1 | [Build it, watch it overspend](workshop/ex1_overspend/README.md) | `workshop/ex1_overspend/` | `solutions/ex1_overspend/` |

To run a solution, use `adk web solutions`. After changing code, restart `adk web` and start a new session.

## For the workshop giver
Before the workshop, regenerate `requirements.txt` after any dependency change:
```bash
uv export --no-dev --no-hashes -o requirements.txt
```
Each agent folder has its own `tools.py`, an `__init__.py` containing `from . import agent`, and an `agent.py` that defines `root_agent`.

All exercises share the mock data in `data/`, so a change there affects every starter and solution. Each dataset has its own file, added when an exercise first needs it.

## Video record
Re-watch [this YouTube stream](link)

## Credits
This workshop was set up by @pyladiesams and @blutab

## Appendix
### Pre-Commit Hooks

To ensure our code looks beautiful, PyLadies uses pre-commit hooks. You can enable them by running `pre-commit install`. You may have to install `pre-commit` first, using `uv sync`, `uv pip install pre-commit` or `pip install pre-commit`.

Happy Coding :)
