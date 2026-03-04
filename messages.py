"""Sparky Tamagotchi — cute messages, greetings, reactions."""

import random

WELCOME_MESSAGE = "Welcome to Sparky Tamagotchi! Your new pink buddy is here! 💕"

GREETING_MESSAGES = [
    "Sparky missed you! 💕",
    "Hey bestie! Sparky is happy to see you! ✨",
    "Welcome back! Sparky was waiting! 💖",
    "There you are! Sparky perks up! 🌸",
]

MOOD_MESSAGES = {
    "ecstatic": [
        "Sparky is feeling AMAZING! Stay sparkly! ✨",
        "Sparky is bursting with joy! 💖",
        "Peak vibes! Sparky is living their best life! 💕",
        "Sparky is doing double thumbs up! You're the best! 🌸",
    ],
    "happy": [
        "Sparky is feeling great! 💕",
        "Happy little Sparky! Everything is good! ✨",
        "Sparky is bouncing with joy! 💖",
        "Good vibes only! Sparky approves! 🌸",
    ],
    "content": [
        "Sparky is doing okay! Just chillin. ✨",
        "Calm and cozy! Sparky is content. 💕",
        "Sparky is relaxing in their bunny onesie. 🌸",
        "Peaceful Sparky energy right now. 💖",
    ],
    "sad": [
        "Sparky could use some love right now. 💕",
        "Sparky is a little down... maybe a snack? 🌸",
        "Sparky would love some attention. ✨",
        "A little play time would brighten Sparky's day! 💖",
    ],
    "miserable": [
        "Sparky really needs some care. 💕",
        "Poor Sparky... some food and love would help! 🌸",
        "Sparky is waiting for you. No rush, just whenever. ✨",
        "Sparky believes in you. A treat would be nice! 💖",
    ],
}

ACTION_MESSAGES = {
    "eating": [
        "Nom nom nom! Sparky loves food! 🍪",
        "Yummy! Sparky munches happily! 💕",
        "Sparky gobbles it up! So tasty! ✨",
    ],
    "playing": [
        "Wheee! Sparky is having so much fun! ✨",
        "Sparky bounces around happily! 🎀",
        "Playtime is the BEST time! 💕",
    ],
    "sleeping": [
        "Sparky curls up in their bunny onesie... 💤",
        "Shh... Sparky is sleeping peacefully. 🌙",
        "Sweet dreams, little Sparky! 💕",
    ],
    "petted": [
        "Sparky purrs softly! So happy! 💕",
        "Sparky nuzzles your hand! 💖",
        "Pat pat! Sparky loves pets! ✨",
    ],
    "treat": [
        "A treat! Sparky's eyes light up! 🍪✨",
        "Sparky does a happy dance for the treat! 💕",
        "Best. Treat. Ever! Sparky is thrilled! 💖",
    ],
    "waking": [
        "Sparky stretches and yawns! Good morning! ✨",
        "Sparky blinks awake! Ready for action! 💕",
        "Rise and shine, Sparky! 🌸",
    ],
    "already_sleeping": [
        "Shh! Sparky is already sleeping! 💤",
    ],
    "already_awake": [
        "Sparky is already wide awake! ✨",
    ],
    "no_treats": [
        "No more treats today! Sparky understands. 💕",
        "Treat limit reached! Gotta save some for tomorrow. 🌸",
    ],
}

LOW_STAT_HINTS = {
    "hunger": [
        "Sparky's tummy is rumbling... try 'feed'! 🍪",
        "A snack would really help right now! 💕",
    ],
    "happiness": [
        "Sparky could use some fun... try 'play' or 'pet'! ✨",
        "A little love goes a long way! 💖",
    ],
    "energy": [
        "Sparky is getting sleepy... try 'sleep'! 💤",
        "Maybe it's nap time? 🌙",
    ],
}


def get_greeting():
    return random.choice(GREETING_MESSAGES)


def get_mood_message(mood):
    pool = MOOD_MESSAGES.get(mood, MOOD_MESSAGES["content"])
    return random.choice(pool)


def get_action_message(action):
    pool = ACTION_MESSAGES.get(action, ["Sparky reacts! 💕"])
    return random.choice(pool)


def get_low_stat_hint(state):
    """Return a hint for the lowest stat below 30, or None."""
    stats = {"hunger": state["hunger"], "happiness": state["happiness"], "energy": state["energy"]}
    lowest_name = min(stats, key=stats.get)
    if stats[lowest_name] < 30:
        return random.choice(LOW_STAT_HINTS[lowest_name])
    return None
