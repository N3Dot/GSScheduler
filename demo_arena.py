#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Code import Arena, Character, RewardSystem, StudyAnalytics, QuestSystem

def main():
    # Tạo character
    character = Character("Test Player")
    character.level = 5
    character.hp = 80
    character.max_hp = 100
    character.dex = 10
    character.int = 8
    character.luk = 12
    
    # Tạo arena
    reward_system = RewardSystem()
    quest_system = QuestSystem()
    analytics = StudyAnalytics(quest_system)
    arena = Arena(character)
    
    print("=== Test Hệ Thống Đấu Trường ===")
    print(f"Player: {character.name} (Lv.{character.level})")
    print(f"HP: {character.hp}/{character.max_hp}")
    print(f"Stats: DEX={character.dex}, INT={character.int}, LUK={character.luk}")
    
    # Tạo bot demo
    demo_code = arena.generate_demo_opponent()
    success = arena.load_opponent(demo_code)
    
    if success:
        print(f"\nBot loaded: {arena.bot.name} (Lv.{arena.bot.level})")
        print(f"Bot HP: {arena.bot.hp}/{arena.bot.max_hp}")
        print(f"Bot Stats: DEX={arena.bot.dex}, INT={arena.bot.int_stat}, LUK={arena.bot.luk}")
        
        # Bắt đầu trận đấu
        arena.start_battle()
        print("\n=== Trận đấu bắt đầu! ===")
        
        # Mô phỏng một vài lượt
        from Backend.Code import SkillType
        turn = 1
        while arena.battle_active and turn <= 5:
            print(f"\n--- Lượt {turn} ---")
            skill = SkillType.ATTACK if turn % 2 == 1 else SkillType.MAGIC
            result = arena.execute_turn(skill)
            
            for message in result["messages"]:
                print(message)
            
            print(f"Player HP: {character.hp}/{character.max_hp}")
            print(f"Bot HP: {arena.bot.hp}/{arena.bot.max_hp}")
            
            if result["battle_ended"]:
                winner = "Player" if result["winner"] == "player" else "Bot"
                print(f"\n🎉 {winner} thắng!")
                break
                
            turn += 1
        
        if not result.get("battle_ended", False):
            print("\nDemo kết thúc sau 5 lượt!")
    
    else:
        print("Không thể load bot!")
    
    print("\n=== Demo Base64 Codes ===")
    from Backend.Code import generate_demo_base64_codes
    codes = generate_demo_base64_codes(3)
    for i, code in enumerate(codes, 1):
        print(f"Code {i}: {code}")

if __name__ == "__main__":
    main()
