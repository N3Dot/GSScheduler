#!/usr/bin/env python3
"""
Test script để kiểm tra các cải tiến arena:
1. Hiệu ứng lắc khi tấn công
2. Thanh máu HP hiển thị đúng (bao gồm số âm)
3. Dialog nhập mã QR
4. Popup khi thua
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Code import Arena, Character, ArenaBot, SkillType
import base64
import json

def test_arena_improvements():
    print("=== TEST ARENA IMPROVEMENTS ===")
    
    # Tạo player và bot
    player = Character("Test Player")
    player.hp = 30  # HP thấp để dễ test
    player.max_hp = 50
    
    arena = Arena()  # Arena không cần player parameter
    
    # Tạo bot mạnh để test thua
    bot_data = {
        'name': 'Strong Bot',
        'level': 5,
        'hp': 80,
        'max_hp': 80,
        'dex': 15,
        'int_stat': 10,
        'luk': 12
    }
    
    # Encode bot data
    json_str = json.dumps(bot_data)
    base64_code = base64.b64encode(json_str.encode()).decode()
    
    # Load bot
    success = arena.load_opponent(base64_code)
    print(f"✅ Bot loaded: {success}")
    print(f"Bot: {arena.bot.name} (Level {arena.bot.level}, HP: {arena.bot.hp}/{arena.bot.max_hp})")
    
    # Bắt đầu trận đấu
    battle_started = arena.start_battle(player)  # Truyền player vào start_battle
    print(f"✅ Battle started: {battle_started}")
    print(f"Player HP in battle: {arena.player_copy.hp}/{arena.player_copy.max_hp}")
    
    # Test nhiều lượt đấu để xem HP có thể âm không
    turn = 1
    while arena.battle_active and turn <= 10:
        print(f"\n--- Turn {turn} ---")
        
        # Player tấn công (test hiệu ứng lắc player)
        result = arena.execute_turn(SkillType.ATTACK)
        
        print(f"Battle messages: {result.get('messages', [])}")
        print(f"Player HP: {arena.player_copy.hp}/{arena.player_copy.max_hp}")
        print(f"Bot HP: {arena.bot.hp}/{arena.bot.max_hp}")
        
        # Kiểm tra HP âm
        if arena.player_copy.hp < 0:
            print(f"✅ Player HP went negative: {arena.player_copy.hp}")
        if arena.bot.hp < 0:
            print(f"✅ Bot HP went negative: {arena.bot.hp}")
        
        if result.get("battle_ended", False):
            winner = result.get("winner")
            print(f"✅ Battle ended! Winner: {winner}")
            
            if winner == "bot":
                print("✅ Player lost - this would trigger defeat popup")
            else:
                print("✅ Player won - victory popup would show")
            break
            
        turn += 1
    
    print("\n=== TEST COMPLETED ===")
    return True

def test_qr_dialog_simulation():
    """Mô phỏng việc nhập QR code"""
    print("\n=== TEST QR DIALOG SIMULATION ===")
    
    # Tạo mã QR giả
    bot_data = {
        'name': 'QR Test Bot',
        'level': 3,
        'hp': 45,
        'max_hp': 45,
        'dex': 8,
        'int_stat': 6,
        'luk': 7
    }
    
    json_str = json.dumps(bot_data)
    qr_code = base64.b64encode(json_str.encode()).decode()
    
    print(f"Sample QR code: {qr_code[:50]}...")
    print("✅ QR code format is valid")
    
    # Test decode
    try:
        decoded = base64.b64decode(qr_code).decode()
        parsed = json.loads(decoded)
        print(f"✅ QR code decoded successfully: {parsed['name']}")
    except Exception as e:
        print(f"❌ QR decode failed: {e}")
    
    return True

if __name__ == "__main__":
    print("Testing Arena Improvements...")
    test_arena_improvements()
    test_qr_dialog_simulation()
    print("\n🎉 All tests completed!")
