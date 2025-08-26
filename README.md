## 🔎 Deep Research SDK 🤖

A Python SDK that automates deep, multi-iteration research using AI agents + web search. It turns a single question into a structured report with sources. 

- **What you get**: AI-generated queries ➜ real-time web results ➜ concise analyses ➜ follow-up loops ➜ a final, well-structured report.
- **Powered by**: LiteLLM, DuckDuckGo Search (`ddgs`), and `rich` for a slick CLI.

---

### ✨ Features

- **🧠 Multi-agent pipeline**: Query generation, web summarization, follow-up decisioning, synthesis.
- **🔁 Iterative research**: Decides if/when to dig deeper; runs multiple rounds automatically.
- **🌐 Live web search**: DuckDuckGo for real-time sources, with basic scraping and summarization.
- **📝 Markdown reports**: Clear structure, headings, and sources list.
- **🎛️ Model-flexible**: Use any LiteLLM-supported model (OpenAI, Anthropic, etc.).
- **📟 Pretty CLI**: Live progress and panels via `rich`.

---

 

### ⚙️ Installation

```bash
git clone <repository-url>
cd deep-research-sdk
pip install .
```

Create a `.env` with your API keys:
```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
# Optional:
# echo "ANTHROPIC_API_KEY=your_anthropic_api_key_here" >> .env
```

- Requires Python 3.11+.

---

### 🚀 Quick Start

#### CLI (interactive)
```bash
# Installed entrypoint (recommended)
deep-research-sdk research

# Or run directly from the repo
python deep_research_sdk/cli.py research

# Show version
deep-research-sdk -v

# Show help
deep-research-sdk -h
python deep_research_sdk/cli.py -h
```
You’ll be prompted for a topic. The tool will research it and print a Markdown report.

---

<details>
<summary>More details</summary>

### 🏗️ Architecture at a glance

- `ResearchCoordinator` — orchestrates the full loop.
- `QueryAgent` — turns your topic into targeted search queries.
- `SearchAgent` — fetches a result, scrapes the page, summarizes it.
- `FollowUpAgent` — decides whether to continue and what to search next.
- `SynthesisAgent` — merges everything into a final report.

---

### 🔬 How it works

1. **🧭 Query generation** — Breaks your topic into focused queries.
2. **🔎 Web search** — Finds results via DuckDuckGo (`ddgs`).
3. **🧪 Page analysis** — Scrapes each result and summarizes with the model.
4. **🤔 Follow-up decision** — Decides whether to search again; generates follow-up queries if needed.
5. **🧵 Synthesis** — Produces a structured Markdown report with key findings and sources.

Note: By default, search pulls a small number of results per query to stay fast and focused.

---

### 📚 API Reference

#### `ResearchCoordinator`
```python
ResearchCoordinator(
  model: str,
  query: str,
  max_iterations: int | None = 3
)
```

- **model**: Any LiteLLM-supported model ID (e.g., `"gpt-4o-mini"`, `"gpt-4"`, `"claude-3-sonnet"`).
- **query**: Your research topic/question.
- **max_iterations**: How many rounds the system may run.

Method:
- `await research() -> str` — Runs the full pipeline and returns a Markdown report.

---

### 🧰 Python examples

```python
import asyncio
from deep_research_sdk import ResearchCoordinator

async def main():
    coordinator = ResearchCoordinator(
        model="gpt-4o-mini",
        query="What are the latest developments in quantum computing?",
        max_iterations=3
    )
    report = await coordinator.research()
    print(report)

asyncio.run(main())
```

```python
import asyncio
from deep_research_sdk import ResearchCoordinator

async def run():
    rc = ResearchCoordinator(
        model="gpt-4",
        query="What are the current theories about dark matter and their implications?",
        max_iterations=3
    )
    report = await rc.research()
    with open("dark_matter_report.md", "w") as f:
        f.write(report)

asyncio.run(run())
```

---

### 🧩 Configuration

Set environment variables via `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
# Optional (LiteLLM supports many providers)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Supported model IDs include (but aren’t limited to):
- `gpt-4o-mini` (great balance)
- `gpt-4`
- `gpt-3.5-turbo`
- `claude-3-sonnet`
- `claude-3-haiku`

---

### ✅ Dependencies

- `litellm` — model routing + unified client
- `pydantic` — typed responses from agents
- `rich` — styled CLI
- `ddgs` — DuckDuckGo search
- `requests`, `bs4` — basic scraping
- `python-dotenv` — env management

---

### 🛠️ Troubleshooting

- ❌ Missing report? Ensure `OPENAI_API_KEY` (or other provider keys) is set.
- 🕸️ Empty/odd summaries? Websites may block scraping; try different queries.
- 🐢 Slow runs? Reduce `max_iterations`, or try a faster/cheaper model.
- 🌍 Network issues? Check firewall/proxy; `ddgs` requires outbound access.

</details>

### 📜 License

MIT License
