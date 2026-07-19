# Lost in the Forest

A text-based adventure game written in Python. You wake up alone in a forest as the sun sets, with rumors of people disappearing at night — can you make it out before dark?

## How to Play

Run the game from your terminal:

```bash
python main.py
```

You'll be presented with a story and a numbered list of choices at each step. Type the number of your choice and press Enter to continue.

```
1. Look around the area
2. Follow the path
3. Save and quit

>
```

## Features

- **Branching story** — your choices shape the path through the forest, from the riverbank to a glowing cave.
- **Stats tracking** — keep an eye on your HP and Gold, shown at the top of every screen.
- **Item system** — find a sword in the cave that can help you survive a bear encounter later on.
- **Save & Quit** — save your progress at any decision point and pick up where you left off next time.
- **Tamper-proof saves** — save files are signed with an HMAC signature, so if the save file is edited by hand, the game will detect it and start fresh instead of loading corrupted or cheated data.
- **Scoring** — finish the game to get a score based on `Health left over + Gold - Deaths`.

## Story Path

1. **The Forest** — wake up and decide whether to explore or head straight for the path.
2. **The River** — a fast, dangerous river blocks your way. Jump it, or play it safe along the bank.
3. **The Cave** — shelter from the night (and any wolves) in a strange, glowing cave.
4. **The Chests** — two mysterious chests hold either gold or a nasty surprise.
5. **The Sword** — find a sword in the dark. Take it or leave it — the choice matters later.
6. **The Bear** — a giant silhouette blocks your path. Fight it (better with a sword) or make a run for it.
7. **The Village** — escape the forest and reach safety to complete the game.

## Requirements

- Python 3.6+
- No external dependencies (uses only the standard library: `hashlib`, `hmac`, `json`, `os`)

## Save Files

Progress is saved to `save.json` in the same directory as the game. On startup, if a save file is found, you'll be asked whether to load it or start a new game.

## Death & Restart

If your HP drops to 0 or below, it's game over — your death count goes up, and you restart from the beginning of the forest with your gold reset. Your sword and progress are lost, but the story remembers how many times you've fallen.
