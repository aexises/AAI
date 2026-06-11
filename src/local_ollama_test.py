#!/usr/bin/env python3
"""Minimal LangChain + Ollama smoke test."""

from __future__ import annotations

import argparse

from langchain_ollama import ChatOllama
from rich.console import Console


def main() -> int:
    parser = argparse.ArgumentParser(description="Test a local Ollama chat model.")
    parser.add_argument(
        "model",
        nargs="?",
        default="llama3.2:3b",
        help="Ollama model name, for example llama3.2:3b or gemma3:4b.",
    )
    args = parser.parse_args()

    console = Console()
    console.print(f"[bold]Testing Ollama model:[/bold] {args.model}")

    llm = ChatOllama(model=args.model, temperature=0.2)
    response = llm.invoke("In one short sentence, explain what an AI agent is.")

    console.print("[bold]Response:[/bold]")
    console.print(response.content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
