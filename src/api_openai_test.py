#!/usr/bin/env python3
"""Minimal LangChain + OpenAI API smoke test."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from rich.console import Console


DEFAULT_MODEL = "gpt-5.4-mini"


def main() -> int:
    console = Console()
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        console.print(
            "[yellow]OPENAI_API_KEY is not set.[/yellow] "
            "Copy .env.example to .env and add a key when you are ready for OpenAI API labs."
        )
        return 0

    llm = ChatOpenAI(model=DEFAULT_MODEL, temperature=0.2)
    response = llm.invoke("In one short sentence, explain why API billing is separate from ChatGPT Plus.")

    console.print(f"[bold]OpenAI model:[/bold] {DEFAULT_MODEL}")
    console.print("[bold]Response:[/bold]")
    console.print(response.content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
