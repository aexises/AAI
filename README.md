# AAI Agentic AI Course Labs

This repository is a clean Python 3.11+ environment for local and API-based LLM agent experiments. It is designed for a MacBook Air M2 with 8 GB RAM, so the local model path stays intentionally lightweight.

## Hardware Assumptions

- Machine: MacBook Air M2
- RAM: 8 GB
- Local inference: Ollama with small models first

Recommended local model strategy:

- `llama3.2:3b`: default local model for fast, lightweight experiments.
- `gemma3:4b`: slightly stronger general-purpose and RAG model.
- `qwen2.5-coder:7b`: optional coding model; useful, but may be slow or heavy on 8 GB RAM.

## API Provider Notes

You do not need to choose an API provider before starting the local labs.

ChatGPT Plus does not include OpenAI API access. OpenAI API billing is separate from ChatGPT subscriptions and requires API billing setup in the OpenAI platform account.

OpenAI vs Anthropic, practically:

- OpenAI: best compatibility with many tutorials, LangChain/LangGraph examples, and inexpensive mini models.
- Anthropic: excellent coding quality, usually more expensive.

The starter scripts install both clients, but API keys are optional until cloud API labs.

## Setup

If your shell has trouble with the square brackets in `AAI[sum26]`, quote the path when opening or moving the repo:

```bash
cd /Users/daeron/Documents
code 'AAI[sum26]'
```

Create and activate a virtual environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `python3.11` is not installed, install Python 3.11+ first. On macOS with Homebrew:

```bash
brew install python@3.11
```

Create a local environment file:

```bash
cp .env.example .env
```

Leave the API keys empty for now if you are only running local Ollama labs.

## Install Ollama

Download and install Ollama for macOS:

```bash
open https://ollama.com/download
```

Open the Ollama app once so the local server starts, then pull the recommended models:

```bash
chmod +x scripts/setup_ollama_models.sh
./scripts/setup_ollama_models.sh
```

The script pulls:

- `llama3.2:3b`
- `gemma3:4b`

It asks before pulling:

- `qwen2.5-coder:7b`

## Check The Environment

```bash
python scripts/check_environment.py
```

This prints your Python version, checks package imports, checks whether the Ollama server responds locally, and reports whether `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` are present. Missing API keys do not block local labs.

## Run Local Tests

Test the default local model:

```bash
python src/local_ollama_test.py
```

Test a different local model:

```bash
python src/local_ollama_test.py gemma3:4b
```

Run the minimal LangGraph example:

```bash
python src/simple_langgraph_agent.py
```

Run the minimal Chroma RAG example:

```bash
python src/simple_rag_chroma.py
```

For better RAG embeddings, optionally pull a local embedding model:

```bash
ollama pull nomic-embed-text
```

The RAG script still runs with a simple deterministic fallback if the embedding model is unavailable.

## Add OpenAI Later

Add your key to `.env`:

```bash
OPENAI_API_KEY=your_key_here
```

Then run:

```bash
python src/api_openai_test.py
```

The default OpenAI test model is `gpt-5.4-mini`, a current lower-cost OpenAI model choice.

## Add Anthropic Later

Add your key to `.env`:

```bash
ANTHROPIC_API_KEY=your_key_here
```

Then run:

```bash
python src/api_anthropic_test.py
```

The default Anthropic test model is `claude-haiku-4-5-20251001`, a fast and cheaper Claude model.

## Recommended Initial Path

1. Install Python 3.11+.
2. Create and activate `.venv`.
3. Run `pip install -r requirements.txt`.
4. Install Ollama.
5. Run `./scripts/setup_ollama_models.sh`.
6. Run `python scripts/check_environment.py`.
7. Run `python src/local_ollama_test.py`.
8. Add an OpenAI or Anthropic API key later if cloud labs need it.

## Files

- `requirements.txt`: Python dependencies for LangChain, LangGraph, MCP, vector stores, tracing, and API clients.
- `.env.example`: API key template with no secrets.
- `scripts/setup_ollama_models.sh`: Ollama model setup helper.
- `scripts/check_environment.py`: local setup diagnostics.
- `src/local_ollama_test.py`: local Ollama smoke test.
- `src/api_openai_test.py`: OpenAI API smoke test.
- `src/api_anthropic_test.py`: Anthropic API smoke test.
- `src/simple_langgraph_agent.py`: minimal LangGraph workflow.
- `src/simple_rag_chroma.py`: minimal local Chroma RAG demo.
