"""
Scoreboard Module
Tracks drinking events and strike history.
"""

from typing import List, Dict, Any
from datetime import datetime


class Event:
    """Represents a game event (strike, drink, clock out)."""

    def __init__(self, event_type: str, player_name: str, details: Dict[str, Any]):
        """
        Initialize an event.

        Args:
            event_type (str): Type of event ('strike', 'drink', 'clock_out', 'block_card').
            player_name (str): Name of the player involved.
            details (Dict): Additional event details.
        """
        self.event_type = event_type
        self.player_name = player_name
        self.details = details
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert event to dictionary.

        Returns:
            Dict: Event data.
        """
        return {
            'event_type': self.event_type,
            'player_name': self.player_name,
            'timestamp': self.timestamp.isoformat(),
            'details': self.details
        }


class Scoreboard:
    """Tracks all game events and statistics."""

    def __init__(self):
        """Initialize scoreboard."""
        self.events: List[Event] = []
        self.player_drinks: Dict[str, int] = {}
        self.player_strikes: Dict[str, int] = {}

    def record_strike(self, player_name: str, strike_count: int, must_drink: bool) -> None:
        """
        Record a strike event.

        Args:
            player_name (str): The player who received the strike.
            strike_count (int): Total strikes after this one.
            must_drink (bool): Whether the player must drink.
        """
        event = Event('strike', player_name, {
            'strike_count': strike_count,
            'must_drink': must_drink
        })
        self.events.append(event)
        self.player_strikes[player_name] = strike_count

    def record_drink(self, player_name: str, drink_count: int) -> None:
        """
        Record a drinking event.

        Args:
            player_name (str): The player who is drinking.
            drink_count (int): Total drinks by this player.
        """
        event = Event('drink', player_name, {
            'drink_count': drink_count
        })
        self.events.append(event)
        self.player_drinks[player_name] = drink_count

    def record_clock_out(self, player_name: str, round_number: int) -> None:
        """
        Record a player clocking out.

        Args:
            player_name (str): The player clocking out.
            round_number (int): Round number when clocked out.
        """
        event = Event('clock_out', player_name, {
            'round': round_number
        })
        self.events.append(event)

    def record_block_card_used(self, player_name: str, target_player: str) -> None:
        """
        Record a block card usage.

        Args:
            player_name (str): The player using the block card.
            target_player (str): The player forced to answer.
        """
        event = Event('block_card', player_name, {
            'target_player': target_player
        })
        self.events.append(event)

    def get_player_drinks(self, player_name: str) -> int:
        """
        Get total drinks for a player.

        Args:
            player_name (str): The player's name.

        Returns:
            int: Total drinks consumed.
        """
        return self.player_drinks.get(player_name, 0)

    def get_player_strikes(self, player_name: str) -> int:
        """
        Get total strikes for a player (current session).

        Args:
            player_name (str): The player's name.

        Returns:
            int: Current strikes.
        """
        return self.player_strikes.get(player_name, 0)

    def get_all_events(self) -> List[Dict[str, Any]]:
        """
        Get all recorded events.

        Returns:
            List[Dict]: All events in order.
        """
        return [event.to_dict() for event in self.events]

    def get_events_by_player(self, player_name: str) -> List[Dict[str, Any]]:
        """
        Get all events involving a specific player.

        Args:
            player_name (str): The player's name.

        Returns:
            List[Dict]: Events involving this player.
        """
        player_events = [e for e in self.events if e.player_name == player_name]
        return [event.to_dict() for event in player_events]

    def get_strike_history(self) -> Dict[str, List[int]]:
        """
        Get strike progression for each player.

        Returns:
            Dict: Player names mapped to list of strike counts.
        """
        strike_history = {}

        for event in self.events:
            if event.event_type == 'strike':
                if event.player_name not in strike_history:
                    strike_history[event.player_name] = []
                strike_history[event.player_name].append(event.details['strike_count'])

        return strike_history

    def get_drinking_history(self) -> Dict[str, List[int]]:
        """
        Get drinking progression for each player.

        Returns:
            Dict: Player names mapped to list of drink counts.
        """
        drinking_history = {}

        for event in self.events:
            if event.event_type == 'drink':
                if event.player_name not in drinking_history:
                    drinking_history[event.player_name] = []
                drinking_history[event.player_name].append(event.details['drink_count'])

        return drinking_history

    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the game.

        Returns:
            Dict: Summary including total events, drinks per player, strikes per player.
        """
        return {
            'total_events': len(self.events),
            'player_drinks': self.player_drinks.copy(),
            'player_strikes': self.player_strikes.copy(),
            'total_drinking_events': sum(1 for e in self.events if e.event_type == 'drink'),
            'total_strike_events': sum(1 for e in self.events if e.event_type == 'strike'),
            'total_clock_outs': sum(1 for e in self.events if e.event_type == 'clock_out'),
            'total_block_cards_used': sum(1 for e in self.events if e.event_type == 'block_card')
        }

    def clear(self) -> None:
        """Clear all recorded events."""
        self.events.clear()
        self.player_drinks.clear()
        self.player_strikes.clear()
