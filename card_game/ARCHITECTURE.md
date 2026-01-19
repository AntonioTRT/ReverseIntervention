# Architecture Guide

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Application                          │
├─────────────────────────────────────────────────────────────┤
│                        main.py                               │
│              (Initialization & Startup)                      │
└────────────┬────────────────────┬────────────────────────────┘
             │                    │
    ┌────────▼─────────┐  ┌──────▼──────────┐
    │   UI Layer       │  │  Game Engines   │
    │   (ui.py)        │  │  (game_logic.py)│
    │   • Tkinter      │  │  • GameState    │
    │   • Events       │  │  • GameEngine   │
    │   • Display      │  │  • Core Logic   │
    └────────┬─────────┘  └──────┬──────────┘
             │                   │
             └───────┬───────────┘
                     │
         ┌───────────▼────────────┐
         │  Data & Logic Layers   │
         ├────────────────────────┤
         │  1. DataManager        │ ◄─── CSV File
         │     (data_manager.py)  │      (questions.csv)
         │     • Load/Save        │
         │     • Query/Filter     │
         │     • Persistence      │
         │                        │
         │  2. Scoreboard         │
         │     (scoreboard.py)    │
         │     • Player Tracking  │
         │     • Score Management │
         │     • Leaderboards     │
         └────────────────────────┘
```

## Data Flow

### Game Initialization
```
main.py
  ↓
├─ Load questions.csv → DataManager
├─ Initialize GameEngine (with DataManager)
├─ Initialize Scoreboard
└─ Launch CardGameUI
```

### Game Round Flow
```
UI (show_game_screen)
  ↓
engine.play_round()
  ↓
GameEngine.draw_card()
  ↓
GameState.draw_card()
  ↓
DataManager.get_random_question()
  ↓
Display question to user
  ↓
User submits answer
  ↓
engine.submit_round(is_correct)
  ↓
GameState.submit_answer()
  ↓
DataManager.mark_question_used() & save()
  ↓
Scoreboard.add_points() / record_answer()
  ↓
Update UI with results
```

## Module Dependencies

```
main.py
├── data_manager.py
├── game_logic.py (depends on data_manager)
├── scoreboard.py
└── ui.py (depends on game_logic, scoreboard)

tests/
└── test_game.py (imports all modules)
```

## Key Design Patterns

### 1. **Separation of Concerns**
Each module has a single responsibility:
- **data_manager.py**: Data I/O only
- **game_logic.py**: Game mechanics only
- **scoreboard.py**: Score tracking only
- **ui.py**: Presentation only

### 2. **Dependency Injection**
```python
# UI receives dependencies rather than creating them
ui = CardGameUI(game_engine, scoreboard)
```

This enables:
- Easy testing (mock dependencies)
- Easy UI swapping (same game engine with different UI)
- Loose coupling between modules

### 3. **Model-View Separation**
- **Models**: GameState, Player, Question (data containers)
- **Controllers**: GameEngine (business logic)
- **Views**: CardGameUI (presentation)

### 4. **Factory Pattern**
DataManager loads and manages Question objects:
```python
def get_random_question(self):
    # Returns fully formed question object
```

## Class Hierarchy

```
DataManager
├── Attributes: csv_path, questions[]
├── Methods:
│   ├── load_questions()
│   ├── save_questions()
│   ├── get_random_question()
│   ├── mark_question_used()
│   └── ... (filtering methods)

GameEngine
├── Attributes: data_manager, game_state, game_history[]
├── Methods:
│   ├── new_game()
│   ├── play_round()
│   ├── submit_round()
│   └── get_game_stats()

GameState
├── Attributes: current_question, current_round
├── Methods:
│   ├── start_game()
│   ├── draw_card()
│   ├── submit_answer()
│   └── is_game_over()

Scoreboard
├── Attributes: players{}
├── Methods:
│   ├── add_player()
│   ├── add_points()
│   ├── get_leaderboard()
│   └── ... (player management)

Player
├── Attributes: name, score, stats
├── Methods:
│   ├── add_points()
│   ├── get_accuracy()
│   └── ... (stat methods)

CardGameUI
├── Attributes: game_engine, scoreboard, root
├── Methods:
│   ├── show_game_screen()
│   ├── show_leaderboard()
│   └── ... (UI methods)
```

## Extension Points

### Adding a Web UI
```
web_ui.py (Flask)
├── Uses GameEngine (same)
├── Uses Scoreboard (same)
├── Provides REST API
└── Renders HTML templates
```

### Adding a Mobile UI
```
mobile_ui.py (Kivy)
├── Uses GameEngine (same)
├── Uses Scoreboard (same)
├── Provides touch interface
└── Uses Kivy widgets
```

### Adding Database Storage
```
database_manager.py (SQLAlchemy)
├── Replaces DataManager
├── Reads from database instead of CSV
├── Provides same interface
└── GameEngine unchanged
```

### Adding Difficulty Adaptation
```
game_logic.py (Enhanced)
├── Add AdaptiveGameEngine(GameEngine)
├── Override play_round()
├── Calculate difficulty dynamically
└── No UI changes needed
```

## Performance Characteristics

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Load questions | O(n) | n = # questions |
| Get random question | O(n) | Could optimize with indexing |
| Mark question used | O(n) | Linear search, could use dict |
| Save to CSV | O(n) | Sequential write |
| Get player stats | O(1) | Direct lookup |
| Get leaderboard | O(n log n) | Sorting required |

**Optimization Opportunities**:
- Use dictionary for question lookup by ID
- Index questions by category/difficulty
- Lazy load questions (pagination)
- Cache frequently accessed data

## Thread Safety

Current implementation is **not thread-safe**:
- CSV operations are not atomic
- No locks on shared data
- Suitable for single-player games

For multiplayer servers, consider:
- Database transactions (atomic operations)
- Locking mechanisms
- Queue-based processing

## Error Handling Strategy

| Layer | Errors | Handling |
|-------|--------|----------|
| data_manager | File I/O errors | Raise ValueError/IOError |
| game_logic | No game errors | Returns None on invalid state |
| scoreboard | Invalid player names | Return False on failure |
| ui | All exceptions | Show messageboxes, continue |

## Testing Strategy

```
Unit Tests (test_game.py)
├── DataManager tests
│   ├── Load/save operations
│   ├── Query/filtering
│   └── State management
├── GameLogic tests
│   ├── Game initialization
│   ├── Round submission
│   └── Game completion
├── Scoreboard tests
│   ├── Player management
│   ├── Score calculations
│   └── Leaderboard generation
└── Integration tests
    └── Full game flow
```

Run with: `pytest tests/ -v`

## Configuration & Constants

Consider centralizing constants:
```python
# config.py
CATEGORIES = {
    1: "Geography",
    2: "Science",
    3: "History"
}

DIFFICULTIES = {
    1: "Easy",
    2: "Medium",
    3: "Hard"
}

POINTS_PER_QUESTION = 10
```

## Deployment Considerations

### Standalone Executable
```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

### Docker Container
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
CMD ["python", "main.py"]
```

### As a Library
```python
# games/card_game/__init__.py
from game_logic import GameEngine
from data_manager import DataManager
# Expose public API
```

---

This architecture prioritizes:
- **Modularity**: Each component is independent
- **Testability**: No hidden dependencies
- **Extensibility**: Easy to add features
- **Maintainability**: Clear structure and responsibilities
