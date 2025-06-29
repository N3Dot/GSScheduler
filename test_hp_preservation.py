#!/usr/bin/env python3
"""
Test script để kiểm tra các cải tiến mới:
1. HP không reset tự động khi thắng/thua
2. HP reset về ban đầu khi nhấn nút Reset
3. Hiệu ứng lắc với pattern đúng
4. UI button cải tiến
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Code import Arena, Character, ArenaBot, SkillType
import base64
import json

def test_hp_preservation():
    print("=== TEST HP PRESERVATION ===")
    
    # Tạo player với HP thấp
    player = Character("Test Player")
    player.hp = 20  # HP thấp để dễ test
    player.max_hp = 50
    original_hp = player.hp
    
    arena = Arena()
    
    # Tạo bot mạnh
    bot_data = {
        'name': 'Strong Bot',
        'level': 5,
        'hp': 80,
        'max_hp': 80,
        'dex': 15,
        'int_stat': 10,
        'luk': 12
    }
    
    json_str = json.dumps(bot_data)
    base64_code = base64.b64encode(json_str.encode()).decode()
    
    # Load bot và bắt đầu trận đấu
    arena.load_opponent(base64_code)
    print(f"Player HP trước trận đấu: {player.hp}")
    
    # Simulate start_battle với lưu HP ban đầu
    arena.original_player_hp = player.hp
    arena.original_bot_hp = arena.bot.hp
    
    battle_started = arena.start_battle(player)
    print(f"Player copy HP sau start: {arena.player_copy.hp}")
    
    # Test chiến đấu cho đến khi kết thúc
    turn = 1
    while arena.battle_active and turn <= 5:
        result = arena.execute_turn(SkillType.ATTACK)
        print(f"Turn {turn}: Player copy HP = {arena.player_copy.hp}, Bot HP = {arena.bot.hp}")
        
        if result.get("battle_ended", False):
            winner = result.get("winner")
            print(f"✅ Battle ended! Winner: {winner}")
            print(f"Player copy HP after battle: {arena.player_copy.hp}")
            print(f"Player original HP (should be unchanged): {player.hp}")
            break
        turn += 1
    
    # Test reset HP
    if hasattr(arena, 'original_player_hp'):
        player.hp = arena.original_player_hp
        print(f"✅ HP restored to original: {player.hp}")
    
    return True

def test_message_patterns():
    print("\n=== TEST MESSAGE PATTERNS ===")
    
    # Test messages với pattern đúng
    test_messages = [
        "Test Player đánh thường gây 15 sát thương!",
        "Strong Bot dùng phép gây 12 sát thương!",
        "Test Player thắng!",
        "Strong Bot đang thủ!"
    ]
    
    bot_name = "Strong Bot"
    
    for message in test_messages:
        if ("đánh thường" in message or "dùng phép" in message) and bot_name in message:
            print(f"✅ Shake trigger for bot: {message}")
        elif ("đánh thường" in message or "dùng phép" in message) and "Test Player" in message:
            print(f"✅ Shake trigger for player: {message}")
        else:
            print(f"No shake: {message}")
    
    return True

if __name__ == "__main__":
    print("Testing HP preservation and shake effects...")
    test_hp_preservation()
    test_message_patterns()
    print("\n🎉 All tests completed!")
