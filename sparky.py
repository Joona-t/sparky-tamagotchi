#!/usr/bin/env python3
"""Sparky Tamagotchi — your pink terminal pet! 💕"""

import sys
import os

# Ensure imports work when run from any directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from rich.console import Console
except ImportError:
    print("Sparky needs the 'rich' library!")
    print("Install it with: pip install rich")
    sys.exit(1)

from state import load_state, apply_decay, save_state, do_action, is_first_run
from ui import render_status, render_help, run_watch

VALID_ACTIONS = ("feed", "play", "sleep", "wake", "pet", "treat")


def main():
    args = sys.argv[1:]
    command = args[0].lower() if args else None

    if command == "help":
        render_help()
        return

    if command == "watch":
        run_watch()
        return

    if command and command not in VALID_ACTIONS:
        console = Console()
        console.print(f"[#E8457C]Unknown command:[/] {command}")
        console.print("[#9E4D6E]Try: sparky help[/]")
        return

    # Load and decay
    first_run = is_first_run()
    state = load_state()
    state = apply_decay(state)
    save_state(state)

    # Perform action if given
    action_result = None
    if command:
        state, action_result = do_action(state, command)

    render_status(state, action_result=action_result, first_run=first_run)


if __name__ == "__main__":
    main()
