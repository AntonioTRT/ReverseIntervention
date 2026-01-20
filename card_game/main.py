"""
Main Entry Point
Clean initialization and launch of the party game with PyQt5 GUI.
"""

import sys
import os
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from PyQt5.QtWidgets import QApplication

from data_manager import DataManager
from game_logic import Game
from scoreboard import Scoreboard
from ui import GameUI


def main():
    """Main entry point for the application."""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    csv_path = script_dir / "questions.csv"

    # Initialize data manager
    try:
        data_manager = DataManager(str(csv_path))
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Reset all questions to unused state at startup
    data_manager.reset_all_questions()

    # Initialize game and scoreboard
    game = Game(data_manager)
    scoreboard = Scoreboard()

    # Create PyQt5 application
    app = QApplication(sys.argv)

    # Create and run UI
    ui = GameUI(game, scoreboard)
    ui.run()

    # Run the Qt application event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
