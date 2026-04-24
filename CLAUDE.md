# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

"你画我猜" (Draw & Guess) — a Python/Tkinter desktop drawing and guessing game with two modes.

## Tech Stack

- Python 3.x + Tkinter (built-in GUI)
- Pillow for image handling and sketch generation
- PyInstaller for exe packaging

## Build & Run

```bash
python main.py                    # Run the game
python generate_sketches.py       # Regenerate sketch images
pyinstaller --onefile --windowed --name DrawAndGuess main.py  # Package as exe
```

## Architecture

```
main.py              → Entry point, launches App
game/
  app.py             → Main window, home screen, mode navigation
  canvas.py          → DrawingCanvas widget (freehand, colors, undo, clear, export)
  mode_draw.py       → 我画电脑猜: player draws on canvas, AI guesses (random)
  mode_guess.py      → 电脑画我猜: loads sketch from assets/, player types guess
  timer.py           → CountdownTimer using Tkinter after()
  scoring.py         → ScoreManager (base + time bonus + streak)
  words.py           → Word list grouped by category, hint generator
assets/sketches/     → 20 pre-generated PNG sketches (猫, 狗, 鱼, 太阳, etc.)
generate_sketches.py → Script to regenerate sketch images using Pillow
```

## Key Patterns

- `App` owns the root `Tk()` and manages frame transitions via `_clear_frame()` / `_show_*()`
- Game modes (`DrawMode`, `GuessMode`) are `tk.Frame` subclasses; they receive `score_mgr` and `on_back` callback
- `DrawingCanvas` manages its own off-screen PIL Image for export and a stroke stack for undo
- Timer uses `root.after()` — always call `timer.stop()` before leaving a mode

## Constraints

- Software installations must NOT go to the C: drive
- AI guessing uses simple random selection (no ML model)
- AI drawings are local pre-stored PNGs in `assets/sketches/`
