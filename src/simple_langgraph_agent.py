#!/usr/bin/env python3
"""A tiny LangGraph workflow using a local Ollama chat model."""

from __future__ import annotations

from typing import TypedDict

from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph
from rich.console import Console


class AgentState(TypedDict):
    question: str
    answer: str


def main() -> int:
    console = Console()
    llm = ChatOllama(model="llama3.2:3b", temperature=0.2)

    def llm_node(state: AgentState) -> AgentState:
        prompt = (
            "You are a concise teaching assistant for an Agentic AI course. "
            f"Answer in two sentences: {state['question']}"
        )
        response = llm.invoke(prompt)
        return {"question": state["question"], "answer": response.content}

    graph_builder = StateGraph(AgentState)
    graph_builder.add_node("llm", llm_node)
    graph_builder.add_edge(START, "llm")
    graph_builder.add_edge("llm", END)

    graph = graph_builder.compile()
    result = graph.invoke({"question": "What is the role of state in LangGraph?", "answer": ""})

    console.print("[bold]LangGraph result:[/bold]")
    console.print(result["answer"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
