# Card-Based Question Game

A modular, scalable board game project built in Python featuring a card-based question game with a clean separation of concerns. The architecture ensures the game logic is completely UI-agnostic and can be reused across different platforms.

## Project Features

- ✅ **Modular Architecture**: Clean separation between data, logic, UI, and scoring
- ✅ **CSV-Based Question Storage**: Easy to manage and extend questions
- ✅ **Multiple UI Support**: Built with Tkinter, easily extensible to web/mobile
- ✅ **Comprehensive Scoring System**: Track player stats, accuracy, and leaderboards
- ✅ **Flexible Game Logic**: Support for categories, difficulty levels, and filtering
- ✅ **Full Test Coverage**: Example unit tests for all major components
- ✅ **Well-Documented**: Extensive docstrings and comments throughout

## Project Structure

```
card_game/
├── questions.csv              # Question database
├── data_manager.py           # CSV handling and data operations
├── game_logic.py             # Core game mechanics (UI-independent)
├── scoreboard.py             # Player scoring system
├── ui.py                     # Tkinter GUI interface
├── main.py                   # Application entry point
└── tests/
    ├── __init__.py
    └── test_game.py          # Unit tests
```

## Installation

### Prerequisites

- Python 3.7+
- tkinter (usually comes with Python)
- pytest (for running tests)

### Setup

1. **Navigate to the project directory**:
   ```bash
   cd card_game
   ```

2. **Install test dependencies** (optional):
   ```bash
   pip install pytest
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

### Running the Game

Simply execute:
```bash
python main.py
```

The application will:
- Load questions from `questions.csv`
- Initialize the game engine and scoreboard
- Launch the Tkinter GUI

### In-Game Flow

1. **Welcome Screen**: Start with new game or view leaderboard
2. **New Game Dialog**: Enter player name and select number of rounds
3. **Game Screen**: 
   - Question is displayed with category and difficulty
   - Mark answer as correct/incorrect
   - Progress bar shows game advancement
4. **Game Over Screen**: View results and stats

### Question CSV Format

Each row in `questions.csv` represents a question card:

```csv
id,category,difficulty,used,question
1,1,1,False,What is the capital of France?
2,1,2,False,Who wrote 'Romeo and Juliet'?
```

**Columns**:
- `id`: Unique identifier (integer)
- `category`: Category ID (1-N, e.g., Geography=1, Science=2)
- `difficulty`: Difficulty level (1-3, where 1=easy, 2=medium, 3=hard)
- `used`: Boolean flag (True/False) indicating if question has been used
- `question`: The question text

## Module Documentation

### 1. `data_manager.py`

**Purpose**: Handle all CSV operations and question data persistence.

**Key Classes**:
- `DataManager`: Main class for data operations

**Key Methods**:
```python
load_questions()                           # Load all questions from CSV
save_questions()                           # Save questions back to CSV
get_all_questions()                        # Get all questions
get_question_by_id(id)                     # Retrieve specific question
get_unused_questions()                     # Get questions not yet played
get_questions_by_category(category)        # Filter by category
get_questions_by_difficulty(difficulty)   # Filter by difficulty
get_random_question(category, difficulty)  # Get random question with filters
mark_question_used(id)                     # Mark question as used
reset_all_questions()                      # Reset used status
get_statistics()                           # Get database stats
```

**Example Usage**:
```python
from data_manager import DataManager

dm = DataManager("questions.csv")
unused = dm.get_unused_questions()
random_q = dm.get_random_question(category=1, difficulty=2)
dm.mark_question_used(1)
dm.save_questions()
```

### 2. `game_logic.py`

**Purpose**: Core game mechanics completely independent from any UI.

**Key Classes**:
- `GameState`: Manages individual game session state
- `GameEngine`: High-level orchestration of game flow

**Key Methods**:
```python
# GameEngine
new_game(max_rounds)                       # Start new game
play_round(category, difficulty)           # Draw question for round
submit_round(is_correct)                   # Process answer
get_game_stats()                           # Get performance metrics
get_available_categories()                 # List available categories
get_available_difficulties()               # List difficulty levels
```

**Example Usage**:
```python
from game_logic import GameEngine
from data_manager import DataManager

dm = DataManager("questions.csv")
engine = GameEngine(dm)
engine.new_game(max_rounds=10)

question = engine.play_round(category=1)
print(question['question'])

result = engine.submit_round(is_correct=True)
stats = engine.get_game_stats()
```

### 3. `scoreboard.py`

**Purpose**: Track player scores and statistics.

**Key Classes**:
- `Player`: Individual player with stats
- `Scoreboard`: Manages multiple players

**Key Methods**:
```python
# Scoreboard
add_player(name)                           # Add player
remove_player(name)                        # Remove player
add_points(name, points)                   # Add points
record_correct_answer(name)                # Track correct answer
record_incorrect_answer(name)              # Track incorrect answer
record_game_completed(name)                # Record game completion
get_scores(sort_by)                        # Get all scores sorted
get_player_stats(name)                     # Get player statistics
get_leaderboard(top_n)                     # Get top N players
```

**Example Usage**:
```python
from scoreboard import Scoreboard

sb = Scoreboard()
sb.add_player("Alice")
sb.add_points("Alice", 50)
sb.record_correct_answer("Alice")

leaderboard = sb.get_leaderboard(top_n=10)
for player in leaderboard:
    print(f"{player['name']}: {player['score']} pts")
```

### 4. `ui.py`

**Purpose**: Tkinter-based graphical user interface.

**Key Classes**:
- `CardGameUI`: Main UI controller

**Key Methods**:
```python
show_welcome_screen()                      # Display welcome
show_new_game_dialog()                     # New game dialog
show_game_screen()                         # Main game interface
show_game_over_screen()                    # Results screen
show_leaderboard()                         # Leaderboard view
run()                                      # Start event loop
```

**Design Note**: UI calls game logic functions but contains no game logic itself. This allows the game to be integrated with other UI frameworks (web, mobile) without changes to core logic.

### 5. `main.py`

**Purpose**: Application entry point with initialization.

**Functionality**:
- Loads questions from CSV
- Initializes game engine and scoreboard
- Launches the UI

**To run**:
```bash
python main.py
```

## API Reference for Developers

### Creating a Custom UI (e.g., Web, Mobile)

The game logic is completely UI-agnostic. Here's how to create a new UI:

```python
from game_logic import GameEngine
from data_manager import DataManager
from scoreboard import Scoreboard

# Initialize
dm = DataManager("questions.csv")
engine = GameEngine(dm)
scoreboard = Scoreboard()

# Game flow (framework-agnostic)
scoreboard.add_player("Player1")
engine.new_game(max_rounds=10)

# Game loop
question = engine.play_round(category=1)
# ... display question in your UI ...
user_answer = get_answer_from_user()  # Your UI handler
is_correct = validate_answer(user_answer)

result = engine.submit_round(is_correct)
scoreboard.add_points("Player1", 10 if is_correct else 0)
```

## Running Tests

### Prerequisites

```bash
pip install pytest
```

### Execute Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_game.py -v

# Run with coverage
pip install pytest-cov
python -m pytest tests/ --cov=. -v
```

### Test Coverage

The `tests/test_game.py` file includes tests for:
- **DataManager**: Loading, filtering, marking questions
- **Player**: Points, stats, accuracy calculations
- **Scoreboard**: Player management, leaderboard
- **GameLogic**: Game flow, round submission, statistics

Example test:
```python
def test_mark_question_used(self, temp_csv):
    dm = DataManager(temp_csv)
    dm.mark_question_used(1)
    question = dm.get_question_by_id(1)
    assert question['used'] is True
```

## Extension Ideas

### 1. **Timer Feature**
Add time limits to questions:
```python
class TimedQuestion(GameState):
    def draw_card(self, time_limit=30):
        # Draw card with timer
        # Auto-mark as incorrect if time expires
```

### 2. **Multiplayer Modes**
Extend game logic to support:
- Turn-based play
- Simultaneous play with team scoring
- Competitive leaderboards

### 3. **Question Categories**
Define and display categories:
```python
CATEGORIES = {
    1: "Geography",
    2: "Science",
    3: "History",
    4: "Literature"
}
```

### 4. **Statistics Export**
Export player stats to JSON/CSV:
```python
def export_stats(self, filename):
    with open(filename, 'w') as f:
        json.dump(self.get_scores(), f)
```

### 5. **Web UI with Flask**
Replace Tkinter with web interface:
```python
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/api/question')
def get_question():
    q = engine.play_round()
    return jsonify(q)
```

### 6. **Mobile App with Kivy**
Create mobile version using Kivy framework while reusing game logic.

### 7. **Advanced Scoring Rules**
Implement bonus systems:
- Difficulty multipliers
- Streak bonuses
- Speed bonuses

### 8. **Question Hints**
Add hint system:
```python
class Question:
    def get_hint(self):
        # Return partial answer or clue
```

### 9. **Difficulty Progression**
Automatically adjust difficulty:
```python
def get_adaptive_difficulty(self, player_accuracy):
    if player_accuracy > 80:
        return 3  # Hard
    elif player_accuracy > 50:
        return 2  # Medium
    else:
        return 1  # Easy
```

### 10. **Question Editor UI**
Add interface to create and modify questions:
```python
class QuestionEditorUI:
    def add_question(self, category, difficulty, text):
        # Add new question and save
```

## Design Principles

### Separation of Concerns
- **data_manager.py**: Data persistence only
- **game_logic.py**: Game mechanics only
- **scoreboard.py**: Scoring logic only
- **ui.py**: Presentation only

### UI-Agnostic Design
Game logic contains no UI calls and no UI frameworks. This enables:
- Easy testing without UI
- Multiple UI implementations
- Command-line or headless usage

### Extensibility
- New categories and difficulties supported automatically
- Easy to add new scoring rules
- Questions stored in simple CSV format
- Modular class design allows inheritance and customization

## Troubleshooting

### Issue: "questions.csv not found"
**Solution**: Ensure `questions.csv` is in the same directory as `main.py`.

### Issue: "No module named tkinter"
**Solution**: Install tkinter:
- Windows: Usually included. Run `pip install tk`
- Linux: `sudo apt-get install python3-tk`
- macOS: Install from https://www.python.org/downloads/

### Issue: Tests fail with import errors
**Solution**: Run tests from the card_game directory:
```bash
cd card_game
python -m pytest tests/ -v
```

## Performance Considerations

- CSV loaded entirely into memory for fast access
- For large question databases (10,000+), consider:
  - Database instead of CSV
  - Lazy loading and pagination
  - Question caching

## Security Notes

- CSV file writable by the application - consider permissions
- For production, validate all user inputs
- Implement player authentication if needed
- Sanitize question text if from untrusted sources

## License

This project is provided as-is for educational purposes.

## Contributing

To extend this project:
1. Follow the existing code style
2. Add docstrings to new functions
3. Include unit tests for new features
4. Update this README with new capabilities

## Version History

- **v1.0** (Initial Release)
  - Core game mechanics
  - CSV-based questions
  - Tkinter UI
  - Scoring system
  - Unit tests

---

**Built with ❤️ for extensibility and clean code practices.**
