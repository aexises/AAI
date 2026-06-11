#!/usr/bin/env python3
"""Minimal local RAG example with Chroma and Ollama."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_ollama import ChatOllama, OllamaEmbeddings
from rich.console import Console


PERSIST_DIR = Path("chroma_db")
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "gemma3:4b"


class DeterministicHashEmbeddings(Embeddings):
    """Tiny fallback embeddings for demos when a real embedding model is unavailable."""

    dimension = 64

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimension
        words = text.lower().split()
        for word in words:
            digest = hashlib.sha256(word.encode("utf-8")).digest()
            index = int.from_bytes(digest[:2], "big") % self.dimension
            vector[index] += 1.0
        norm = sum(value * value for value in vector) ** 0.5 or 1.0
        return [value / norm for value in vector]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)


def make_documents() -> list[Document]:
    return [
        Document(
            page_content="llama3.2:3b is the default local model for lightweight labs on an 8 GB Mac.",
            metadata={"source": "course-notes"},
        ),
        Document(
            page_content="gemma3:4b is a good local choice for slightly stronger general tasks and RAG answers.",
            metadata={"source": "course-notes"},
        ),
        Document(
            page_content="qwen2.5-coder:7b can help with coding tasks, but may be slow or heavy on 8 GB RAM.",
            metadata={"source": "course-notes"},
        ),
        Document(
            page_content="API keys are optional for local labs and only needed for cloud API experiments.",
            metadata={"source": "course-notes"},
        ),
    ]


def choose_embeddings(console: Console) -> Embeddings:
    try:
        embeddings = OllamaEmbeddings(model=EMBED_MODEL)
        embeddings.embed_query("test")
    except Exception as exc:
        console.print(
            f"[yellow]Could not use Ollama embedding model {EMBED_MODEL}: {exc}[/yellow]"
        )
        console.print(
            "[yellow]Falling back to simple deterministic hash embeddings for this demo.[/yellow]"
        )
        console.print(f"For better retrieval later, run: ollama pull {EMBED_MODEL}")
        return DeterministicHashEmbeddings()

    console.print(f"[green]Using Ollama embeddings:[/green] {EMBED_MODEL}")
    return embeddings


def format_context(docs: Iterable[Document]) -> str:
    return "\n".join(f"- {doc.page_content}" for doc in docs)


def main() -> int:
    console = Console()
    embeddings = choose_embeddings(console)
    documents = make_documents()

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(PERSIST_DIR),
        collection_name="agentic_ai_course_demo",
    )

    question = "Which local model should I start with on an 8 GB MacBook Air?"
    retrieved_docs = vectorstore.similarity_search(question, k=3)

    console.print("[bold]Retrieved documents:[/bold]")
    for index, doc in enumerate(retrieved_docs, start=1):
        console.print(f"{index}. {doc.page_content} ({doc.metadata.get('source', 'unknown')})")

    context = format_context(retrieved_docs)
    prompt = (
        "Answer using only the context below. Keep it beginner-friendly and concise.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}"
    )

    llm = ChatOllama(model=CHAT_MODEL, temperature=0.2)
    response = llm.invoke(prompt)

    console.print()
    console.print(f"[bold]LLM answer from {CHAT_MODEL}:[/bold]")
    console.print(response.content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
