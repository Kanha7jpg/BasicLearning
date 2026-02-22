# Snake Game

A classic Snake game built with Python's `turtle` graphics library.

## Requirements

- Python 3.x (no external libraries needed — `turtle` is included in the standard library)

## How to Run

```bash
python snake.py
```

## How to Play

When the game launches, you'll see the main menu. Select a difficulty to start:

| Key | Difficulty | Speed |
|-----|-----------|-------|
| `1` | Easy | Slow |
| `2` | Medium | Normal |
| `3` | Hard | Fast |

**Move the snake** using the arrow keys or WASD:

- `W` / `↑` — Move Up
- `S` / `↓` — Move Down
- `A` / `←` — Move Left
- `D` / `→` — Move Right

**Goal:** Eat the red food to grow your snake and increase your score. Each food item is worth **10 points**.

## Rules

- Don't hit the walls — the game ends if the snake goes out of bounds.
- Don't run into yourself — colliding with your own body ends the game.
- After a game over, the game returns to the menu automatically. Your high score is tracked for the session.

## Features

- Three difficulty levels
- Score and high score display
- Menu screen between rounds
- Grows in length with each food eaten