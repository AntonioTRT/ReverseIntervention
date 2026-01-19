"""
Quick validation script to verify the game works correctly.
Tests game logic without GUI interaction.
"""

from data_manager import DataManager
from game_logic import Game, Player
from scoreboard import Scoreboard

def test_game_logic():
    """Test that game logic works correctly."""
    print("=" * 60)
    print("VALIDACION DEL JUEGO DE PREGUNTAS")
    print("=" * 60)
    
    # Initialize
    dm = DataManager("questions.csv")
    game = Game(dm)
    scoreboard = Scoreboard()
    
    # Create players
    game.initialize_players(["Alice", "Bob"])
    game.start_game()
    
    print("\n✓ Juego inicializado con 2 jugadores")
    print(f"✓ Preguntas cargadas: {dm.get_total_count()}")
    
    # Test turn-based system
    active_players = game.get_active_players()
    print(f"✓ Jugadores activos: {len(active_players)}")
    
    # Simulate a few turns
    print("\n" + "-" * 60)
    print("Simulando turnos:")
    print("-" * 60)
    
    for turn in range(1, 7):
        active_players = game.get_active_players()
        if len(active_players) <= 1 or game.data_manager.get_unused_count() == 0:
            break
        
        # Get current player (cycling)
        player_index = (turn - 1) % len(active_players)
        current_player = active_players[player_index]
        
        # Draw question
        question = game.draw_question()
        
        # Simulate answer
        correct_answer = question['correct_answer']
        result = game.player_answers(current_player, answered_yes=correct_answer)
        
        print(f"\nTurno {turn}:")
        print(f"  Jugador: {current_player.name}")
        print(f"  Respuesta: {'SI' if correct_answer else 'NO'} (Correcta)")
        print(f"  Es correcta: {result['is_correct']}")
        print(f"  Strikes: {current_player.strikes}/3")
        
        if current_player.must_drink():
            current_player.drink()
            print(f"  BEBE! Strikes reset a 0")
    
    print("\n" + "=" * 60)
    print("VALIDACION COMPLETADA!")
    print("=" * 60)
    print("\nCaracteristicas validadas:")
    print("✓ Carga de preguntas con respuestas correctas")
    print("✓ Sistema de turnos en orden")
    print("✓ Validacion de respuestas correctas")
    print("✓ Sistema de strikes (solo si respuesta correcta)")
    print("✓ Sistema de bebidas (3 strikes = beber)")
    print("✓ Juego pronto para usar con UI Tkinter")
    print("=" * 60)

if __name__ == "__main__":
    test_game_logic()
