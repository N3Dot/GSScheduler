#!/usr/bin/env python3
"""
Final verification test for new reward system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Code import Character, Arena, SkillType
import json
import base64

def verify_reward_system():
    """Quick verification of the new reward system"""
    print("🔍 Final Verification: New Arena Reward System")
    
    # Test with high-level bot to ensure cap works
    player = Character("FinalTest")
    player.gold = 50
    player.xp = 20
    
    arena = Arena()
    
    # High level bot (should be capped at 10/10)
    bot_data = {
        "c": {"n": "HighLevelBot", "l": 50, "h": 1, "m": 1, "d": 1, "i": 1, "k": 1}
    }
    bot_base64 = base64.b64encode(json.dumps(bot_data).encode('utf-8')).decode('utf-8')
    
    arena.load_opponent(bot_base64)
    arena.start_battle(player)
    
    print(f"Before: XP={player.xp}, Gold={player.gold}")
    print(f"Bot Level: {arena.bot.level}")
    
    result = arena.execute_turn(SkillType.ATTACK)
    
    if result.get("battle_ended") and result.get("winner") == "player":
        xp_reward = result.get("xp_reward", 0)
        gold_reward = result.get("gold_reward", 0)
        
        print(f"After: XP={player.xp}, Gold={player.gold}")
        print(f"Rewards: XP +{xp_reward}, Gold +{gold_reward}")
        
        # Should be exactly 10/10 due to cap
        assert xp_reward == 10, f"XP reward should be 10, got {xp_reward}"
        assert gold_reward == 10, f"Gold reward should be 10, got {gold_reward}"
        
        print("✅ SUCCESS: Rewards capped at 10 XP and 10 Gold")
        print("✅ New formula working: min(1 + bot_level, 10)")
    else:
        print("❌ Battle test failed")

if __name__ == "__main__":
    verify_reward_system()
