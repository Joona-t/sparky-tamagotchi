"""Sparky Tamagotchi — Rich terminal rendering (CLI + watch mode)."""

import os
import sys
import time

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich import box

from state import get_health, get_mood, load_state, apply_decay, save_state, do_action, is_first_run, MAX_TREATS_PER_DAY
from art import get_idle_frame, get_action_frame
from messages import get_mood_message, get_action_message, get_greeting, get_low_stat_hint, WELCOME_MESSAGE

# LoveSpark color palette
PINK_ACCENT = "#E8457C"
PINK_DEEP = "#D63466"
PINK_LIGHT = "#FDCFE1"
PINK_MID = "#F9A8C9"
TEXT_DARK = "#5C1A36"
TEXT_MUTED = "#9E4D6E"
WHITE = "#FFFFFF"
PURPLE = "#7C3AED"
TEAL = "#0D9488"

console = Console()


def stat_bar(value, width=10):
    """Render a stat bar like ████████░░"""
    filled = round(value / 100 * width)
    empty = width - filled
    return "█" * filled + "░" * empty


def color_for_stat(value):
    if value >= 70:
        return TEAL
    if value >= 40:
        return PINK_ACCENT
    return PINK_DEEP


def render_status(state, action_result=None, first_run=False):
    """Render compact CLI status view."""
    mood = get_mood(state)
    health = get_health(state)

    # Pick art frame
    if action_result and get_action_frame(action_result):
        art = get_action_frame(action_result)
    else:
        art = get_idle_frame(state)

    # Build art text
    art_text = Text(art, style=PINK_ACCENT)

    # Build stats
    stats_lines = Text()
    for emoji, label, value in [
        ("🍪", "Hunger   ", state["hunger"]),
        ("💖", "Happiness", state["happiness"]),
        ("⚡", "Energy   ", state["energy"]),
        ("💗", "Health   ", health),
    ]:
        bar = stat_bar(value)
        color = color_for_stat(value)
        stats_lines.append(f" {emoji} {label} ")
        stats_lines.append(bar, style=color)
        stats_lines.append(f" {round(value)}\n", style=color)

    stats_lines.append(f"\n Age: {state['age_days']} days\n", style=TEXT_MUTED)
    treats_left = MAX_TREATS_PER_DAY - state.get("treats_today", 0)
    stats_lines.append(f" Treats: {treats_left}/{MAX_TREATS_PER_DAY} left\n", style=TEXT_MUTED)
    if state.get("sleeping"):
        stats_lines.append(" 💤 Sleeping...\n", style=PURPLE)

    # Build layout table
    layout = Table(show_header=False, show_edge=False, box=None, padding=0)
    layout.add_column(width=22)
    layout.add_column()
    layout.add_row(art_text, stats_lines)

    # Pick message
    if first_run:
        message = WELCOME_MESSAGE
    elif action_result:
        message = get_action_message(action_result)
    else:
        hint = get_low_stat_hint(state)
        if hint:
            message = hint
        else:
            message = get_mood_message(mood)

    # Greeting line for returning users
    greeting = ""
    if not first_run and not action_result:
        greeting = get_greeting() + "\n"

    # Render panel
    content = Text()
    if greeting:
        content.append(greeting, style=TEXT_MUTED)
    content.append_text(Text(""))  # spacer

    full_content = Table(show_header=False, show_edge=False, box=None, padding=0)
    full_content.add_row(layout)
    full_content.add_row(Text(""))
    full_content.add_row(Text(f" {message}", style=TEXT_DARK))

    panel = Panel(
        full_content,
        title="[bold]✨ Sparky Tamagotchi ✨[/bold]",
        title_align="center",
        border_style=PINK_ACCENT,
        padding=(1, 2),
    )

    if greeting:
        console.print(Text(f" {greeting.strip()}", style=TEXT_MUTED))
    console.print(panel)


def render_help():
    """Render help panel."""
    help_text = Text()
    commands = [
        ("sparky", "Quick status check"),
        ("sparky feed", "Feed Sparky (+hunger)"),
        ("sparky play", "Play with Sparky (+happiness, -energy)"),
        ("sparky sleep", "Put Sparky to sleep (+energy over time)"),
        ("sparky wake", "Wake up Sparky"),
        ("sparky pet", "Pet Sparky (+happiness)"),
        ("sparky treat", "Give a treat (all stats +15, 3/day)"),
        ("sparky watch", "Live dashboard mode"),
        ("sparky help", "Show this help"),
    ]
    for cmd, desc in commands:
        help_text.append(f"  {cmd:<18}", style=PINK_ACCENT)
        help_text.append(f"{desc}\n", style=TEXT_DARK)

    panel = Panel(
        help_text,
        title="[bold]✨ Sparky Commands ✨[/bold]",
        title_align="center",
        border_style=PINK_ACCENT,
        padding=(1, 2),
    )
    console.print(panel)


def build_watch_layout(state, action_result=None, message_override=None):
    """Build the full watch mode panel as a renderable."""
    mood = get_mood(state)
    health = get_health(state)

    # Pick art
    if action_result and get_action_frame(action_result):
        art = get_action_frame(action_result)
    else:
        art = get_idle_frame(state)

    art_text = Text(art, style=PINK_ACCENT)

    # Stats column
    stats = Text()
    for emoji, label, value in [
        ("🍪", "Hunger   ", state["hunger"]),
        ("💖", "Happiness", state["happiness"]),
        ("⚡", "Energy   ", state["energy"]),
        ("💗", "Health   ", health),
    ]:
        bar = stat_bar(value)
        color = color_for_stat(value)
        stats.append(f" {emoji} {label} ")
        stats.append(bar, style=color)
        stats.append(f" {round(value)}\n", style=color)

    stats.append(f"\n Age: {state['age_days']} days\n", style=TEXT_MUTED)
    treats_left = MAX_TREATS_PER_DAY - state.get("treats_today", 0)
    stats.append(f" Treats: {treats_left}/{MAX_TREATS_PER_DAY} left\n", style=TEXT_MUTED)
    if state.get("sleeping"):
        stats.append(" 💤 Sleeping...\n", style=PURPLE)

    # Side by side
    layout = Table(show_header=False, show_edge=False, box=None, padding=0)
    layout.add_column(width=22)
    layout.add_column()
    layout.add_row(art_text, stats)

    # Message
    if message_override:
        message = message_override
    elif action_result:
        message = get_action_message(action_result)
    else:
        hint = get_low_stat_hint(state)
        message = hint if hint else get_mood_message(mood)

    # Commands footer
    cmd_text = Text("  feed | play | sleep | pet | treat | quit", style=TEXT_MUTED)

    # Compose
    content = Table(show_header=False, show_edge=False, box=None, padding=0)
    content.add_row(layout)
    content.add_row(Text(""))
    content.add_row(Panel(Text(f" {message}", style=TEXT_DARK), border_style=PINK_MID, box=box.HORIZONTALS))
    content.add_row(Text(""))
    content.add_row(cmd_text)

    return Panel(
        content,
        title="[bold]✨ Sparky Tamagotchi ✨[/bold]",
        title_align="center",
        border_style=PINK_ACCENT,
        padding=(1, 2),
    )


def clear_screen():
    # Static arguments only — "clear" on Unix, "cls" on Windows
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def run_watch():
    """Interactive watch mode — clear-reprint-input loop."""
    state = load_state()
    state = apply_decay(state)
    save_state(state)

    action_result = None
    message_override = None

    while True:
        clear_screen()
        panel = build_watch_layout(state, action_result=action_result, message_override=message_override)
        console.print(panel)

        # Reset action display after showing once
        action_result = None
        message_override = None

        try:
            cmd = console.input("[#E8457C]  💕 > [/]").strip().lower()
        except (EOFError, KeyboardInterrupt):
            clear_screen()
            console.print(Text(" Bye bye! Sparky waves! 💕\n", style=PINK_ACCENT))
            break

        if cmd in ("quit", "q", "exit"):
            clear_screen()
            console.print(Text(" Bye bye! Sparky waves! 💕\n", style=PINK_ACCENT))
            break
        elif cmd in ("feed", "play", "sleep", "wake", "pet", "treat"):
            # Re-apply decay before action
            state = apply_decay(state)
            state, action_result = do_action(state, cmd)
        elif cmd == "help":
            message_override = "feed | play | sleep | wake | pet | treat | quit"
        elif cmd == "":
            # Just refresh — re-apply decay
            state = apply_decay(state)
            save_state(state)
        else:
            message_override = f"Unknown command: {cmd}. Try: feed, play, sleep, pet, treat, quit"
