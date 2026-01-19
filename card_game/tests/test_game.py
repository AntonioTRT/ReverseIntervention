"""
Unit Tests for Party Question Game
Run with: python -m pytest tests/ -v
"""

import pytest
import tempfile
import csv
from pathlib import Path

from data_manager import DataManager
from game_logic import Player, Game
from scoreboard import Scoreboard, Event


class TestPlayer:
    """Tests for Player class."""

    def test_player_creation(self):
        """Test creating a player."""
        player = Player("Alice")
        assert player.name == "Alice"
        assert player.strikes == 0
        assert player.has_block_card is True
        assert player.is_active is True
        assert player.drinks_consumed == 0

    def test_add_strike(self):
        """Test adding strikes."""
        player = Player("Bob")
        strikes = player.add_strike()
        assert strikes == 1
        strikes = player.add_strike()
        assert strikes == 2

    def test_must_drink_threshold(self):
        """Test must drink threshold (3 strikes)."""
        player = Player("Carol")
        player.add_strike()
        assert not player.must_drink()
        player.add_strike()
        assert not player.must_drink()
        player.add_strike()
        assert player.must_drink()

    def test_drink_resets_strikes(self):
        """Test that drinking resets strikes."""
        player = Player("Dave")
        player.add_strike()
        player.add_strike()
        player.add_strike()
        player.drink()
        assert player.strikes == 0
        assert player.drinks_consumed == 1

    def test_block_card_usage(self):
        """Test block card usage."""
        player = Player("Eve")
        assert player.has_block_card is True
        used = player.use_block_card()
        assert used is True
        assert player.has_block_card is False
        used = player.use_block_card()
        assert used is False

    def test_clock_out(self):
        """Test clocking out."""
        player = Player("Frank")
        player.clock_out()
        assert player.is_active is False

    def test_player_status(self):
        """Test getting player status."""
        player = Player("Grace")
        player.add_strike()
        player.use_block_card()
        status = player.get_status()
        assert status['name'] == "Grace"
        assert status['strikes'] == 1
        assert status['has_block_card'] is False
        assert status['is_active'] is True


class TestDataManager:
    """Tests for DataManager class."""

    @pytest.fixture
    def temp_csv(self):
        """Create a temporary CSV file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'question', 'category', 'difficulty', 'used', 'correct_answer'])
            writer.writeheader()
            writer.writerows([
                {'id': '1', 'question': 'Q1?', 'category': '1', 'difficulty': '1', 'used': 'False', 'correct_answer': 'Yes'},
                {'id': '2', 'question': 'Q2?', 'category': '1', 'difficulty': '2', 'used': 'False', 'correct_answer': 'No'},
                {'id': '3', 'question': 'Q3?', 'category': '2', 'difficulty': '1', 'used': 'False', 'correct_answer': 'Yes'},
            ])
            temp_path = f.name
        yield temp_path
        Path(temp_path).unlink()

    def test_load_questions(self, temp_csv):
        """Test loading questions from CSV."""
        dm = DataManager(temp_csv)
        assert dm.get_total_count() == 3

    def test_get_unused_questions(self, temp_csv):
        """Test getting unused questions."""
        dm = DataManager(temp_csv)
        unused = dm.get_unused_questions()
        assert len(unused) == 3

    def test_mark_question_used(self, temp_csv):
        """Test marking a question as used."""
        dm = DataManager(temp_csv)
        dm.mark_question_used(1)
        unused = dm.get_unused_questions()
        assert len(unused) == 2

    def test_get_random_unused_question(self, temp_csv):
        """Test getting random unused question."""
        dm = DataManager(temp_csv)
        question = dm.get_random_unused_question()
        assert question is not None
        assert 'question' in question

    def test_reset_all_questions(self, temp_csv):
        """Test resetting all questions."""
        dm = DataManager(temp_csv)
        dm.mark_question_used(1)
        dm.mark_question_used(2)
        dm.reset_all_questions()
        unused = dm.get_unused_questions()
        assert len(unused) == 3

    def test_get_unused_count(self, temp_csv):
        """Test getting unused question count."""
        dm = DataManager(temp_csv)
        assert dm.get_unused_count() == 3
        dm.mark_question_used(1)
        assert dm.get_unused_count() == 2


class TestScoreboard:
    """Tests for Scoreboard class."""

    def test_scoreboard_creation(self):
        """Test creating a scoreboard."""
        sb = Scoreboard()
        assert len(sb.events) == 0

    def test_record_strike(self):
        """Test recording a strike."""
        sb = Scoreboard()
        sb.record_strike("Alice", 1, False)
        assert len(sb.events) == 1
        assert sb.get_player_strikes("Alice") == 1

    def test_record_drink(self):
        """Test recording a drink."""
        sb = Scoreboard()
        sb.record_drink("Bob", 1)
        assert len(sb.events) == 1
        assert sb.get_player_drinks("Bob") == 1

    def test_record_clock_out(self):
        """Test recording clock out."""
        sb = Scoreboard()
        sb.record_clock_out("Carol", 5)
        assert len(sb.events) == 1

    def test_get_events_by_player(self):
        """Test getting events by player."""
        sb = Scoreboard()
        sb.record_strike("Dave", 1, False)
        sb.record_strike("Alice", 1, False)
        dave_events = sb.get_events_by_player("Dave")
        assert len(dave_events) == 1

    def test_get_summary(self):
        """Test getting summary."""
        sb = Scoreboard()
        sb.record_strike("Eve", 1, False)
        sb.record_drink("Eve", 1)
        summary = sb.get_summary()
        assert summary['total_events'] == 2
        assert summary['total_strike_events'] == 1
        assert summary['total_drinking_events'] == 1


class TestGame:
    """Tests for Game class."""

    @pytest.fixture
    def game_setup(self):
        """Set up game for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'question', 'category', 'difficulty', 'used', 'correct_answer'])
            writer.writeheader()
            for i in range(1, 6):
                writer.writerow({
                    'id': str(i),
                    'question': f'Q{i}?',
                    'category': '1',
                    'difficulty': '1',
                    'used': 'False',
                    'correct_answer': 'Yes' if i % 2 == 0 else 'No'
                })
            temp_path = f.name
        
        dm = DataManager(temp_path)
        game = Game(dm)
        yield game
        Path(temp_path).unlink()

    def test_game_initialization(self, game_setup):
        """Test initializing game."""
        game = game_setup
        names = ["Alice", "Bob"]
        game.initialize_players(names)
        assert len(game.players) == 2
        assert game.is_game_active is True

    def test_get_active_players(self, game_setup):
        """Test getting active players."""
        game = game_setup
        game.initialize_players(["Alice", "Bob"])
        active = game.get_active_players()
        assert len(active) == 2
        active[0].clock_out()
        active = game.get_active_players()
        assert len(active) == 1

    def test_select_random_player(self, game_setup):
        """Test selecting random player."""
        game = game_setup
        game.initialize_players(["Alice", "Bob"])
        player = game.select_random_player()
        assert player is not None
        assert player.is_active

    def test_draw_question(self, game_setup):
        """Test drawing question."""
        game = game_setup
        game.initialize_players(["Alice"])
        question = game.draw_question()
        assert question is not None
        assert game.current_question is not None

    def test_player_answers_correct(self, game_setup):
        """Test player answering correctly - should add strike."""
        game = game_setup
        game.initialize_players(["Alice"])
        player = game.players[0]
        game.draw_question()
        
        # Get the correct answer for the current question
        correct_answer = game.current_question['correct_answer']
        
        # Player answers correctly
        result = game.player_answers(player, answered_yes=correct_answer)
        
        assert result['is_correct'] is True
        assert result['answered_yes'] == correct_answer
        assert result['correct_answer'] == correct_answer
        assert player.strikes == 1  # Strike should be added

    def test_player_answers_incorrect(self, game_setup):
        """Test player answering incorrectly - should NOT add strike."""
        game = game_setup
        game.initialize_players(["Alice"])
        player = game.players[0]
        game.draw_question()
        
        # Get the correct answer for the current question
        correct_answer = game.current_question['correct_answer']
        incorrect_answer = not correct_answer  # Answer the opposite
        
        # Player answers incorrectly
        result = game.player_answers(player, answered_yes=incorrect_answer)
        
        assert result['is_correct'] is False
        assert result['answered_yes'] == incorrect_answer
        assert result['correct_answer'] == correct_answer
        assert player.strikes == 0  # Strike should NOT be added

    def test_player_answers_triggers_drink(self, game_setup):
        """Test that 3 correct answers trigger drinking."""
        game = game_setup
        game.initialize_players(["Alice"])
        player = game.players[0]
        
        # Get three questions and answer correctly
        for _ in range(3):
            game.draw_question()
            correct_answer = game.current_question['correct_answer']
            result = game.player_answers(player, answered_yes=correct_answer)
            
            if player.must_drink():
                player.drink()
                break
        
        assert player.drinks_consumed == 1
        assert player.strikes == 0  # Should reset after drinking

    def test_is_game_over(self, game_setup):
        """Test game over condition."""
        game = game_setup
        game.initialize_players(["Alice", "Bob"])
        assert not game.is_game_over()
        game.players[0].clock_out()
        assert game.is_game_over()

    def test_use_block_card(self, game_setup):
        """Test using block card."""
        game = game_setup
        game.initialize_players(["Alice", "Bob", "Carol"])
        game.select_random_player()
        blocker = game.players[0]
        target = game.use_block_card(blocker)
        assert target is not None
        assert not blocker.has_block_card

    def test_player_clock_out(self, game_setup):
        """Test player clocking out."""
        game = game_setup
        game.initialize_players(["Alice", "Bob"])
        player = game.players[0]
        game.player_clock_out(player)
        assert not player.is_active


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
