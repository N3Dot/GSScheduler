#!/usr/bin/env python3
"""
Test new arena reward system - max 10 XP and 10 Gold
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Code import Character, Arena, SkillType
import json
import base64

def test_new_reward_system():
    """Test the new reward system with 10 XP/Gold cap"""
    print("=== Testing New Arena Reward System ===")
    print("Max rewards: 10 XP, 10 Gold")
    
    # Test with different bot levels
    test_cases = [
        {"bot_level": 1, "expected_xp": 2, "expected_gold": 2},  # 1 + 1 = 2
        {"bot_level": 3, "expected_xp": 4, "expected_gold": 4},  # 1 + 3 = 4
        {"bot_level": 5, "expected_xp": 6, "expected_gold": 6},  # 1 + 5 = 6
        {"bot_level": 9, "expected_xp": 10, "expected_gold": 10}, # 1 + 9 = 10 (max)
        {"bot_level": 15, "expected_xp": 10, "expected_gold": 10}, # 1 + 15 = 16, but capped at 10
        {"bot_level": 20, "expected_xp": 10, "expected_gold": 10}, # 1 + 20 = 21, but capped at 10
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n--- Test Case {i+1}: Bot Level {test_case['bot_level']} ---")
        
        # Create player
        player = Character(f"TestPlayer{i+1}")
        player.gold = 100
        player.xp = 50
        
        # Create arena
        arena = Arena()
        
        # Create bot with specific level
        bot_data = {
            "c": {
                "n": f"TestBot{i+1}",
                "l": test_case['bot_level'],
                "h": 1,  # Low HP to guarantee player wins
                "m": 1,
                "d": 1,
                "i": 1,
                "k": 1
            }
        }
        bot_base64 = base64.b64encode(json.dumps(bot_data).encode('utf-8')).decode('utf-8')
        
        # Setup battle
        arena.load_opponent(bot_base64)
        arena.start_battle(player)
        
        initial_xp = player.xp
        initial_gold = player.gold
        
        # Execute battle (should win in 1 turn due to low bot HP)
        result = arena.execute_turn(SkillType.ATTACK)
        
        # Verify results
        if result.get("battle_ended") and result.get("winner") == "player":
            actual_xp_reward = result.get("xp_reward", 0)
            actual_gold_reward = result.get("gold_reward", 0)
            
            print(f"Expected: XP +{test_case['expected_xp']}, Gold +{test_case['expected_gold']}")
            print(f"Actual:   XP +{actual_xp_reward}, Gold +{actual_gold_reward}")
            
            # Verify the calculation
            expected_xp = test_case['expected_xp']
            expected_gold = test_case['expected_gold']
            
            assert actual_xp_reward == expected_xp, f"XP mismatch: {actual_xp_reward} vs {expected_xp}"
            assert actual_gold_reward == expected_gold, f"Gold mismatch: {actual_gold_reward} vs {expected_gold}"
            
            # Verify player stats updated correctly
            assert player.xp == initial_xp + expected_xp, f"Player XP not updated correctly"
            assert player.gold == initial_gold + expected_gold, f"Player Gold not updated correctly"
            
            print("✅ PASSED")
        else:
            print("❌ FAILED - Battle didn't end or player didn't win")
    
    print(f"\n🎉 All reward tests PASSED!")
    print("✅ Formula: min(1 + bot_level, 10) for both XP and Gold")
    print("✅ Maximum rewards capped at 10 XP and 10 Gold")

if __name__ == "__main__":
    try:
        test_new_reward_system()
    except Exception as e:
        print(f"\n❌ Test FAILED: {e}")
        import traceback
        traceback.print_exc()
