# Sparky Tamagotchi

A terminal Tamagotchi featuring Sparky, the LoveSpark mascot. A cute pink buddy that lives alongside your coding sessions.

No guilt, no death — just a fluffy friend in a bunny onesie.

## Install

Requires Python 3.11+ and `rich`:

```bash
pip install rich
```

## Usage

```
python3 sparky.py              # Quick status check
python3 sparky.py feed         # Feed Sparky (+hunger)
python3 sparky.py play         # Play with Sparky (+happiness, -energy)
python3 sparky.py sleep        # Put Sparky to sleep (+energy over time)
python3 sparky.py wake         # Wake up Sparky
python3 sparky.py pet          # Pet Sparky (+happiness)
python3 sparky.py treat        # Give a treat (all stats +15, 3/day)
python3 sparky.py watch        # Live dashboard mode
python3 sparky.py help         # Show commands
```

### Shell Alias

Add to your `.zshrc` or `.bashrc`:

```bash
alias sparky='python3 ~/Apps\ \&\ Tools/sparky-tamagotchi/sparky.py'
```

Then just use `sparky`, `sparky feed`, `sparky watch`, etc.

## How It Works

- **Stats** (hunger, happiness, energy) range from 0–100
- **Health** is derived from the other three stats
- **Decay** happens passively based on time since last interaction — no background process
- **Sleep mode** recovers energy while reducing hunger/happiness decay
- **Treats** are limited to 3 per day
- **Moods** change based on average stats: ecstatic, happy, content, sad, miserable
- Stats can hit 0 but Sparky never dies — just gets very sad

## Files

| File | Purpose |
|------|---------|
| `sparky.py` | CLI entry point |
| `state.py` | State management, decay, persistence |
| `art.py` | ASCII art frames (5 moods + 4 actions) |
| `messages.py` | Cute messages and reactions |
| `ui.py` | Rich terminal rendering |
| `sparky_data.json` | Auto-created save file |

## Part of LoveSpark

MIT License — free, no ads, no data collection.
