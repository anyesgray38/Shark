#!/usr/bin/env python3
"""
Persistent Memory Claude — a terminal AI that remembers everything across sessions.
Memories are stored in a local ChromaDB vector database (~/.shark_memory/).
"""

import os
import sys
import json
import hashlib
import datetime
import readline
import anthropic
import chromadb
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

# ── Config ────────────────────────────────────────────────────────────────────
MEMORY_DIR = Path.home() / ".shark_memory"
MEMORY_DIR.mkdir(exist_ok=True)

MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-4-8")
BASE_URL = os.getenv("ANTHROPIC_BASE_URL")          # set this for local/Ollama
API_KEY  = os.getenv("ANTHROPIC_API_KEY", "sk-dummy")

MAX_MEMORIES_PER_QUERY = 6   # how many past memories to inject per turn
MEMORY_THRESHOLD = 3         # inject memory every N turns

console = Console()

# ── Vector memory store ───────────────────────────────────────────────────────
chroma = chromadb.PersistentClient(path=str(MEMORY_DIR / "chroma"))

try:
    mem_collection = chroma.get_collection("memories")
except Exception:
    mem_collection = chroma.create_collection(
        "memories",
        metadata={"hnsw:space": "cosine"},
    )


def _mem_id(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def save_memory(text: str, role: str = "user") -> None:
    ts = datetime.datetime.now().isoformat()
    uid = _mem_id(text + ts)
    mem_collection.add(
        documents=[text],
        metadatas=[{"role": role, "ts": ts}],
        ids=[uid],
    )


def recall_memories(query: str, n: int = MAX_MEMORIES_PER_QUERY) -> list[str]:
    count = mem_collection.count()
    if count == 0:
        return []
    results = mem_collection.query(
        query_texts=[query],
        n_results=min(n, count),
    )
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    out = []
    for doc, meta in zip(docs, metas):
        ts = meta.get("ts", "")[:19].replace("T", " ")
        role = meta.get("role", "?")
        out.append(f"[{ts}] {role}: {doc}")
    return out


def forget_all() -> int:
    count = mem_collection.count()
    if count:
        all_ids = mem_collection.get()["ids"]
        mem_collection.delete(ids=all_ids)
    return count


# ── Conversation history (in-session) ────────────────────────────────────────
history: list[dict] = []


def build_system(memories: list[str]) -> str:
    base = (
        "You are Shark — a persistent AI assistant running 24/7 on this terminal. "
        "You remember past conversations and use them to give better answers. "
        "When the user references something past, use the memories below. "
        "Be direct, concise, and technical when needed."
    )
    if memories:
        mem_block = "\n".join(f"  • {m}" for m in memories)
        base += f"\n\n## Relevant memories from past sessions:\n{mem_block}"
    return base


# ── Claude client ─────────────────────────────────────────────────────────────
client_kwargs = {"api_key": API_KEY}
if BASE_URL:
    client_kwargs["base_url"] = BASE_URL

client = anthropic.Anthropic(**client_kwargs)


def chat(user_input: str, turn: int) -> str:
    # Save user message to long-term memory
    save_memory(user_input, role="user")

    # Recall relevant memories every MEMORY_THRESHOLD turns or on first turn
    memories = []
    if turn % MEMORY_THRESHOLD == 0 or turn == 1:
        memories = recall_memories(user_input)

    history.append({"role": "user", "content": user_input})

    # Stream response
    full_response = ""
    with client.messages.stream(
        model=MODEL,
        max_tokens=4096,
        system=build_system(memories),
        messages=history,
        thinking={"type": "adaptive"},
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_response += text

    print()  # newline after stream

    # Save assistant reply to memory and history
    save_memory(full_response, role="assistant")
    history.append({"role": "assistant", "content": full_response})

    return full_response


# ── Commands ──────────────────────────────────────────────────────────────────
COMMANDS = {
    "/memories": "Show recent memories",
    "/forget":   "Wipe all memories",
    "/stats":    "Show memory stats",
    "/history":  "Show this session's history",
    "/help":     "Show commands",
    "/quit":     "Exit",
}


def handle_command(cmd: str) -> bool:
    cmd = cmd.strip().lower()
    if cmd == "/quit" or cmd == "/exit":
        console.print("\n[bold cyan]Shark shutting down. Memory persisted.[/]")
        sys.exit(0)

    elif cmd == "/memories":
        count = mem_collection.count()
        console.print(f"\n[bold]Total memories stored:[/] {count}")
        if count:
            sample = mem_collection.get(limit=10)
            for doc, meta in zip(sample["documents"], sample["metadatas"]):
                ts = meta.get("ts", "")[:19].replace("T", " ")
                role = meta.get("role", "?")
                console.print(f"  [dim]{ts}[/] [cyan]{role}[/]: {doc[:120]}")

    elif cmd == "/forget":
        n = forget_all()
        console.print(f"[red]Wiped {n} memories.[/]")

    elif cmd == "/stats":
        count = mem_collection.count()
        size = sum(f.stat().st_size for f in MEMORY_DIR.rglob("*") if f.is_file())
        console.print(f"[bold]Memories:[/] {count}")
        console.print(f"[bold]DB size:[/]  {size / 1024:.1f} KB")
        console.print(f"[bold]DB path:[/]  {MEMORY_DIR}")

    elif cmd == "/history":
        for msg in history:
            role = msg["role"].upper()
            console.print(f"\n[bold cyan]{role}[/]: {msg['content'][:300]}")

    elif cmd == "/help":
        for c, desc in COMMANDS.items():
            console.print(f"  [bold cyan]{c}[/]  {desc}")

    else:
        console.print(f"[red]Unknown command.[/] Type [cyan]/help[/] for options.")

    return True


# ── Main loop ─────────────────────────────────────────────────────────────────
def main():
    console.print(Panel(
        "[bold cyan]Shark[/] — Persistent Memory AI\n"
        f"Model: [yellow]{MODEL}[/]   "
        f"Base URL: [yellow]{BASE_URL or 'Anthropic default'}[/]\n"
        f"Memory DB: [dim]{MEMORY_DIR}[/]\n"
        "Type [cyan]/help[/] for commands, [cyan]/quit[/] to exit.",
        title="[bold]SHARK[/]",
        border_style="cyan",
    ))

    turn = 0
    while True:
        try:
            user_input = input("\n[You] ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[bold cyan]Bye. Memory persisted.[/]")
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            handle_command(user_input)
            continue

        turn += 1
        console.print("\n[bold green][Shark][/]")
        chat(user_input, turn)


if __name__ == "__main__":
    main()
