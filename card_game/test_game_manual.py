"""
Manual game testing script to verify scoring works correctly.
This simulates a game session where:
1. Player 1 answers a question correctly (should add strike)
2. Player 2 answers a question incorrectly (should NOT add strike)
3. Player 1 reaches 3 strikes and drinks (resets to 0 strikes)
"""

from data_manager import DataManager
from game_logic import Player, Game
from scoreboard import Scoreboard

def test_scoring_logic():
    """Test that scoring works correctly."""
    print("=" * 60)
    print("PARTY GAME SCORING SYSTEM TEST")
    print("=" * 60)
    
    # Initialize game
    dm = DataManager("questions.csv")
    game = Game(dm)
    sb = Scoreboard()
    
    # Create players
    players = [Player("Alice"), Player("Bob")]
    game.initialize_players([p.name for p in players])
    
    print(f"\n✓ Created {len(players)} players: {', '.join([p.name for p in players])}")
    
    # Test 1: Player answers correctly (should add strike)
    print("\n" + "-" * 60)
    print("TEST 1: CORRECT ANSWER (should add strike)")
    print("-" * 60)
    
    game.draw_question()
    question = game.current_question
    correct_answer = question['correct_answer']
    
    print(f"Question: {question['question']}")
    print(f"Correct answer: {'Yes' if correct_answer else 'No'}")
    
    player = game.players[0]
    result = game.player_answers(player, answered_yes=correct_answer)
    
    print(f"\n→ Alice answered: {'Yes' if result['answered_yes'] else 'No'}")
    print(f"✓ Is correct: {result['is_correct']}")
    print(f"✓ Alice strikes: {player.strikes}")
    
    assert result['is_correct'] is True, "Answer should be correct!"
    assert player.strikes == 1, "Strike should be added for correct answer!"
    print("✓ TEST 1 PASSED: Strike was correctly added!")
    
    # Test 2: Player answers incorrectly (should NOT add strike)
    print("\n" + "-" * 60)
    print("TEST 2: INCORRECT ANSWER (should NOT add strike)")
    print("-" * 60)
    
    game.draw_question()
    question = game.current_question
    correct_answer = question['correct_answer']
    incorrect_answer = not correct_answer  # Answer opposite
    
    print(f"Question: {question['question']}")
    print(f"Correct answer: {'Yes' if correct_answer else 'No'}")
    
    player = game.players[1]
    strikes_before = player.strikes
    result = game.player_answers(player, answered_yes=incorrect_answer)
    
    print(f"\n→ Bob answered: {'Yes' if result['answered_yes'] else 'No'}")
    print(f"✓ Is correct: {result['is_correct']}")
    print(f"✓ Bob strikes before: {strikes_before}")
    print(f"✓ Bob strikes after: {player.strikes}")
    
    assert result['is_correct'] is False, "Answer should be incorrect!"
    assert player.strikes == strikes_before, "Strike should NOT be added for incorrect answer!"
    print("✓ TEST 2 PASSED: Strike was NOT added for incorrect answer!")
    
    # Test 3: Multiple correct answers trigger drinking
    print("\n" + "-" * 60)
    print("TEST 3: THREE CORRECT ANSWERS → DRINKING")
    print("-" * 60)
    
    player = game.players[0]
    player.strikes = 0  # Reset strikes for this test
    
    for i in range(1, 4):
        game.draw_question()
        question = game.current_question
        correct_answer = question['correct_answer']
        
        result = game.player_answers(player, answered_yes=correct_answer)
        
        print(f"\nRound {i}:")
        print(f"  Question: {question['question']}")
        print(f"  Answered: {'Yes' if result['answered_yes'] else 'No'} (Correct)")
        print(f"  Strikes: {player.strikes}")
        
        if player.must_drink():
            print(f"  🍻 {player.name} must drink!")
            player.drink()
            print(f"  Drinks consumed: {player.drinks_consumed}")
            print(f"  Strikes reset: {player.strikes}")
            break
    
    assert player.drinks_consumed == 1, "Player should have consumed 1 drink!"
    assert player.strikes == 0, "Strikes should be reset after drinking!"
    print("\n✓ TEST 3 PASSED: Drinking system works correctly!")
    
    # Summary
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED! ✓")
    print("=" * 60)
    print("\nSummary:")
    print(f"✓ Correct answers ADD strikes")
    print(f"✓ Incorrect answers DO NOT add strikes")
    print(f"✓ 3 strikes trigger drinking and reset counter")
    print(f"✓ Scoring system works as intended!")
    print("=" * 60)

if __name__ == "__main__":
    test_scoring_logic()
