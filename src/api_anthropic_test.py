#!/usr/bin/env python3
"""Minimal LangChain + Anthropic API smoke test."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from rich.console import Console


DEFAULT_MODEL = "claude-haiku-4-5-20251001"


def main() -> int:
    console = Console()
    load_dotenv()

    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print(
            "[yellow]ANTHROPIC_API_KEY is not set.[/yellow] "
            "Copy .env.example to .env and add a key when you are ready for Anthropic API labs."
        )
        return 0

    llm = ChatAnthropic(model=DEFAULT_MODEL, temperature=0.2)
    response = llm.invoke("In one short sentence, explain what LangGraph is useful for.")

    console.print(f"[bold]Anthropic model:[/bold] {DEFAULT_MODEL}")
    console.print("[bold]Response:[/bold]")
    console.print(response.content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
