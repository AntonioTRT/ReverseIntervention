"""
Game Logic Module
Contains core game mechanics independent from UI.
Manages players, strikes, block cards, and game flow.
"""

from typing import List, Optional, Dict, Any
from data_manager import DataManager
import random


class Player:
    """Represents a player in the party game."""

    def __init__(self, name: str):
        """
        Initialize a player.

        Args:
            name (str): The player's name.
        """
        self.name = name
        self.strikes = 0
        self.has_block_card = True
        self.is_active = True
        self.drinks_consumed = 0

    def add_strike(self) -> int:
        """
        Add a strike to the player.
        Returns total strikes.

        Returns:
            int: Current number of strikes.
        """
        self.strikes += 1
        return self.strikes

    def reset_strikes(self) -> None:
        """Reset strikes to 0 (after drinking)."""
        self.strikes = 0

    def use_block_card(self) -> bool:
        """
        Use the player's block card.

        Returns:
            bool: True if block card was available and used, False otherwise.
        """
        if self.has_block_card:
            self.has_block_card = False
            return True
        return False

    def drink(self) -> None:
        """Record that the player has drunk and reset strikes."""
        self.drinks_consumed += 1
        self.reset_strikes()

    def clock_out(self) -> None:
        """Remove the player from the game."""
        self.is_active = False

    def must_drink(self) -> bool:
        """
        Check if the player must drink (3 strikes).

        Returns:
            bool: True if player has 3 or more strikes.
        """
        return self.strikes >= 3

    def get_status(self) -> Dict[str, Any]:
        """
        Get player's current status.

        Returns:
            Dict: Player information including name, strikes, and status.
        """
        return {
            'name': self.name,
            'strikes': self.strikes,
            'has_block_card': self.has_block_card,
            'is_active': self.is_active,
            'drinks_consumed': self.drinks_consumed
        }


class Game:
    """Main game controller managing game flow and state."""

    def __init__(self, data_manager: DataManager):
        """
        Initialize a game.

        Args:
            data_manager (DataManager): Instance managing question data.
        """
        self.data_manager = data_manager
        self.players: List[Player] = []
        self.current_player_index: Optional[int] = None
        self.current_question: Optional[Dict[str, Any]] = None
        self.current_question_player: Optional[Player] = None
        self.is_game_active = False
        self.round_number = 0
        self.game_history: List[Dict[str, Any]] = []

    def initialize_players(self, player_names: List[str]) -> bool:
        """
        Initialize game with player names.

        Args:
            player_names (List[str]): List of player names.

        Returns:
            bool: True if successful, False if invalid input.
        """
        if not player_names or len(player_names) < 1:
            return False

        self.players = [Player(name) for name in player_names]
        self.data_manager.reset_all_questions()
        self.is_game_active = True
        return True

    def start_game(self) -> bool:
        """
        Start the game.

        Returns:
            bool: True if game started successfully.
        """
        if not self.players:
            return False

        self.is_game_active = True
        self.round_number = 0
        self.current_player_index = 0
        return True

    def get_active_players(self) -> List[Player]:
        """
        Get list of active players.

        Returns:
            List[Player]: List of players still in the game.
        """
        return [p for p in self.players if p.is_active]

    def select_random_player(self) -> Optional[Player]:
        """
        Select a random active player.

        Returns:
            Optional[Player]: A random active player or None if no active players.
        """
        active = self.get_active_players()
        if not active:
            return None

        player = random.choice(active)
        self.current_player_index = self.players.index(player)
        self.current_question_player = player
        return player

    def draw_question(self) -> Optional[Dict[str, Any]]:
        """
        Draw a random unused question.

        Returns:
            Optional[Dict]: Question data or None if no questions available.
        """
        question = self.data_manager.get_random_unused_question()
        if question:
            self.current_question = question
            self.round_number += 1
        return question

    def player_answers(self, player: Player, answered_yes: bool) -> Dict[str, Any]:
        """
        Handle player answering the question.

        Args:
            player (Player): The player who is answering.
            answered_yes (bool): True if player said yes, False if player said no.

        Returns:
            Dict: Result containing strike info based on answer.
        """
        if not self.current_question:
            return {'strikes': 0, 'must_drink': False, 'answered_yes': answered_yes}

        result = {
            'player_name': player.name,
            'answered_yes': answered_yes,
            'strikes': player.strikes,
            'must_drink': False
        }

        # Only add strike if player answered YES
        if answered_yes:
            strikes = player.add_strike()
            result['strikes'] = strikes
            must_drink = player.must_drink()
            result['must_drink'] = must_drink

            if must_drink:
                player.drink()

        # Mark question as used
        self.data_manager.mark_question_used(self.current_question['id'])
        self.data_manager.save_questions()

        self.game_history.append(result)
        return result

    def use_block_card(self, blocker: Player) -> Optional[Player]:
        """
        Handle block card usage.

        Args:
            blocker (Player): The player using the block card.

        Returns:
            Optional[Player]: The player who must now answer (previous player).
        """
        if not blocker.use_block_card():
            return None

        # Get previous player (circular)
        current_idx = self.players.index(blocker)
        previous_idx = (current_idx - 1) % len(self.players)

        # Find previous active player
        attempts = 0
        while attempts < len(self.players):
            previous_player = self.players[previous_idx]
            if previous_player.is_active and previous_player != blocker:
                self.current_question_player = previous_player
                return previous_player
            previous_idx = (previous_idx - 1) % len(self.players)
            attempts += 1

        return None

    def player_clock_out(self, player: Player) -> bool:
        """
        Remove player from the game (clock out).

        Args:
            player (Player): The player clocking out.

        Returns:
            bool: True if successfully clocked out.
        """
        if not player.is_active:
            return False

        player.clock_out()

        # Mark question as used if it was answered during clock out
        if self.current_question:
            self.data_manager.mark_question_used(self.current_question['id'])
            self.data_manager.save_questions()

        result = {
            'player_name': player.name,
            'action': 'clock_out',
            'round': self.round_number
        }

        self.game_history.append(result)
        return True

    def is_game_over(self) -> bool:
        """
        Check if the game is over (only one or zero active players).

        Returns:
            bool: True if game is over.
        """
        active_count = len(self.get_active_players())
        return active_count <= 1

    def get_game_status(self) -> Dict[str, Any]:
        """
        Get complete game status.

        Returns:
            Dict: Current game state including all players, round, and active status.
        """
        return {
            'round': self.round_number,
            'is_active': self.is_game_active,
            'is_over': self.is_game_over(),
            'players': [p.get_status() for p in self.players],
            'active_players_count': len(self.get_active_players()),
            'unused_questions': self.data_manager.get_unused_count(),
            'current_question_player': self.current_question_player.name if self.current_question_player else None,
            'current_question': self.current_question.copy() if self.current_question else None
        }

    def get_final_results(self) -> Dict[str, Any]:
        """
        Get final game results.

        Returns:
            Dict: Final standings and winner.
        """
        # Sort by drinks consumed (most drinks = loser)
        sorted_players = sorted(self.players, key=lambda p: p.drinks_consumed, reverse=True)

        results = {
            'winner': sorted_players[-1].name if sorted_players else None,
            'loser': sorted_players[0].name if sorted_players else None,
            'standings': [
                {
                    'rank': idx + 1,
                    'name': p.name,
                    'drinks': p.drinks_consumed,
                    'strikes': p.strikes,
                    'block_card_used': not p.has_block_card
                }
                for idx, p in enumerate(sorted_players)
            ],
            'total_rounds': self.round_number,
            'game_history_length': len(self.game_history)
        }

        return results

    def get_player(self, name: str) -> Optional[Player]:
        """
        Get a player by name.

        Args:
            name (str): The player's name.

        Returns:
            Optional[Player]: The player or None if not found.
        """
        for player in self.players:
            if player.name.lower() == name.lower():
                return player
        return None

    def end_game(self) -> bool:
        """
        End the game.

        Returns:
            bool: True if game ended successfully.
        """
        self.is_game_active = False
        return True
