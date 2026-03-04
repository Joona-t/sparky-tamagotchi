"""Sparky Tamagotchi — ASCII art frames for all moods and actions."""

# Each frame is ~10 lines, consistent width
# Sparky: fluffy creature in bunny onesie with bunny slippers

FRAME_ECSTATIC = r"""
    💖  ✨  💕
   ╭─────────╮
   │  ◕ ▽ ◕  │
   ╰────┬────╯
    ╭───┴───╮
    │ bunny │
    │onesie!│
    ╰─┬───┬─╯
    d(👍)  (👍)b
"""

FRAME_HAPPY = r"""
      ✨  💕
   ╭─────────╮
   │  ◕ ‿ ◕  │
   ╰────┬────╯
    ╭───┴───╮
    │ bunny │
    │onesie!│
    ╰─┬───┬─╯
     d│   │b
"""

FRAME_CONTENT = r"""
        ~
   ╭─────────╮
   │  ◕ ◡ ◕  │
   ╰────┬────╯
    ╭───┴───╮
    │ bunny │
    │onesie!│
    ╰─┬───┬─╯
     d│   │b
"""

FRAME_SAD = r"""
        ·
   ╭─────────╮
   │  ◕ ︵ ◕  │
   ╰────┬────╯
    ╭───┴───╮
    │ bunny │
    │onesie…│
    ╰─┬───┬─╯
     d│   │b
"""

FRAME_MISERABLE = r"""

   ╭─────────╮
   │  ◕ ﹏ ◕  │
   ╰────┬────╯
    ╭───┴───╮
    │ bunny │
    │onesie…│
    ╰─┬───┬─╯
     d│   │b
"""

FRAME_EATING = r"""
    🍪 nom nom!
   ╭─────────╮
   │  ◕ ◡ ◕  │
   ╰────┬────╯
    ╭───┴───╮
    │ bunny │🍪
    │onesie!│
    ╰─┬───┬─╯
     d│   │b
"""

FRAME_PLAYING = r"""
    ✨ wheee! ✨
   ╭─────────╮
   │  ◕ ▽ ◕  │
   ╰────┬────╯
    ╭───┴───╮
    │ bunny │  🎀
    │onesie!│
    ╰─┬───┬─╯
      \│ │/
"""

FRAME_SLEEPING = r"""
      💤 z z z
   ╭─────────╮
   │  – ‿ –  │
   ╰────┬────╯
    ╭───┴───╮
    │ bunny │
    │onesie…│
    ╰─┬───┬─╯
     d│   │b
"""

FRAME_PETTED = r"""
    💕  💖  💕
   ╭─────────╮
   │  ◕ ▽ ◕  │
   ╰────┬────╯
    ╭───┴───╮
    │ bunny │
    │onesie!│
    ╰─┬───┬─╯
     d│   │b
"""

MOOD_FRAMES = {
    "ecstatic": FRAME_ECSTATIC,
    "happy": FRAME_HAPPY,
    "content": FRAME_CONTENT,
    "sad": FRAME_SAD,
    "miserable": FRAME_MISERABLE,
}

ACTION_FRAMES = {
    "eating": FRAME_EATING,
    "playing": FRAME_PLAYING,
    "sleeping": FRAME_SLEEPING,
    "petted": FRAME_PETTED,
    "treat": FRAME_EATING,
    "waking": FRAME_HAPPY,
}


def get_mood_frame(mood):
    """Return ASCII art for a mood string."""
    return MOOD_FRAMES.get(mood, FRAME_CONTENT)


def get_action_frame(action):
    """Return ASCII art for an action, or None if not an action frame."""
    return ACTION_FRAMES.get(action)


def get_idle_frame(state_dict):
    """Return the appropriate idle frame based on current state."""
    from state import get_mood
    if state_dict.get("sleeping"):
        return FRAME_SLEEPING
    mood = get_mood(state_dict)
    return get_mood_frame(mood)
