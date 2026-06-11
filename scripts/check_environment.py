#!/usr/bin/env python3
"""Check local setup for the Agentic AI labs."""

from __future__ import annotations

import importlib
import os
import sys
import urllib.error
import urllib.request

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table


REQUIRED_IMPORTS = {
    "langchain": "langchain",
    "langchain-community": "langchain_community",
    "langchain-ollama": "langchain_ollama",
    "langchain-openai": "langchain_openai",
    "langchain-anthropic": "langchain_anthropic",
    "langgraph": "langgraph",
    "mcp": "mcp",
    "chromadb": "chromadb",
    "faiss-cpu": "faiss",
    "langfuse": "langfuse",
    "python-dotenv": "dotenv",
    "pydantic": "pydantic",
    "tiktoken": "tiktoken",
    "rich": "rich",
}


def check_imports(console: Console) -> bool:
    table = Table(title="Python Package Imports")
    table.add_column("Package")
    table.add_column("Import")
    table.add_column("Status")

    all_ok = True
    for package, module_name in REQUIRED_IMPORTS.items():
        try:
            importlib.import_module(module_name)
        except Exception as exc:
            all_ok = False
            table.add_row(package, module_name, f"[red]FAILED[/red] {exc}")
        else:
            table.add_row(package, module_name, "[green]OK[/green]")

    console.print(table)
    return all_ok


def check_ollama(console: Console) -> bool:
    url = "http://localhost:11434/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            ok = response.status == 200
    except urllib.error.URLError as exc:
        console.print(f"[yellow]Ollama server check failed:[/yellow] {exc}")
        console.print("Start Ollama by opening the Ollama app or running: ollama serve")
        return False

    if ok:
        console.print("[green]Ollama server is responding at http://localhost:11434[/green]")
        return True

    console.print("[yellow]Ollama responded, but not with HTTP 200.[/yellow]")
    return False


def check_api_keys(console: Console) -> None:
    load_dotenv()
    console.print()
    console.print("[bold]API Keys[/bold]")

    for key_name in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
        if os.getenv(key_name):
            console.print(f"[green]{key_name} is set.[/green]")
        else:
            console.print(f"[yellow]{key_name} is not set.[/yellow]")

    console.print(
        "API keys are optional for local Ollama labs. Add one later when you start cloud API labs."
    )


def main() -> int:
    console = Console()
    console.print("[bold]Agentic AI Environment Check[/bold]")
    console.print(f"Python: {sys.version.split()[0]}")

    if sys.version_info < (3, 11):
        console.print("[red]Python 3.11+ is required.[/red]")
    else:
        console.print("[green]Python version is 3.11 or newer.[/green]")

    console.print()
    imports_ok = check_imports(console)
    console.print()
    ollama_ok = check_ollama(console)
    check_api_keys(console)

    console.print()
    if imports_ok and ollama_ok and sys.version_info >= (3, 11):
        console.print("[green]Environment looks ready for local labs.[/green]")
        return 0

    console.print("[yellow]Some checks need attention. See messages above.[/yellow]")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
