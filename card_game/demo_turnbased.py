"""
Demo script showing the turn-based game flow.
Each player takes turns answering questions in order.
"""

from data_manager import DataManager
from game_logic import Player, Game
from ui import GameUI
from scoreboard import Scoreboard

def demo_turn_based_game():
    """Demonstrate the new turn-based game flow."""
    print("=" * 70)
    print("  DEMOSTRACIÓN: JUEGO CON TURNOS EN ORDEN")
    print("=" * 70)
    
    # Initialize
    dm = DataManager("questions.csv")
    game = Game(dm)
    scoreboard = Scoreboard()
    
    # Create 3 players
    player_names = ["Alice", "Bob", "Carol"]
    game.initialize_players(player_names)
    
    print(f"\n✓ Jugadores: {', '.join(player_names)}")
    print(f"✓ Preguntas disponibles: {dm.get_unused_count()}")
    
    print("\n" + "=" * 70)
    print("FLUJO DEL JUEGO (Turnos en Orden)")
    print("=" * 70)
    
    active_players = game.get_active_players()
    print(f"\nJugadores activos: {len(active_players)}")
    
    # Simulate turns
    turn = 0
    current_player_index = 0
    
    while turn < 9 and not game.is_game_over():
        active_players = game.get_active_players()
        
        if len(active_players) <= 1:
            break
        
        # Get current player
        current_player_index = current_player_index % len(active_players)
        current_player = active_players[current_player_index]
        
        # Draw question
        question = game.draw_question()
        
        turn += 1
        print(f"\n--- TURNO {turn} ---")
        print(f"Jugador: {current_player.name}")
        print(f"Pregunta: {question['question']}")
        print(f"Respuesta correcta: {'SÍ' if question['correct_answer'] else 'NO'}")
        
        # Simulate answer
        if turn % 3 == 1:
            # First turn - correct answer
            answered = question['correct_answer']
            print(f"Respondió: {'SÍ' if answered else 'NO'} ✅ CORRECTO")
            result = game.player_answers(current_player, answered_yes=answered)
        elif turn % 3 == 2:
            # Second turn - incorrect answer
            answered = not question['correct_answer']
            print(f"Respondió: {'SÍ' if answered else 'NO'} ❌ INCORRECTO")
            result = game.player_answers(current_player, answered_yes=answered)
        else:
            # Third turn - correct answer
            answered = question['correct_answer']
            print(f"Respondió: {'SÍ' if answered else 'NO'} ✅ CORRECTO")
            result = game.player_answers(current_player, answered_yes=answered)
        
        print(f"Strikes actuales: {current_player.strikes}/3")
        
        if current_player.must_drink():
            current_player.drink()
            print(f"🍻 {current_player.name} ¡DEBE BEBER! (Strikes reset a 0)")
        
        # Move to next player
        current_player_index += 1
        
        # Show current standings
        print(f"\nEstadísticas:")
        for i, p in enumerate(active_players):
            print(f"  {i+1}. {p.name}: {p.strikes} strikes, {p.drinks_consumed} bebidas")
    
    print("\n" + "=" * 70)
    print("✓ DEMOSTRACIÓN COMPLETA")
    print("=" * 70)
    print("\nMécanica implementada:")
    print("✓ Jugadores seleccionados al inicio")
    print("✓ Cada jugador responde en su turno (en orden)")
    print("✓ Máximo 3 strikes por jugador")
    print("✓ Strikes SOLO al responder correctamente")
    print("✓ 3 strikes = 1 bebida (y reset de strikes)")
    print("=" * 70)

if __name__ == "__main__":
    demo_turn_based_game()
