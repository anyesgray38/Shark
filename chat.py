#!/usr/bin/env python3
"""
Shark AI — terminal chat with swappable providers.

Usage:
    python chat.py                  # start chat
    python chat.py --provider local # use local model this session
    python chat.py --set-provider local  # save local as default
    python chat.py --sessions       # list saved sessions
    python chat.py --load <file>    # resume a session
"""
import argparse
import sys
import os

# Allow running from repo root without install
sys.path.insert(0, os.path.dirname(__file__))

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

from ai.core import config, session, factory

console = Console()


def parse_args():
    p = argparse.ArgumentParser(prog="chat", description="Shark AI terminal chat")
    p.add_argument("--provider", choices=["claude", "local"], help="Override provider for this session")
    p.add_argument("--set-provider", choices=["claude", "local"], metavar="PROVIDER", help="Save provider as default")
    p.add_argument("--set-system", metavar="PROMPT", help="Set a persistent system prompt")
    p.add_argument("--set-model", metavar="MODEL", help="Set local model name (e.g. llama3, mistral)")
    p.add_argument("--sessions", action="store_true", help="List saved sessions")
    p.add_argument("--load", metavar="FILE", help="Resume a saved session")
    p.add_argument("--no-stream", action="store_true", help="Disable streaming output")
    return p.parse_args()


def handle_config_flags(args, cfg):
    changed = False
    if args.set_provider:
        cfg["provider"] = args.set_provider
        changed = True
    if args.set_system is not None:
        cfg["system_prompt"] = args.set_system
        changed = True
    if args.set_model:
        cfg["local_model"] = args.set_model
        changed = True
    if changed:
        config.save(cfg)
        sys.exit(0)


def print_banner(provider_name: str):
    console.print(Panel(
        f"[bold cyan]Shark AI[/bold cyan]  [dim]powered by {provider_name}[/dim]\n"
        "[dim]Commands: /quit  /save  /clear  /sessions  /switch claude|local  /system <prompt>[/dim]",
        border_style="cyan",
        expand=False,
    ))


def run_chat(args):
    cfg = config.load()
    handle_config_flags(args, cfg)

    if args.sessions:
        sessions = session.list_sessions()
        if not sessions:
            console.print("[dim]No saved sessions.[/dim]")
        for s in sessions:
            console.print(f"  {s}")
        sys.exit(0)

    # Apply session override
    if args.provider:
        cfg["provider"] = args.provider
    if args.no_stream:
        cfg["stream"] = False

    messages: list[dict] = []
    if args.load:
        messages = session.load(args.load)
        console.print(f"[dim]Loaded {len(messages)} messages from {args.load}[/dim]")

    try:
        provider = factory.make_provider(cfg)
    except RuntimeError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    print_banner(provider.name)

    while True:
        try:
            user_input = console.input("[bold green]You:[/bold green] ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Bye.[/dim]")
            break

        if not user_input:
            continue

        # Slash commands
        if user_input.startswith("/"):
            cmd = user_input.split(None, 1)
            verb = cmd[0].lower()

            if verb == "/quit":
                console.print("[dim]Bye.[/dim]")
                break

            elif verb == "/save":
                path = session.save(messages, provider.name)
                console.print(f"[dim]Session saved to {path}[/dim]")

            elif verb == "/clear":
                messages.clear()
                console.print("[dim]History cleared.[/dim]")

            elif verb == "/sessions":
                for s in session.list_sessions():
                    console.print(f"  {s}")

            elif verb == "/switch" and len(cmd) > 1:
                cfg["provider"] = cmd[1].strip()
                try:
                    provider = factory.make_provider(cfg)
                    console.print(f"[dim]Switched to {provider.name}[/dim]")
                except Exception as e:
                    console.print(f"[red]Switch failed:[/red] {e}")

            elif verb == "/system" and len(cmd) > 1:
                cfg["system_prompt"] = cmd[1].strip()
                provider = factory.make_provider(cfg)
                console.print(f"[dim]System prompt updated.[/dim]")

            else:
                console.print("[dim]Unknown command. Try /quit /save /clear /sessions /switch /system[/dim]")
            continue

        messages.append({"role": "user", "content": user_input})

        console.print("[bold magenta]AI:[/bold magenta] ", end="")
        full_response = ""
        try:
            for chunk in provider.chat(messages, stream=cfg.get("stream", True)):
                console.print(chunk, end="", markup=False)
                full_response += chunk
            console.print()  # newline after stream ends
        except Exception as e:
            console.print(f"\n[red]Error:[/red] {e}")
            messages.pop()  # remove failed user message
            continue

        messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    args = parse_args()
    run_chat(args)
