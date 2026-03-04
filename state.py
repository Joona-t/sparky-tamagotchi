"""Sparky Tamagotchi — state management, decay, persistence."""

import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sparky_data.json")

DEFAULT_STATE = {
    "name": "Sparky",
    "hunger": 80,
    "happiness": 80,
    "energy": 80,
    "last_interaction": None,
    "treats_today": 0,
    "treats_last_date": None,
    "age_days": 0,
    "created_at": None,
    "total_interactions": 0,
    "sleeping": False,
}

DECAY_RATES = {
    "hunger": 10.0,     # per hour
    "happiness": 5.0,
    "energy": 3.0,
}

SLEEP_DECAY_MULTIPLIER = 0.3
SLEEP_ENERGY_RECOVERY = 12.0  # per hour

MAX_TREATS_PER_DAY = 3

MOOD_THRESHOLDS = [
    (90, "ecstatic"),
    (70, "happy"),
    (50, "content"),
    (30, "sad"),
    (0, "miserable"),
]


def clamp(value, lo=0, hi=100):
    return max(lo, min(hi, value))


def now_iso():
    return datetime.now().isoformat()


def today_str():
    return datetime.now().strftime("%Y-%m-%d")


def load_state():
    if not os.path.exists(DATA_FILE):
        return create_fresh_state()
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        # Merge any missing keys from default
        for key, val in DEFAULT_STATE.items():
            if key not in data:
                data[key] = val
        return data
    except (json.JSONDecodeError, IOError):
        return create_fresh_state()


def create_fresh_state():
    state = dict(DEFAULT_STATE)
    now = now_iso()
    state["last_interaction"] = now
    state["created_at"] = now
    state["treats_last_date"] = today_str()
    return state


def save_state(state):
    with open(DATA_FILE, "w") as f:
        json.dump(state, f, indent=2)


def is_first_run():
    return not os.path.exists(DATA_FILE)


def apply_decay(state):
    """Apply time-based decay since last interaction. Mutates state in place."""
    if not state["last_interaction"]:
        return state

    try:
        last = datetime.fromisoformat(state["last_interaction"])
    except (ValueError, TypeError):
        state["last_interaction"] = now_iso()
        return state

    elapsed_hours = (datetime.now() - last).total_seconds() / 3600.0
    if elapsed_hours <= 0:
        return state

    sleeping = state.get("sleeping", False)

    if sleeping:
        # Energy recovers while sleeping
        state["energy"] = clamp(state["energy"] + SLEEP_ENERGY_RECOVERY * elapsed_hours)
        # Hunger and happiness decay at reduced rate
        state["hunger"] = clamp(state["hunger"] - DECAY_RATES["hunger"] * elapsed_hours * SLEEP_DECAY_MULTIPLIER)
        state["happiness"] = clamp(state["happiness"] - DECAY_RATES["happiness"] * elapsed_hours * SLEEP_DECAY_MULTIPLIER)
    else:
        for stat, rate in DECAY_RATES.items():
            state[stat] = clamp(state[stat] - rate * elapsed_hours)

    # Update age
    if state["created_at"]:
        try:
            created = datetime.fromisoformat(state["created_at"])
            state["age_days"] = (datetime.now() - created).days
        except (ValueError, TypeError):
            pass

    # Reset daily treats if new day
    if state.get("treats_last_date") != today_str():
        state["treats_today"] = 0
        state["treats_last_date"] = today_str()

    state["last_interaction"] = now_iso()
    return state


def get_health(state):
    """Derived health stat — never stored."""
    return round(state["hunger"] * 0.4 + state["happiness"] * 0.35 + state["energy"] * 0.25)


def get_mood(state):
    """Return mood string based on average of hunger, happiness, energy."""
    avg = (state["hunger"] + state["happiness"] + state["energy"]) / 3.0
    for threshold, mood in MOOD_THRESHOLDS:
        if avg >= threshold:
            return mood
    return "miserable"


def do_action(state, action):
    """Perform an action on Sparky. Returns (state, message)."""
    # Auto-wake on any action except sleep
    if state["sleeping"] and action != "sleep":
        state["sleeping"] = False

    state["total_interactions"] = state.get("total_interactions", 0) + 1

    if action == "feed":
        state["hunger"] = clamp(state["hunger"] + 30)
        state["last_interaction"] = now_iso()
        save_state(state)
        return state, "eating"

    elif action == "play":
        state["happiness"] = clamp(state["happiness"] + 25)
        state["energy"] = clamp(state["energy"] - 10)
        state["last_interaction"] = now_iso()
        save_state(state)
        return state, "playing"

    elif action == "sleep":
        if state["sleeping"]:
            return state, "already_sleeping"
        state["sleeping"] = True
        state["last_interaction"] = now_iso()
        save_state(state)
        return state, "sleeping"

    elif action == "wake":
        if not state["sleeping"]:
            return state, "already_awake"
        state["sleeping"] = False
        state["last_interaction"] = now_iso()
        save_state(state)
        return state, "waking"

    elif action == "pet":
        state["happiness"] = clamp(state["happiness"] + 10)
        state["last_interaction"] = now_iso()
        save_state(state)
        return state, "petted"

    elif action == "treat":
        if state["treats_today"] >= MAX_TREATS_PER_DAY:
            return state, "no_treats"
        state["hunger"] = clamp(state["hunger"] + 15)
        state["happiness"] = clamp(state["happiness"] + 15)
        state["energy"] = clamp(state["energy"] + 15)
        state["treats_today"] += 1
        state["last_interaction"] = now_iso()
        save_state(state)
        return state, "treat"

    return state, "unknown"
