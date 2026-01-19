# Quick Start Guide

## 5-Minute Setup

### 1. Navigate to Project
```bash
cd card_game
```

### 2. Run the Game
```bash
python main.py
```

That's it! The Tkinter GUI will launch.

## First Game

1. Click "New Game"
2. Enter your player name
3. Choose number of rounds (default: 10)
4. Click "Start Game"
5. Read the question displayed
6. Click "Correct" or "Incorrect" based on the right answer
7. Watch your score accumulate
8. View results when game ends

## Running Tests

```bash
# Install test dependency (one time)
pip install pytest

# Run tests
python -m pytest tests/ -v
```

Expected output: All tests pass ✓

## Common Tasks

### Add More Questions
Edit `questions.csv` and add rows:
```csv
21,2,3,False,What is Einstein's E=mc²?
22,3,2,False,What is photosynthesis?
```

Then reload the game - new questions will be available!

### View Leaderboard
Click "View Leaderboard" from welcome screen or File menu.

### Start New Game
Click "File" → "New Game" anytime.

## Project Files Overview

| File | Purpose |
|------|---------|
| `main.py` | Start here - launches the game |
| `game_logic.py` | Brain of the game - the logic |
| `data_manager.py` | Reads/writes questions.csv |
| `scoreboard.py` | Tracks player scores |
| `ui.py` | Visual interface (Tkinter) |
| `questions.csv` | All the questions - easy to edit |
| `README.md` | Full documentation |
| `ARCHITECTURE.md` | How it's built |

## Troubleshooting

**Game won't start?**
- Make sure `questions.csv` is in the same folder as `main.py`
- Check Python is version 3.7+: `python --version`

**Tkinter missing?**
- Windows: `pip install tk`
- Mac: Download from python.org
- Linux: `sudo apt-get install python3-tk`

**Tests failing?**
- Install pytest: `pip install pytest`
- Run from project root: `python -m pytest tests/ -v`

## Customization Ideas (5 minutes)

### Change Question Topics
Edit `questions.csv` - add your own questions!

### Add More Categories
Edit category numbers in CSV (1, 2, 3, 4, 5...)
They work automatically - no code changes needed!

### Modify Point Values
In `ui.py`, find this line:
```python
self.scoreboard.add_points(self.current_player, 10)
```
Change `10` to any points value you want.

### Change Game Rounds
In the "New Game" dialog, the rounds can be set 1-50.

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [ARCHITECTURE.md](ARCHITECTURE.md) to understand design
- Explore [tests/test_game.py](tests/test_game.py) for code examples
- Modify `questions.csv` with your own questions
- Try extending with features from README.md suggestions

## One Command to Rule Them All

```bash
python main.py
```

🎮 **Happy gaming!**
